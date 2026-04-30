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
- Python 3.6+
- An Obsidian vault (any local directory)
- Git (recommended but optional)

## Installation

Clone the repo:

```bash
git clone https://github.com/Hermon803/claude-obsidian-organizer.git ~/.claude/skills/organize
```

### Set environment variables

Set `VAULT_PATH` and `SKILL_PATH` in global Claude Code settings:

```bash
cat >> ~/.claude/settings.local.json << 'EOF'
{
  "env": {
    "VAULT_PATH": "/path/to/your/vault",
    "SKILL_PATH": "/root/.claude/skills/organize"
  }
}
EOF
```

Or set them in your shell profile (`~/.bashrc` / `~/.zshrc`):

```bash
export VAULT_PATH="/path/to/your/vault"
export SKILL_PATH="$HOME/.claude/skills/organize"
```

### Set up vault structure

The skill auto-creates templates on first use. No manual setup needed.

Just point `VAULT_PATH` to any directory (even an empty one) and start organizing.

All index files (`_directory-map.md`, `_index.md`, `_tags.md`, `_graph.md`) and PARA directories (`areas/`, `projects/`, `resources/`, `journal/`, `ideas/`) are created on demand as you organize content.

## Usage

In Claude Code, use:

```
/organize <content>                              — Classify and save text
/organize                                        — Organize current conversation
/organize --title "My Title" <content>           — Specify a custom title
/organize --name "FileName" <content>             — Specify a custom filename
/organize --title "X" --name "Y" <content>        — Specify both title and filename
```

### Classification Scoring

The skill uses heuristic guidance (not a precise algorithm) to score content against directories. It verifies keyword matches explicitly before deciding:

| Guideline | Action |
|-----------|--------|
| Strong match (≈≥7) | Auto-classify |
| Moderate match (≈4-6) | Show top-2 candidates |
| Weak/no match (≈<4) | Ask if new category needed |

## File Structure

```
claude-obsidian-organizer/
├── SKILL.md               # Skill definition (English)
├── SKILL.zh-CN.md         # Skill definition (Chinese)
├── README.md              # This file
├── README.zh-CN.md        # Chinese README
├── CONVENTIONS.md         # Writing conventions guide
├── scripts/               # Python tooling
│   ├── search.py          # Full-text search
│   ├── stats.py           # Vault statistics
│   ├── orphans.py         # Orphan note detection
│   └── backlinks.py       # Backlink finder
├── templates/             # Obsidian note templates
│   ├── note.md            # Generic note (English)
│   ├── note.zh-CN.md      # Generic note (Chinese)
│   ├── area.md            # Long-term focus area
│   ├── area.zh-CN.md      # Chinese version
│   ├── project.md         # Goal-oriented project
│   ├── project.zh-CN.md   # Chinese version
│   ├── resource.md        # Reference/resource
│   ├── resource.zh-CN.md  # Chinese version
│   ├── idea.md            # Idea/thought
│   ├── idea.zh-CN.md      # Chinese version
│   ├── journal.md         # Daily journal
│   └── journal.zh-CN.md   # Chinese version
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
- **Built-in tooling** — Python scripts for reliable search, stats, and link analysis

## License

MIT
