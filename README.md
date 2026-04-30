# Claude Obsidian Organizer

A **Claude Code slash command** that intelligently classifies conversation content into an Obsidian knowledge base. Automatically analyzes content, matches the best directory, creates well-formatted notes, updates indices, and commits to Git.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Slash%20Command-8A2BE2)](https://claude.ai/code)
[![Obsidian](https://img.shields.io/badge/Obsidian-Knowledge%20Base-7C3AED)](https://obsidian.md)

## Features

- **Smart Classification** — AI-powered content analysis with keyword scoring, type matching, and context awareness
- **Template-based Notes** — Clean YAML frontmatter notes using customizable Obsidian templates
- **Auto Indexing** — Automatically updates `_index.md`, `_tags.md`, and `_graph.md` after every operation
- **Git Integration** — Auto-commits and pushes changes to your vault's Git repository
- **Bidirectional Links** — Searches and builds `[[related]]` links between notes
- **New Category Support** — Detects when content doesn't fit existing directories and helps create new ones

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- An Obsidian vault (any local directory)
- Git repository initialized in your vault

## Installation

One line:

```bash
mkdir -p ~/.claude/skills/organize && \
curl -fsSL https://raw.githubusercontent.com/Hermon803/claude-obsidian-organizer/main/SKILL.md \
  -o ~/.claude/skills/organize/SKILL.md
```

### Set vault path

Set `VAULT_PATH` in global Claude Code settings:

```bash
cat >> ~/.claude/settings.local.json << 'EOF'
{
  "env": {
    "VAULT_PATH": "/path/to/your/vault"
  }
}
EOF
```

Or set it in your shell profile (`~/.bashrc` / `~/.zshrc`):

```bash
export VAULT_PATH="/path/to/your/vault"
```

### Set up vault structure

Make sure your vault has these directories and files (copy `templates/` and `examples/` from this repo):

```
your-vault/
├── _directory-map.md       # Directory classification table
├── _index.md               # Vault index
├── _tags.md                # Tag index
├── _graph.md               # Relationship graph
├── CONVENTIONS.md          # Writing conventions
├── templates/              # Note templates (copy from this repo)
├── areas/                  # Long-term focus areas
├── projects/               # Goal-oriented projects
├── resources/              # References & learning notes
├── journal/                # Daily logs
└── ideas/                  # Idea drafts
```

### Initialize indices

Create the initial `_directory-map.md` from the example provided in this repo, then start organizing!

## Usage

In Claude Code, use:

```
/organize <content>                    — Classify and save text
/organize                              — Organize current conversation
/organize --title "My Title" <content> — Specify a custom title
```

### Classification Scoring

The skill scores content against your directories:

| Score | Action |
|-------|--------|
| ≥ 7   | Auto-classify |
| 4–6   | Show top-2 candidates for you to choose |
| < 4   | Ask if a new category is needed |

## File Structure

```
claude-obsidian-organizer/
├── SKILL.md               # The core Claude Code slash command
├── README.md              # This file
├── CONVENTIONS.md         # Writing conventions guide
├── templates/             # Obsidian note templates
│   ├── note.md            # Generic note
│   ├── area.md            # Long-term focus area
│   ├── project.md         # Goal-oriented project
│   ├── resource.md        # Reference/resource
│   ├── idea.md            # Idea/thought
│   └── journal.md         # Daily journal
└── examples/              # Example vault files
    ├── _directory-map.md  # Classification mapping
    ├── _index.md          # Vault index
    ├── _tags.md           # Tag index
    └── _graph.md          # Relationship graph
```

## Examples

### Scenario 1: Learning a new technology

```
You: I just finished a tutorial on React hooks and want to save notes.
Claude: /organize I just finished a tutorial on React hooks. Key points: useState for local state, useEffect for side effects, useContext for dependency injection...
```

The skill auto-detects this as a `resource` type, matches to `resources/` or `CodeNotebook/React/`, creates a formatted note, and updates all indices.

### Scenario 2: Planning a project

```
You: /organize I'm planning to build a personal website with Astro. Goals: portfolio + blog, deadline: end of month.
```

Auto-detected as `project` type, filed under `projects/`, with goal and deadline in frontmatter.

## Customization

- **Templates**: Edit the `templates/*.md` files to match your note-taking style
- **Directory mapping**: Edit `_directory-map.md` to add keywords that match your content domains
- **Scoring rules**: Modify the scoring logic in `SKILL.md` if you want different sensitivity

## Why This Approach

Unlike plugins that require Obsidian to be running, this skill works entirely at the filesystem level via Claude Code:

- **No plugins needed** — Works with any Obsidian vault, even without Obsidian running
- **AI-powered classification** — Goes beyond simple keyword matching to understand content context
- **Version-controlled** — Git integration means every note is backed up
- **Prompt-driven** — No external binaries or dependencies beyond Claude Code itself

## License

MIT
