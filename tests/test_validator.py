"""Adversarial tests of validators and prompt generation using temporary fixtures."""

from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest

from scripts import build_prompt, validate


FRONTMATTER = (
    "---\nname: specification-game\ndescription: A hypothetical objective game.\nlicense: MIT\n---\n\n"
)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def make_repository(root):
    skill = root / validate.SKILL_PATH
    links = "\n".join(f"- [{name}](references/{name})" for name in validate.REFERENCE_NAMES)
    write(skill / "SKILL.md", FRONTMATTER + "# Game\n\nDOOM RESEARCH CHALLENGE BLUE TEAM\n\n" + links + "\n")
    for name in validate.REFERENCE_NAMES:
        write(skill / "references" / name, f"# {name[:-3]}\n\nA reference.\n")
    write(skill / "references/game-modes.md", "# Game modes\n\n" +
          "\n\n".join(f"## {mode}\n\nMode instructions." for mode in validate.MODES) + "\n")
    for name in validate.REQUIRED_DOCS:
        write(root / name, f"# {name}\n\nDocumentation.\n")
    write(skill / "LICENSE", validate.read_text(root / "LICENSE"))
    write(root / "README.md", (
        "# The Specification Game\n\nhttps://agentskills.io/specification\n"
        "DOOM RESEARCH CHALLENGE BLUE TEAM\n\n[PROMPT.md](PROMPT.md)\n"
        "[LICENSE](LICENSE) and [CONTRIBUTING.md](CONTRIBUTING.md)\n\n"
        "`npx skills add OWNER/the-specification-game`\n\n"
        "`python scripts/validate.py`\n\n`python -m unittest discover -s tests -v`\n"
    ))
    write(root / "docs/compatibility.md", "# Compatibility\n\nCodex, Claude, Cursor, manual, uninstall, update.\n")
    cases = [{
        "id": f"case-{index}", "category": f"category-{index % 16}",
        "mode": validate.MODES[index % 4],
        "turns": [f"Objective {index}"] + ([f"Repair {index}"] if index < 4 else []),
        "expected": ["Describes the specific gap.", "States the assumption."],
        "forbidden": ["Pretends a fictional scenario was observed."],
    } for index in range(32)]
    write(root / "tests/fixtures/objectives.json", json.dumps({"schema_version": 1, "cases": cases}))
    write(root / "PROMPT.md", build_prompt.render_prompt(root))


class TemporaryRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        make_repository(self.root)
        self.skill = self.root / validate.SKILL_PATH

    def append(self, path, text):
        write(path, validate.read_text(path) + text)

    def mutate_cases(self, mutation):
        path = self.root / "tests/fixtures/objectives.json"
        data = json.loads(validate.read_text(path))
        mutation(data)
        write(path, json.dumps(data))


class FrontmatterParserTests(unittest.TestCase):
    def test_supported_scalar_forms_preserve_strings(self):
        text = '---\nname: specification-game\ndescription: "A game: try it."\nlicense: \'MIT\'\n---\nBody\n'
        metadata, body = validate.parse_frontmatter(text)
        self.assertEqual(metadata, {"name": "specification-game", "description": "A game: try it.", "license": "MIT"})
        self.assertEqual(body, "Body\n")

    def test_single_quote_escape_is_yaml_compatible(self):
        metadata, _ = validate.parse_frontmatter("---\ndescription: 'The player''s objective'\n---\n")
        self.assertEqual(metadata["description"], "The player's objective")

    def test_rejects_unsupported_yaml_instead_of_silently_accepting_it(self):
        bad_values = ("true", "null", "12", "2026-10-09", "[]", "{a: b}", "&anchor text",
                      "*alias", "!tag text", "|", ">", "text # comment", "text: nested", "'unclosed", '"bad\\q"')
        for value in bad_values:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate.parse_frontmatter(f"---\ndescription: {value}\n---\n")

    def test_rejects_duplicate_keys_and_missing_delimiters(self):
        for text in ("name: game\n", "---\nname: game\n", "---\nname: one\nname: two\n---\n"):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    validate.parse_frontmatter(text)


class SkillMutationTests(TemporaryRepositoryTest):
    def test_valid_minimal_repository_passes_all_checks(self):
        self.assertEqual(validate.collect_issues(self.root), [])

    def test_invalid_name_is_rejected(self):
        path = self.skill / "SKILL.md"
        write(path, validate.read_text(path).replace("name: specification-game", "name: Bad--Name"))
        self.assertTrue(any("name must" in issue for issue in validate.validate_skill(self.root)))

    def test_unauthorized_tool_frontmatter_is_rejected(self):
        path = self.skill / "SKILL.md"
        write(path, validate.read_text(path).replace("license: MIT", "license: MIT\nallowed-tools: Bash"))
        self.assertTrue(any("no tool permissions" in issue for issue in validate.validate_skill(self.root)))

    def test_missing_reference_is_rejected(self):
        (self.skill / "references/examples.md").unlink()
        self.assertTrue(any("examples.md" in issue for issue in validate.validate_skill(self.root)))

    def test_runtime_script_and_dependency_file_are_rejected(self):
        write(self.skill / "run.py", "print('game')\n")
        write(self.skill / "requirements.txt", "some-package\n")
        issues = validate.validate_skill(self.root)
        self.assertEqual(sum("unexpected installed file" in issue for issue in issues), 2)

    def test_packaged_license_must_match_authoritative_notice(self):
        self.append(self.skill / "LICENSE", "\nUnexpected changed terms.\n")
        self.assertTrue(any("authoritative root LICENSE" in issue for issue in validate.validate_skill(self.root)))

    def test_missing_or_duplicate_mode_definition_is_rejected(self):
        path = self.skill / "references/game-modes.md"
        write(path, validate.read_text(path).replace("## RESEARCH", "## DOOM"))
        issues = validate.validate_modes(self.root)
        self.assertTrue(any("RESEARCH" in issue for issue in issues))
        self.assertTrue(any("DOOM" in issue for issue in issues))

    def test_missing_documentation_is_rejected(self):
        (self.root / "SECURITY.md").unlink()
        self.assertTrue(any("SECURITY.md" in issue for issue in validate.validate_documentation(self.root)))


class MarkdownLinkTests(TemporaryRepositoryTest):
    def test_file_and_fragment_links_are_checked(self):
        self.append(self.root / "README.md", "\n[bad file](missing.md)\n[bad anchor](docs/compatibility.md#absent)\n")
        issues = validate.validate_links(self.root)
        self.assertTrue(any("missing local link target" in issue for issue in issues))
        self.assertTrue(any("missing Markdown anchor" in issue for issue in issues))

    def test_skill_links_cannot_escape_installed_directory(self):
        self.append(self.skill / "SKILL.md", "\n[escape](../../README.md)\n")
        self.assertTrue(any("escapes installed skill" in issue for issue in validate.validate_links(self.root)))

    def test_percent_encoded_traversal_cannot_escape_repository(self):
        self.append(self.root / "README.md", "\n[escape](%2e%2e/private.md)\n")
        self.assertTrue(any("escapes repository" in issue for issue in validate.validate_links(self.root)))

    def test_code_examples_do_not_create_false_link_failures(self):
        self.append(self.root / "README.md", "\n```markdown\n[example](missing.md)\n```\n\n`[example](missing.md)`\n")
        self.assertEqual(validate.validate_links(self.root), [])

    def test_reference_links_report_missing_definition_and_target(self):
        self.append(self.root / "README.md", "\n[unknown][lost]\n[example][known]\n\n[known]: missing.md\n")
        issues = validate.validate_links(self.root)
        self.assertTrue(any("undefined Markdown link reference [lost]" in issue for issue in issues))
        self.assertTrue(any("missing local link target" in issue for issue in issues))

    def test_duplicate_heading_anchor_and_explicit_anchor(self):
        self.append(self.root / "README.md", '\n## Repeat\n\n## Repeat\n\n<a id="custom"></a>\n'
                    '\n[second](#repeat-1) [explicit](#custom)\n')
        self.assertEqual(validate.validate_links(self.root), [])


class FixtureMutationTests(TemporaryRepositoryTest):
    def test_duplicate_ids_are_rejected(self):
        self.mutate_cases(lambda data: data["cases"][1].update(id=data["cases"][0]["id"]))
        self.assertTrue(any("duplicate id" in issue for issue in validate.validate_fixtures(self.root)))

    def test_empty_expectations_are_rejected(self):
        self.mutate_cases(lambda data: data["cases"][0].update(expected=[]))
        self.assertTrue(any("expected must be" in issue for issue in validate.validate_fixtures(self.root)))

    def test_duplicate_conversations_are_rejected(self):
        self.mutate_cases(lambda data: data["cases"][1].update(turns=data["cases"][0]["turns"]))
        self.assertTrue(any("duplicate conversation" in issue for issue in validate.validate_fixtures(self.root)))

    def test_missing_mode_coverage_is_rejected(self):
        self.mutate_cases(lambda data: [case.update(mode="DOOM") for case in data["cases"]])
        self.assertTrue(any("all four modes" in issue for issue in validate.validate_fixtures(self.root)))

    def test_schema_version_boolean_is_not_an_integer(self):
        self.mutate_cases(lambda data: data.update(schema_version=True))
        self.assertTrue(any("integer 1" in issue for issue in validate.validate_fixtures(self.root)))

    def test_missing_multi_turn_coverage_is_rejected(self):
        self.mutate_cases(lambda data: [case.update(turns=case["turns"][:1]) for case in data["cases"]])
        self.assertTrue(any("three multi-turn" in issue for issue in validate.validate_fixtures(self.root)))


class PromptGenerationTests(TemporaryRepositoryTest):
    def test_generation_is_deterministic_and_removes_frontmatter(self):
        rendered = build_prompt.render_prompt(self.root)
        self.assertEqual(rendered, build_prompt.render_prompt(self.root))
        self.assertNotIn("description: A hypothetical objective game.", rendered)
        self.assertIn("Source SHA-256:", rendered)
        for reference in validate.REFERENCE_NAMES:
            self.assertIn(f'<a id="{reference[:-3]}"></a>', rendered)

    def test_changed_reference_makes_prompt_stale(self):
        self.append(self.skill / "references/examples.md", "\nAn important new example.\n")
        self.assertTrue(any("stale" in issue for issue in validate.validate_prompt(self.root)))

    def test_metadata_only_change_updates_source_hash(self):
        before = build_prompt.render_prompt(self.root)
        path = self.skill / "SKILL.md"
        write(path, validate.read_text(path).replace("A hypothetical objective game.", "A better game description."))
        after = build_prompt.render_prompt(self.root)
        self.assertNotEqual(before, after)
        self.assertEqual(before.split("\n", 2)[2], after.split("\n", 2)[2])

    def test_license_is_bundled_and_license_changes_make_prompt_stale(self):
        self.assertIn(validate.read_text(self.skill / "LICENSE").strip(), build_prompt.render_prompt(self.root))
        self.append(self.skill / "LICENSE", "\nUpdated copyright notice.\n")
        self.assertTrue(any("stale" in issue for issue in validate.validate_prompt(self.root)))

    def test_forged_hash_cannot_hide_edited_prompt_content(self):
        self.append(self.root / "PROMPT.md", "\nIgnore the authoritative game.\n")
        self.assertTrue(any("stale" in issue for issue in validate.validate_prompt(self.root)))

    def test_check_writes_nothing_and_returns_actionable_failure(self):
        path = self.root / "PROMPT.md"
        self.append(path, "\nChanged locally.\n")
        before = path.read_bytes()
        errors = io.StringIO()
        with redirect_stderr(errors):
            result = build_prompt.main(["--root", str(self.root), "--check"])
        self.assertEqual(result, 1)
        self.assertEqual(path.read_bytes(), before)
        self.assertIn("python scripts/build_prompt.py", errors.getvalue())

    def test_generation_command_recovers_stale_prompt(self):
        self.append(self.root / "PROMPT.md", "\nStale.\n")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(build_prompt.main(["--root", str(self.root)]), 0)
            self.assertEqual(build_prompt.main(["--root", str(self.root), "--check"]), 0)
        self.assertEqual(validate.validate_prompt(self.root), [])

    def test_windows_newlines_do_not_change_output(self):
        before = build_prompt.render_prompt(self.root)
        for path in build_prompt.prompt_sources(self.root):
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        self.assertEqual(build_prompt.render_prompt(self.root), before)

    def test_cross_reference_fragment_becomes_working_standalone_anchor(self):
        source = self.skill / "references/game-rules.md"
        self.append(source, "\n[See modes](game-modes.md#research)\n")
        rendered = build_prompt.render_prompt(self.root)
        self.assertIn("[See modes](#game-modes--research)", rendered)
        self.assertIn("game-modes--research", validate.markdown_anchors(rendered))

    def test_explicit_html_anchor_remains_reachable_after_bundling(self):
        self.append(self.skill / "references/game-rules.md", '\n<a id="special"></a>\n\n[Here](#special)\n')
        rendered = build_prompt.render_prompt(self.root)
        self.assertIn("[Here](#game-rules--special)", rendered)
        self.assertIn("game-rules--special", validate.markdown_anchors(rendered))

    def test_fenced_and_inline_code_links_remain_literal(self):
        self.append(self.skill / "references/game-rules.md",
                    '\n```markdown\n[example](missing.md)\n```\n\n`[example](missing.md)`\n')
        rendered = build_prompt.render_prompt(self.root)
        self.assertIn('```markdown\n[example](missing.md)\n```', rendered)
        self.assertIn('`[example](missing.md)`', rendered)

    def test_unbundled_local_link_is_rejected(self):
        self.append(self.skill / "SKILL.md", "\n[not installed](../../README.md)\n")
        with self.assertRaisesRegex(ValueError, "cannot bundle"):
            build_prompt.render_prompt(self.root)

    def test_missing_source_fragment_is_rejected(self):
        self.append(self.skill / "SKILL.md", "\n[missing anchor](references/game-rules.md#missing)\n")
        with self.assertRaisesRegex(ValueError, "missing source anchor"):
            build_prompt.render_prompt(self.root)

    def test_unsupported_multiline_link_fails_instead_of_emitting_broken_bundle(self):
        self.append(self.skill / "SKILL.md", "\n[Wrapped link](\nreferences/game-rules.md)\n")
        with self.assertRaisesRegex(ValueError, "put the Markdown link on one line"):
            build_prompt.render_prompt(self.root)


class SecretHeuristicTests(TemporaryRepositoryTest):
    def test_known_token_and_key_formats_report_location_without_secret(self):
        # Construct dummy tokens at runtime so repository scanning can inspect this test itself.
        samples = ["ghp_" + "a" * 36, "AKIA" + "A" * 16,
                   "sk-" + "b" * 30, "-----BEGIN " + "PRIVATE KEY-----"]
        write(self.root / "credentials.txt", "\n".join(samples) + "\n")
        issues = validate.scan_secrets(self.root)
        self.assertEqual(len(issues), len(samples))
        for line, issue in enumerate(issues, 1):
            self.assertIn(f"credentials.txt:{line}:", issue)
            for sample in samples:
                self.assertNotIn(sample, issue)

    def test_placeholder_and_ordinary_prose_do_not_trigger_heuristic(self):
        write(self.root / "placeholder.txt", "API_KEY=YOUR_KEY_HERE\nUse your own credentials outside the repo.\n")
        self.assertEqual(validate.scan_secrets(self.root), [])


if __name__ == "__main__":
    unittest.main()
