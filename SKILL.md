---
name: organize
version: 1.0.0
description: |
  Organize conversation content into an Obsidian knowledge base — auto-classify, smart archive, update indices, Git push.
  Triggered when: organize, 整理, 归类, save to vault, organize notes, categorize
Triggers: organize, 整理, 归类, 保存笔记, 存到仓库, 归档, 分类保存, 整理当前对话, save to vault, organize notes, categorize
---

# /organize — Note Organizing Assistant

Classify conversation content or specified text into an Obsidian knowledge base. Automatically analyze content, match the best directory, create formatted notes, update indices, and commit to Git.

> This is a **Claude Code custom slash command**. Install it in your project's `.claude/skills/organize/SKILL.md`.

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- An Obsidian vault (any local directory)
- Git repository initialized in the vault

## Installation

1. Create the skills directory in your Claude Code config:

   ```bash
   mkdir -p ~/.claude/skills/organize
   ```

2. Copy this file to `~/.claude/skills/organize/SKILL.md`

3. Replace `$VAULT_PATH` in this file with the absolute path to your Obsidian vault

## Vault Configuration

The `/organize` skill expects your vault to have this structure:

```
your-vault/
├── _directory-map.md       # Directory classification table (auto-maintained)
├── _index.md               # Vault index
├── _tags.md                # Tag index
├── _graph.md               # Relationship graph
├── CONVENTIONS.md          # Writing conventions
├── templates/              # Note templates
│   ├── note.md
│   ├── area.md
│   ├── project.md
│   ├── resource.md
│   ├── idea.md
│   └── journal.md
├── areas/                  # Long-term focus areas
├── projects/               # Goal-oriented projects
├── resources/              # References & learning notes
├── journal/                # Daily logs
└── ideas/                  # Idea drafts
```

## Usage

```
/organize <content>          — Classify and save text directly
/organize                     — Organize current conversation into notes
/organize --title "xxx" <content>  — Specify a custom title
```

## Core Workflow

### Step 1: Read Directory Map

Read `_directory-map.md` to get all directory classifications and keyword mappings.
If the file doesn't exist, scan the vault directory structure and create it.

### Step 2: Content Analysis — Find Best Directory

Score content against directories using:

1. **Keyword matching**: Match content keywords against each directory's Keywords in `_directory-map.md`
2. **Semantic judgment**: Determine note type from content nature (area/project/resource/idea/journal)
3. **Context clues**: If from conversation, note user scenarios ("learning X" → resource, "planning X" → project)

Scoring (max 10):
- **Direct hit** (keyword exactly matches): +4
- **Type match** (content type aligns with directory type): +3
- **Partial match** (keyword partially related): +2
- **Directory activity** (recently updated directories get priority): +1

### Step 3: Decision

| Condition | Action |
|-----------|--------|
| Highest score ≥ 7 | Auto-assign, inform user |
| 4 ≤ highest score < 7 | Show top-2 candidates, let user choose |
| Highest score < 4 | Inform user no suitable directory found, ask if new category needed |
| Tie | Priority: project > area > resource > idea > journal |

### Step 4: Create New Category (if needed)

When no matching directory:
1. Inform user no suitable directory exists
2. Analyze core topic, suggest 2-3 candidate directory names
3. Let user confirm or provide their own
4. Add new entry to `_directory-map.md`
5. Create physical directory and `_index.md`

### Step 5: Create Note

Follow `CONVENTIONS.md` and templates:

1. Read the template for the matched type (`templates/{type}.md`)
2. Replace all `{{}}` placeholders with actual values
3. Extract title from content (or use `--title` argument)
4. File naming: lowercase-hyphens (English) or original text (Chinese), no spaces
5. Write to the selected directory

### Step 6: Update Indices

1. Update the directory's `_index.md` (add file entry)
2. Update `_tags.md` (add new tags)
3. Update `_graph.md` (if related notes exist)
4. Search for related notes and build bidirectional links

### Step 7: Git Commit & Push

```bash
cd $VAULT_PATH
git add -A
git commit -m "organize: <title>"
git push
```

If git push fails (network/permission), keep the local commit and inform user.

## Directory Types & Templates

| Prefix | Type | Template | Description |
|--------|------|----------|-------------|
| areas/ | area | `templates/area.md` | Long-term focus areas |
| projects/ | project | `templates/project.md` | Goal-oriented projects |
| resources/ | resource | `templates/resource.md` | References & learning |
| journal/ | journal | `templates/journal.md` | Work logs |
| ideas/ | idea | `templates/idea.md` | Idea drafts |

## Classification Quick Reference

| Content Type | Recommended Directory | Reason |
|-------------|----------------------|--------|
| Programming, frameworks, language features | `CodeNotebook/<subcategory>/` | Tech notes |
| AI/ML/Deep Learning | `CodeNotebook/AI/` | Highest keyword match |
| Daily learning | `resources/` | References |
| Personal ideas, inspiration | `ideas/` | Unpolished ideas |
| Work plans, progress | `projects/` | Goal-oriented |
| Long-term focus areas | `areas/` | No-deadline ongoing |
| Daily records, work summaries | `journal/` | Timeline logs |
| Exam preparation | `exam-notes/` | Exam-specific |
| Personal diary | `diary/` | Private records |

## Special Handling

1. **Diary/Log**: Personal life records → `diary/`; Work summaries → `journal/`
2. **Code snippets**: Content with code blocks → `CodeNotebook/<subcategory>/`
3. **Mixed topics**: Extract main topic for primary category, link secondary topics in `related`
4. **Short content (< 50 chars)**: Suggest `ideas/` or capture instead of full note
5. **Similar existing notes**: Search vault, ask user if appending is preferred

## Directory Map Maintenance

After each `/organize` run, check `_directory-map.md`:
- New directory created? Add entry
- Directory accumulated many notes? Update description and keywords
- Directory empty for long time? Ask user if keeping

## Error Handling

| Error | Handling |
|-------|----------|
| Empty content | Prompt user for content |
| Directory doesn't exist | Run new-category workflow |
| Git push fails | Keep local commit, inform user |
| Filename conflict | Append timestamp |
| Template missing | Use standard frontmatter template |
