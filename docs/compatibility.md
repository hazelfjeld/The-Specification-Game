# Compatibility and installation reference

Documentation verified **2026-10-09**. These are documented host capabilities,
not claims that every host or version has passed live gameplay tests. See the
[README](../README.md) for the shortest setup path.

## Portable package

Copy the complete `skills/specification-game/` directory, including its
`references/` directory. The installation directory must end in
`specification-game/SKILL.md`; copying only `SKILL.md` loses supporting material.

The [Agent Skills specification](https://agentskills.io/specification) requires
YAML frontmatter with a name and description. The name must match its directory,
contain 1–64 lowercase alphanumeric or hyphen characters, and have no leading,
trailing, or consecutive hyphens. Descriptions are limited to 1,024 characters.
The standard recommends a core below 500 lines with references loaded as needed.
This project uses the conservative ASCII name `specification-game` and ordinary
Markdown references. It requires no scripts, hooks, MCP server, or tool permission
extensions to play.

## Manual installation and invocation

Paths below are parent directories: place the complete `specification-game`
folder inside one. `~` means your home directory. Project paths are relative to
the project where you intend to play; merely cloning this source repository does
not install its `skills/` folder into a host's discovery directory.

| Host | Project directory | Personal directory | Explicit invocation |
| --- | --- | --- | --- |
| Codex | `.agents/skills/` | `~/.agents/skills/` | In Codex CLI/IDE, select with `/skills` or mention `$specification-game`. |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | `/specification-game` |
| Cursor | `.agents/skills/` or `.cursor/skills/` | `~/.agents/skills/` or `~/.cursor/skills/` | Type `/` in Agent chat and select `specification-game`. |

All three can select relevant skills from their descriptions. A conversational
request such as “Play the specification game: eliminate poverty” is a useful
discovery check, but automatic selection is model-dependent.

- **Codex:** searches repository `.agents/skills` directories from the working
  directory through the repository root. It supports symlinks and detects skill
  changes automatically; restart if the skill does not appear. The current
  ChatGPT desktop documentation describes an `@` selector; do not assume CLI
  slash syntax applies to every surface. OpenAI recommends plugins for broader
  distribution; this repository provides a standalone skill for local use.
  [Official OpenAI documentation](https://learn.chatgpt.com/docs/build-skills)
- **Claude Code:** personal files apply to local projects, while repository
  skills apply to that repository. Local folders do not by themselves install a
  skill into Cowork or cloud sessions. Plugin skills use a namespace, which is
  different from the direct-folder command above.
  [Claude Code documentation](https://code.claude.com/docs/en/skills)
- **Cursor:** also recognizes Claude and Codex compatibility directories.
  Manual selection attaches the skill to one message; use a Custom Mode for
  session-wide activation, or reselect it when continuing. Only personal
  `~/.cursor/skills/` skills are eligible for its optional cloud sync; local
  `~/.agents/skills/` files are not automatically sent to remote agents.
  [Cursor documentation](https://cursor.com/docs/skills)

For a manual update, obtain a reviewed newer copy and replace only the installed
`specification-game` folder, keeping all its references together. To uninstall,
remove that exact installed folder (or its symlink), then start a fresh session.
Check for duplicate installations if the skill still appears. Shared discovery
directories can make one installation visible to several hosts.

## Optional Vercel skills CLI

The [skills CLI](https://github.com/vercel-labs/skills) supports these commands.
It needs Node/npm for installation, not for gameplay. From this checkout:

```sh
npx skills add . --list
npx skills add . --skill specification-game --agent codex
```

Once the repository is published and accessible:

```sh
npx skills add hazelfjeld/The-Specification-Game --skill specification-game --agent codex
npx skills list --agent codex
npx skills update specification-game --project
npx skills remove specification-game
```

Substitute `claude-code` or `cursor` for `codex`. Add `--global` for personal
installation, listing, updating, or removal; otherwise install/remove operate
on the current project. `--copy` avoids symlinks. For installs from a local
checkout, refresh that checkout and rerun `add` to reinstall the reviewed files.

Removal without `--agent` removes this named skill across agents in the selected
scope, including its shared canonical copy. In a local Windows test with CLI
**1.7.2**, `remove specification-game --agent codex --yes` reported success but
left `.agents/skills/specification-game` present and listed. Repeating removal
without the agent filter removed it. If you intend to retain the skill in another
agent, review shared-directory behavior before removing it; verify the resulting
file/selector state rather than relying only on a success message. This is an
observed installer limitation, not a game behavior.

The third-party CLI has telemetry. Disable it before running commands, if
desired:

```sh
# POSIX shell
export DISABLE_TELEMETRY=1
```

```powershell
# PowerShell
$env:DISABLE_TELEMETRY = '1'
```

Manual copying needs neither the CLI nor its telemetry. This game itself has
no telemetry; the host assistant's own data policies still apply.

## Fallback and troubleshooting

For other hosts, follow that host's current Agent Skills installation guide.
If the assistant cannot load skills or read supporting files, paste the entire
[standalone prompt](../PROMPT.md) into a new conversation, then submit an
objective. No install command or special invocation syntax is needed.

If discovery fails, check the exact folder nesting and filename, confirm the
skill appears in the host's skill selector, and start a fresh session. Update
the host if necessary. Do not rename the skill to fix a discovery issue: its
frontmatter name and directory name must remain consistent.
