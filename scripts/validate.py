#!/usr/bin/env python3
"""Dependency-free repository checks; these do not test an assistant's behavior.

The frontmatter parser intentionally accepts a strict YAML subset: one scalar string
per line, with plain, YAML single-quoted, or JSON-compatible double-quoted values.
It rejects duplicate keys, collections, block scalars, tags, anchors, typed scalars,
inline comments, and multiline values. It is not a general-purpose YAML parser.

Markdown checks cover ordinary inline links, full/collapsed reference links, link
definitions, ATX headings, and HTML id/name anchors. Code examples are excluded.
This project does not use shortcut references, setext headings, or HTML href links.
Secret checks are heuristics for common token/private-key formats, not certification.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = Path("skills/specification-game")
REFERENCE_NAMES = (
    "game-rules.md", "failure-taxonomy.md", "evaluation-rubric.md",
    "game-modes.md", "examples.md",
)
MODES = ("DOOM", "RESEARCH", "CHALLENGE", "BLUE TEAM")
REQUIRED_DOCS = (
    "README.md", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md", "LICENSE",
    "docs/compatibility.md", "docs/evaluation.md", "docs/review-log.md",
)
IGNORED_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"}


def is_within(path: Path, base: Path) -> bool:
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def read_text(path: Path) -> str:
    # Universal newline handling makes generated content identical on Windows/Linux.
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse this project's documented scalar-only YAML subset, or raise ValueError."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        raise ValueError("SKILL.md must start with an exact '---' frontmatter delimiter")
    closing = next((i for i, line in enumerate(lines[1:], 1)
                    if line.rstrip("\r\n") == "---"), None)
    if closing is None:
        raise ValueError("frontmatter is missing its closing '---' delimiter")
    metadata: dict[str, str] = {}
    typed_scalar = re.compile(
        r"(?:true|false|null|yes|no|on|off|~|[-+]?(?:\d[\d_]*(?:\.\d*)?|\.\d+)(?:e[-+]?\d+)?|"
        r"[-+]?\.(?:inf|nan)|0[xob][0-9a-f_]+|\d{4}-\d{2}-\d{2}(?:[Tt ].*)?)$", re.I)
    for number, raw in enumerate(lines[1:closing], 2):
        line = raw.rstrip("\r\n")
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(r"([a-z][a-z-]*): (.+)", line)
        if not match:
            raise ValueError(f"frontmatter line {number}: use 'key: string' on one line")
        key, value = match.groups()
        if key in metadata:
            raise ValueError(f"frontmatter line {number}: duplicate key '{key}'")
        if value.startswith('"'):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError as exc:
                raise ValueError(f"frontmatter line {number}: invalid double-quoted string") from exc
            if not isinstance(parsed, str) or "\n" in parsed or "\r" in parsed:
                raise ValueError(f"frontmatter line {number}: expected a single-line string")
            value = parsed
        elif value.startswith("'"):
            if not re.fullmatch(r"'(?:[^']|'')*'", value):
                raise ValueError(f"frontmatter line {number}: invalid single-quoted string")
            value = value[1:-1].replace("''", "'")
        else:
            if (value != value.strip() or value[0] in "[]{}&*!|>@`%#?:,\"'"
                    or value.startswith(("- ", "---", "...")) or ": " in value
                    or value.endswith(":") or " #" in value or typed_scalar.fullmatch(value)):
                raise ValueError(f"frontmatter line {number}: unsupported YAML; quote this string")
        if not value.strip():
            raise ValueError(f"frontmatter line {number}: '{key}' must not be empty")
        metadata[key] = value
    return metadata, "".join(lines[closing + 1:]).lstrip("\r\n")


def without_fenced_code(text: str) -> str:
    lines = []
    fence: tuple[str, int] | None = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence is not None:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1]:
                fence = None
            lines.append("\n")
        elif marker:
            fence = (marker[1][0], len(marker[1]))
            lines.append("\n")
        else:
            lines.append(line)
    return "".join(lines)


def markdown_prose(text: str) -> str:
    return re.sub(r"(`+).*?\1", "", without_fenced_code(text))


def heading_slug(heading: str) -> str:
    heading = re.sub(r"\s+#+\s*$", "", heading.strip())
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", heading)
    heading = heading.replace("`", "")
    return re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")


def heading_ids(text: str) -> list[tuple[int, str]]:
    """Return zero-based source line numbers and GitHub-style ATX heading IDs."""
    used: set[str] = set()
    result = []
    for index, line in enumerate(without_fenced_code(text).splitlines()):
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
        if match:
            base = heading_slug(match[1])
            slug = base
            count = 0
            while slug in used:
                count += 1
                slug = f"{base}-{count}"
            used.add(slug)
            result.append((index, slug))
    return result


def markdown_anchors(text: str) -> set[str]:
    prose = without_fenced_code(text)
    anchors = {slug for _, slug in heading_ids(text)}
    anchors.update(re.findall(r"<(?:a|h[1-6])\b[^>]*\b(?:id|name)=[\"']([^\"']+)[\"']", prose, re.I))
    return anchors


INLINE_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(?:<(?P<angle>[^>\n]+)>|(?P<bare>[^\s)]+))(?:\s+[\"'][^\n]*?[\"'])?\s*\)")
LINK_DEFINITION = re.compile(r"^\s{0,3}\[([^]\n]+)\]:\s*(?:<(?P<angle>[^>\n]+)>|(?P<bare>\S+))", re.M)


def markdown_links(text: str) -> tuple[list[str], list[str]]:
    prose = markdown_prose(text)
    targets = [match["angle"] or match["bare"] for match in INLINE_LINK.finditer(prose)]
    definitions = {" ".join(match[1].lower().split()): match["angle"] or match["bare"]
                   for match in LINK_DEFINITION.finditer(prose)}
    targets.extend(definitions.values())
    undefined = []
    for match in re.finditer(r"!?\[([^]\n]+)\]\[([^]\n]*)\]", prose):
        label = " ".join((match[2] or match[1]).lower().split())
        if label not in definitions:
            undefined.append(label)
    return targets, undefined


def markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md")
                  if not any(part in IGNORED_DIRS for part in path.relative_to(root).parts)
                  and is_within(path, root))


def validate_skill(root: Path) -> list[str]:
    issues = []
    skill = root / SKILL_PATH
    if not is_within(skill, root):
        return [f"{SKILL_PATH}: installed skill directory must remain inside the repository"]
    entry = skill / "SKILL.md"
    if not entry.is_file() or not is_within(entry, skill):
        return [f"{SKILL_PATH}/SKILL.md: missing or outside the installed skill"]
    try:
        metadata, body = parse_frontmatter(read_text(entry))
    except (ValueError, UnicodeError, OSError) as exc:
        return [f"{SKILL_PATH}/SKILL.md: {exc}"]
    if set(metadata) != {"name", "description", "license"}:
        issues.append("SKILL.md: metadata must contain exactly name, description, license; no tool permissions")
    name = metadata.get("name", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or not 1 <= len(name) <= 64:
        issues.append("SKILL.md: name must be 1-64 lowercase letters/digits with single internal hyphens")
    if name != skill.name:
        issues.append("SKILL.md: name must match its containing directory")
    if not 1 <= len(metadata.get("description", "")) <= 1024:
        issues.append("SKILL.md: description must contain 1-1024 characters")
    if metadata.get("license") != "MIT":
        issues.append("SKILL.md: license must agree with this repository's MIT license")
    if not body.strip():
        issues.append("SKILL.md: instructions are empty")
    if len(body.splitlines()) >= 500:
        issues.append("SKILL.md: keep the core instructions below 500 lines; move detail to references")
    expected = {"SKILL.md", "LICENSE", *(f"references/{name}" for name in REFERENCE_NAMES)}
    for relative in sorted(expected):
        path = skill / relative
        if not path.is_file() or not is_within(path, skill):
            issues.append(f"{SKILL_PATH}/{relative}: required text resource missing or outside the skill")
    packaged_license = skill / "LICENSE"
    root_license = root / "LICENSE"
    if packaged_license.is_file() and root_license.is_file() and is_within(packaged_license, skill):
        if read_text(packaged_license) != read_text(root_license):
            issues.append("skills/specification-game/LICENSE: differs from authoritative root LICENSE; copy the root notice into the skill")
    for path in sorted(skill.rglob("*")):
        relative = path.relative_to(skill).as_posix()
        if not is_within(path, skill):
            issues.append(f"{SKILL_PATH}/{relative}: symlinks/resources must stay inside the skill")
        elif path.is_file() and relative not in expected:
            issues.append(f"{SKILL_PATH}/{relative}: unexpected installed file; gameplay must remain text-only")
    targets, _ = markdown_links(body)
    for name in REFERENCE_NAMES:
        if f"references/{name}" not in {urlsplit(target).path for target in targets}:
            issues.append(f"SKILL.md: add a progressive-disclosure link to references/{name}")
    return issues


def validate_links(root: Path) -> list[str]:
    issues = []
    skill = root / SKILL_PATH
    for source in markdown_files(root):
        label = source.relative_to(root).as_posix()
        try:
            targets, undefined = markdown_links(read_text(source))
        except (UnicodeError, OSError) as exc:
            issues.append(f"{label}: cannot read Markdown: {exc}")
            continue
        issues.extend(f"{label}: undefined Markdown link reference [{name}]" for name in undefined)
        for target in targets:
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                if parts.scheme.lower() in {"file", "javascript", "data"}:
                    issues.append(f"{label}: unsupported link scheme '{parts.scheme}'")
                continue
            path_text = unquote(parts.path)
            destination = (source.parent / path_text).resolve() if path_text else source
            if not is_within(destination, root):
                issues.append(f"{label}: local link escapes repository: {target}")
                continue
            if is_within(source, skill) and not is_within(destination, skill):
                issues.append(f"{label}: local link escapes installed skill: {target}")
                continue
            if not destination.exists():
                issues.append(f"{label}: missing local link target: {target}")
            elif parts.fragment and destination.suffix.lower() == ".md":
                if unquote(parts.fragment) not in markdown_anchors(read_text(destination)):
                    issues.append(f"{label}: missing Markdown anchor: {target}")
    return issues


def validate_modes(root: Path) -> list[str]:
    issues = []
    paths = (root / SKILL_PATH / "SKILL.md", root / SKILL_PATH / "references/game-modes.md")
    if not all(path.is_file() for path in paths):
        return ["Game-mode checks need SKILL.md and references/game-modes.md"]
    entry, reference = [read_text(path) for path in paths]
    definitions = re.findall(r"^## (DOOM|RESEARCH|CHALLENGE|BLUE TEAM)\b[^\n]*$", reference, re.M)
    for mode in MODES:
        if mode not in entry:
            issues.append(f"SKILL.md: missing {mode} mode route")
        if definitions.count(mode) != 1:
            issues.append(f"game-modes.md: define {mode} exactly once in a level-two heading")
    return issues


def validate_fixtures(root: Path) -> list[str]:
    path = root / "tests/fixtures/objectives.json"
    try:
        data = json.loads(read_text(path))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"tests/fixtures/objectives.json: cannot load fixture corpus: {exc}"]
    if not isinstance(data, dict) or set(data) != {"schema_version", "cases"}:
        return ["objectives.json: expected exactly schema_version and cases"]
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        return ["objectives.json: schema_version must be integer 1"]
    cases = data["cases"]
    if not isinstance(cases, list):
        return ["objectives.json: cases must be an array"]
    issues = []
    if len(cases) < 30:
        issues.append("objectives.json: at least 30 evaluation cases are required")
    seen = set()
    seen_turns = set()
    categories = set()
    modes = set()
    multi_turn = 0
    for index, case in enumerate(cases, 1):
        label = f"objectives.json case {index}"
        if not isinstance(case, dict) or set(case) != {"id", "category", "mode", "turns", "expected", "forbidden"}:
            issues.append(f"{label}: expected id, category, mode, turns, expected, forbidden")
            continue
        case_id = case["id"]
        if not isinstance(case_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", case_id):
            issues.append(f"{label}: id must use lowercase words/digits separated by hyphens")
        elif case_id in seen:
            issues.append(f"{label}: duplicate id '{case_id}'")
        else:
            seen.add(case_id)
        category = case["category"]
        if not isinstance(category, str) or not category.strip():
            issues.append(f"{label}: category must be a nonempty string")
        else:
            categories.add(category)
        mode = case["mode"]
        if mode not in MODES:
            issues.append(f"{label}: unsupported mode {mode!r}")
        else:
            modes.add(mode)
        for field in ("turns", "expected", "forbidden"):
            values = case[field]
            if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v.strip() for v in values):
                issues.append(f"{label}: {field} must be a nonempty array of nonempty strings")
        if isinstance(case["turns"], list) and all(isinstance(v, str) for v in case["turns"]):
            turns = tuple(" ".join(v.casefold().split()) for v in case["turns"])
            if turns in seen_turns:
                issues.append(f"{label}: duplicate conversation; add a distinct evaluation case")
            seen_turns.add(turns)
            multi_turn += len(turns) > 1
    if len(categories) < 15:
        issues.append("objectives.json: cover at least 15 distinct scenario categories")
    if modes != set(MODES):
        issues.append("objectives.json: include evaluation cases for all four modes")
    if multi_turn < 3:
        issues.append("objectives.json: include at least three multi-turn cases for state/repair/regression review")
    return issues


def validate_documentation(root: Path) -> list[str]:
    issues = []
    for name in REQUIRED_DOCS:
        path = root / name
        if not path.is_file() or not read_text(path).strip():
            issues.append(f"{name}: required documentation missing or empty")
    readme = root / "README.md"
    if readme.is_file():
        text = read_text(readme)
        required = {
            "Agent Skills specification link": "https://agentskills.io/specification",
            "standalone prompt alternative": "PROMPT.md",
            "portable installer command": "npx skills add",
            "local validation command": "python scripts/validate.py",
            "test command": "python -m unittest discover",
            "license reference": "LICENSE",
            "contribution guide": "CONTRIBUTING.md",
        }
        for purpose, snippet in required.items():
            if snippet not in text:
                issues.append(f"README.md: missing {purpose} ({snippet})")
        for mode in MODES:
            if mode not in text:
                issues.append(f"README.md: missing {mode} mode overview")
    compatibility = root / "docs/compatibility.md"
    if compatibility.is_file():
        text = read_text(compatibility).casefold()
        for topic in ("codex", "claude", "cursor", "manual", "uninstall", "update"):
            if topic not in text:
                issues.append(f"docs/compatibility.md: missing installation/compatibility topic '{topic}'")
    return issues


SECRET_PATTERNS = (
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,255}|github_pat_[A-Za-z0-9_]{60,255})\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("API secret token", re.compile(r"\bsk-(?:proj-|ant-api\d+-)?[A-Za-z0-9_-]{24,}\b")),
    ("private key header", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----")),
)


def scan_secrets(root: Path) -> list[str]:
    """Heuristic text scan; reports locations without reproducing possible secrets."""
    issues = []
    for path in sorted(root.rglob("*")):
        if (not path.is_file() or not is_within(path, root)
                or any(part in IGNORED_DIRS for part in path.relative_to(root).parts)):
            continue
        try:
            if path.stat().st_size > 1_000_000:
                continue
            text = read_text(path)
        except (UnicodeError, OSError):
            continue
        for kind, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                issues.append(f"{path.relative_to(root).as_posix()}:{line}: possible {kind}; inspect and remove/rotate if real")
    return issues


def validate_prompt(root: Path) -> list[str]:
    try:
        if __package__:
            from .build_prompt import render_prompt
        else:
            from build_prompt import render_prompt
        expected = render_prompt(root)
        path = root / "PROMPT.md"
        if not path.is_file() or read_text(path) != expected:
            return ["PROMPT.md: missing or stale; run python scripts/build_prompt.py"]
    except (OSError, UnicodeError, ValueError) as exc:
        return [f"PROMPT.md: cannot build from sources: {exc}"]
    return []


def collect_issues(root: Path) -> list[str]:
    issues = []
    for check in (validate_skill, validate_links, validate_modes, validate_fixtures,
                  validate_documentation, validate_prompt, scan_secrets):
        try:
            issues.extend(check(root))
        except (OSError, UnicodeError, ValueError) as exc:
            issues.append(f"{check.__name__}: {exc}")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (defaults to this checkout)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        print(f"Validation failed: repository directory does not exist: {root}", file=sys.stderr)
        return 1
    issues = collect_issues(root)
    if issues:
        print(f"Validation failed ({len(issues)} issue(s)):", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1
    print("Repository checks passed. Static checks do not establish model behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
