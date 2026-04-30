---
name: organize
version: 1.1.0
description: |
  Organize conversation content into an Obsidian knowledge base — auto-classify, smart archive, update indices, Git push.
  Triggered when: organize, 整理, 归类, save to vault, organize notes, categorize
Triggers: organize, 整理, 归类, 保存笔记, 存到仓库, 归档, 分类保存, 整理当前对话, save to vault, organize notes, categorize
---

# /organize — Note Organizing Assistant

Classify conversation content or specified text into an Obsidian knowledge base. Automatically analyze content, match the best directory, create formatted notes, update indices, and commit to Git.

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Python 3.6+
- An Obsidian vault (any local directory) with `$VAULT_PATH` set to its absolute path
- Git repository initialized in your vault — **recommended but optional**; the skill operates without git

## Installation

Clone the repo:

```bash
git clone https://github.com/Hermon803/claude-obsidian-organizer.git ~/.claude/skills/organize
```

### Set environment variables

Add to `~/.claude/settings.local.json`:

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

## Vault Configuration

The `/organize` skill works with this structure. Most items are created on demand — only `templates/` is created during bootstrap.

```
your-vault/
├── _directory-map.md       # Directory classification table (auto-maintained)
├── _index.md               # Vault index
├── _tags.md                # Tag index
├── _graph.md               # Relationship graph
├── CONVENTIONS.md          # Writing conventions
├── templates/              # Note templates (bootstrapped)
│   ├── note.md             # English
│   ├── note.zh-CN.md       # Chinese
│   ├── area.md
│   ├── area.zh-CN.md
│   ├── project.md
│   ├── project.zh-CN.md
│   ├── resource.md
│   ├── resource.zh-CN.md
│   ├── idea.md
│   ├── idea.zh-CN.md
│   ├── journal.md
│   └── journal.zh-CN.md
├── areas/                  # Long-term focus areas
├── projects/               # Goal-oriented projects
├── resources/              # References & learning notes
├── journal/                # Daily logs
└── ideas/                  # Idea drafts

Scripts are at `$SKILL_PATH/scripts/` (not inside the vault).
```

## Usage

```
/organize <content>                         — Classify and save text directly
/organize                                    — Organize current conversation into notes
/organize --title "My Title" <content>       — Specify a custom display title
/organize --name "CustomFileName" <content>  — Specify a custom filename
/organize --title "X" --name "Y" <content>   — Specify both title and filename
```

---

## 1. Validation: Pre-Flight Checks

Run these checks in order before anything else. Each failure must print a clear, actionable message.

### 1.1 VAULT_PATH is set

Read `$VAULT_PATH`. If unset or empty:
- Print: "VAULT_PATH is not set. Please configure it in Claude Code settings (~/.claude/settings.local.json) or export it in your shell profile (~/.bashrc / ~/.zshrc), then try again."
- Abort.

### 1.2 Vault directory exists

Run `test -d "$VAULT_PATH"`. If the directory does not exist:
- Ask the user if they want to create it with `mkdir -p "$VAULT_PATH"`.
- If yes, create it. If no, abort.

### 1.3 Vault directory is writable

Run `touch "$VAULT_PATH/.organize-write-test" && rm "$VAULT_PATH/.organize-write-test"`. If write fails:
- Print: "VAULT_PATH ($VAULT_PATH) is not writable. Please check directory permissions."
- Abort.

### 1.4 Resolve absolute path

Use `realpath "$VAULT_PATH"` to resolve symlinks or relative paths. Use the resolved path for all subsequent operations.

---

## 2. Bootstrap: Initialize Templates

Check if `$VAULT_PATH/templates/` exists. If it is missing or empty:
1. Create `$VAULT_PATH/templates/`
2. Write all 12 template files (6 English + 6 Chinese) using the standard template content shown below
3. Print: "Created templates/ with English and Chinese note templates."
4. Done.

**Do NOT create** `_directory-map.md`, `_index.md`, `_tags.md`, `_graph.md`, `CONVENTIONS.md`, or any PARA directories. All of those are created on demand during the core workflow.

### Standard Template Content

Each template uses `{{PLACEHOLDER}}` syntax. The templates directory should contain both language variants.

**English templates** (as listed in `templates/` directory of this skill repo):
- `note.md` — Minimal frontmatter, no section headings
- `area.md` — Sections: Current Focus, Key Questions, Recent Progress (table), Resources
- `project.md` — Sections: Goal, Progress (table), TODO, Notes
- `resource.md` — Sections: Key Points, Notes, Related
- `idea.md` — Sections: The Idea, Why, Next Steps
- `journal.md` — Sections: Records, Ideas, Tomorrow + prev/next navigation

**Chinese templates** (suffixed `.zh-CN.md`):
- `note.zh-CN.md` — Same frontmatter, no section headings
- `area.zh-CN.md` — Sections: 当前关注, 关键问题, 近期进展 (table), 资源
- `project.zh-CN.md` — Sections: 目标, 进度 (table), 待办, 笔记
- `resource.zh-CN.md` — Sections: 要点, 笔记, 相关
- `idea.zh-CN.md` — Sections: 想法, 为什么, 下一步
- `journal.zh-CN.md` — Sections: 记录, 想法, 明天计划 + prev/next navigation

### Template Selection Rule

When creating a note, pick the template based on user language and content language:

| Condition | Use template |
|-----------|-------------|
| Chinese template exists AND (user is using Chinese OR note content is Chinese) | `{type}.zh-CN.md` |
| All other cases | `{type}.md` |

Fallback: if the selected template file does not exist, try the other language variant. If neither exists, use a standard frontmatter-only template inline.

---

## 4. Built-in Tools

These Python scripts live at `$SKILL_PATH/scripts/` and provide reliable vault operations.
Always use these tools instead of ad-hoc `find`/`grep` commands unless the tool cannot handle your specific need.

### search

Search vault notes by keyword. Returns file paths with matching context lines.

```
python3 "$SKILL_PATH/scripts/search.py" "$VAULT_PATH" <keyword> [--limit N] [--type TYPE]

# --type: filter by note type (area/project/resource/idea/journal)
# --limit: max results (default 20)
```

### stats

Vault statistics: note counts by type, tag frequency, orphan count, broken links.

```
python3 "$SKILL_PATH/scripts/stats.py" "$VAULT_PATH"
```

### orphans

List orphan notes that have no incoming `[[]]` links from other notes.

```
python3 "$SKILL_PATH/scripts/orphans.py" "$VAULT_PATH"
```

### backlinks

Find all notes that link to a given note title.

```
python3 "$SKILL_PATH/scripts/backlinks.py" "$VAULT_PATH" <note_title>
# note_title: filename without .md extension
```

### Tool Usage Rules

1. **Prefer these tools** over ad-hoc shell commands for vault searching and analysis
2. **Parse the output** — tools return structured `key: value` or line-based formats
3. **Error handling**: if a tool exits with non-zero, read its stderr message and report to the user
4. **Missing script**: if `$SKILL_PATH` is not set or the script doesn't exist, fall back to manual commands and remind the user they may have an incomplete install

---

## 5. Core Workflow

### Step 1: Read Directory Map

Read `_directory-map.md` to get all directory classifications and keyword mappings.
If the file doesn't exist, scan the vault directory structure and create it.

### Step 2: Content Analysis — Find Best Directory

Score content against directories using **heuristic guidance** (not a precise algorithm):

Heuristics (cumulative):
- **Direct keyword match**: Content contains a keyword from a directory's Keywords column → strong signal
- **Type alignment**: Content nature matches the directory's type (area/project/resource/idea/journal)
- **Partial keyword match**: Content is topically related but uses different phrasing
- **Directory activity**: Recently updated directories get slight priority

Estimated weight guide:
- Direct match: +4
- Type alignment: +3
- Partial match: +2
- Directory activity: +1
- Maximum cumulative: 10

**IMPORTANT — Scoring Verification (Mandatory):**
After assigning scores, you MUST write out your reasoning explicitly:
1. "Keyword matches found: {list matched keywords from _directory-map.md}"
2. "Type alignment: {note type} ↔ {directory type} — YES/NO"
3. "Partial matches: {list partial topic overlaps}"
4. "Final scores: {directory A}: {score}, {directory B}: {score}"

If you cannot identify at least one keyword match or type alignment for the top-scoring directory, treat it as "no match" (score < 4).

### Step 3: Decision

| Condition (Guideline) | Action |
|-----------------------|--------|
| Strong match (score >= 7 guideline) | Auto-assign, inform user with reasoning |
| Moderate match (score 4-7 guideline) | Show top-2 candidates, let user choose |
| Weak/no match (score < 4 guideline) | Inform user, ask if new category needed |
| Tie | Priority: project > area > resource > idea > journal |

### Step 4: Create New Category (if needed)

When no matching directory:
1. Inform user no suitable directory exists
2. Analyze core topic, suggest 2-3 candidate directory names
3. Let user confirm or provide their own
4. Add new entry to `_directory-map.md`
5. Create physical directory and `_index.md`

### Step 5: Create Note

1. Read the template for the matched type — use the **Template Selection Rule** from Section 2 to pick English vs Chinese
2. Replace all `{{}}` placeholders with actual values
3. Extract title from content (or use `--title` argument)
4. Determine file name using the naming rules below
5. Write to the selected directory

#### File Naming Rules

Priority: `--name` parameter > auto-inferred from title

| Language | Convention | Examples |
|----------|-----------|----------|
| English (all ASCII characters) | PascalCase, no spaces | `ReactHooksGuide.md`, `DockerComposeNotes.md` |
| Chinese (contains non-ASCII) | Original Chinese text | `RPA与影刀自动化工具.md`, `深度学习笔记.md` |
| User-specified | `--name` value, PascalCase for ASCII | `/organize --name MyTitle ...` → `MyTitle.md` |
| Journal | Always date format | `2026-04-30.md` |
| Mixed EN/ZH | Follow the primary language | Use judgment |

Sanitization (apply after naming):
- Replace filename-prohibited characters (`/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`) with hyphens
- If filename would be empty after sanitization, use `untitled-{timestamp}.md`
- If filename already exists in target directory, append `{YYYYMMDDHHmmss}` timestamp

### Step 6: Update Indices & Linking

**Order matters** — linking may modify notes, so graph must be updated last.

#### 6.1 Update directory `_index.md`
- Add the new note as an entry in its directory's `_index.md`
- If `_index.md` does not exist, create it with frontmatter and a Markdown list

#### 6.2 Update `_tags.md`
- Add new tags from the note's frontmatter to `_tags.md`
- Group by tag, list notes under each tag
- If `_tags.md` does not exist, create it

#### 6.3 Bidirectional Linking

Purpose: If the new note mentions other notes or topics that exist in the vault, establish `[[]]` links in both directions.

Algorithm:
1. Extract up to 5 link keywords from the new note:
   a. Any `[[...]]` references already present in the note body
   b. Topics from the summary or body that may match existing note titles
   c. Tags from the note's frontmatter
2. For each keyword, use the **search** tool to find candidate notes:
   ```
   python3 "$SKILL_PATH/scripts/search.py" "$VAULT_PATH" "<keyword>"
   ```
3. Review the search results. For each returning a candidate:
   a. Verify relevance by reading the candidate note's title and first paragraph
   b. If relevant, add `[[CandidateNote]]` to the new note's `related:` field
   c. In the existing candidate note, append `[[NewNote]]` to its `related:` field (preserving existing entries)
   d. Update the existing note's `updated:` date
4. If no candidates found, leave `related: []`

#### 6.4 Update `_graph.md`

Format reference (every node follows this template):

```
## Node: {Note Title}
- **related**: [[RelatedNote1]], [[RelatedNote2]]
- **tags**: #tag1 #tag2
```

Rules:
- One `## Node:` heading per note that has `[[]]` links or a non-empty `related:` field
- The `**related**:` field lists all notes linked from this note
- The `**tags**:` field lists all tags from the note's frontmatter, space-separated with `#` prefix
- If a note has no related notes, use `**related**: []`
- Maintain bidirectional references: if Note A links to Note B, both nodes must exist
- Remove nodes for deleted notes

Procedure:
1. Read current `_graph.md` (or create if missing)
2. List all notes with `[[]]` links or non-empty `related:`
3. Create/update `## Node:` entries for each
4. Remove nodes for notes that no longer exist
5. Update `updated:` date in frontmatter

### Step 7: Git Operations (Optional)

Run pre-flight checks in order. Skip gracefully if any check fails.

```
# Check 1: Is git installed?
git --version 2>/dev/null || { echo "Git not found. Skipping."; exit 0; }

# Check 2: Is the vault a git repo?
git -C "$VAULT_PATH" rev-parse --is-inside-work-tree 2>/dev/null || { echo "Not a git repository. Skipping."; exit 0; }

# Check 3: Stage and commit
git -C "$VAULT_PATH" add "$VAULT_PATH/"
git -C "$VAULT_PATH" commit -m "organize: <note-title>"

# Check 4: Push if remote exists
git -C "$VAULT_PATH" remote -v | grep -q . && git -C "$VAULT_PATH" push || echo "No remote configured. Local commit kept."
```

Key rules:
- Always scope `git add` to `$VAULT_PATH/` (not `-A` which would stage parent repo changes in a monorepo)
- If git push fails (network/permission), keep the local commit and inform user: "Git push failed. Your commit is saved locally; push manually later."
- If any check fails, continue with the rest of the skill — git is optional

---

## Directory Types & Templates

| Prefix | Type | Template (EN) | Template (ZH) | Description |
|--------|------|---------------|---------------|-------------|
| areas/ | area | `templates/area.md` | `templates/area.zh-CN.md` | Long-term focus areas |
| projects/ | project | `templates/project.md` | `templates/project.zh-CN.md` | Goal-oriented projects |
| resources/ | resource | `templates/resource.md` | `templates/resource.zh-CN.md` | References & learning |
| journal/ | journal | `templates/journal.md` | `templates/journal.zh-CN.md` | Work logs |
| ideas/ | idea | `templates/idea.md` | `templates/idea.zh-CN.md` | Idea drafts |

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

## _graph.md Format Reference

When updating or creating `_graph.md`, follow this exact format:

```markdown
---
title: Graph
type: meta
updated: YYYY-MM-DD
---

# Knowledge Graph

## Node: {Note Title}
- **related**: [[RelatedNote1]], [[RelatedNote2]]
- **tags**: #tag1 #tag2
```

- One `## Node:` per note with `[[]]` links or `related:` entries
- `**related**:` lists bidirectional links (use `[]` if none)
- `**tags**:` space-separated tags with `#` prefix
- Both directions must exist in the graph (A→B and B→A)
- Remove nodes for deleted notes
- Update frontmatter `updated:` on each change

## Error Handling

| Error | Handling |
|-------|----------|
| Empty content | Prompt user for content |
| VAULT_PATH not set | Print configuration instructions, abort |
| VAULT_PATH does not exist | Ask user if they want to create it |
| VAULT_PATH not writable | Print permission instructions, abort |
| Directory doesn't exist | Run new-category workflow (Step 4) |
| Git not installed | Skip git, inform user |
| Not a git repository | Skip git, inform user |
| No remote configured | Commit locally, inform user |
| Git push fails | Keep local commit, inform user |
| Filename conflict | Append timestamp |
| Template missing | Use standard frontmatter template |
| Script not found ($SKILL_PATH/scripts/) | Fall back to manual commands, inform user of incomplete install |
| Python3 not installed | Fall back to manual commands, suggest installing Python |
