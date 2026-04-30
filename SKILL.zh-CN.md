---
name: organize
version: 1.1.0
description: |
  将对话内容整理到 Obsidian 笔记仓库 — 自动分类、智能归档、更新索引、Git 推送。
  当用户说"整理"、"归类"、"保存到仓库"、"归档笔记"、"分类保存"时触发。
Triggers: organize, 整理, 归类, 保存笔记, 存到仓库, 归档, 分类保存, 整理当前对话, save to vault, organize notes, categorize
---

# /organize — 笔记整理助手

将对话内容或指定文本整理到 Obsidian 知识库。自动分析内容、匹配最佳目录、创建规范笔记、更新索引、提交 Git。

## 前置条件

- 已安装 [Claude Code](https://claude.ai/code)
- Python 3.6+
- 一个 Obsidian 知识库（任意本地目录），需设置 `$VAULT_PATH` 指向其绝对路径
- 知识库已初始化 Git 仓库 — **推荐但非必需**；无 Git 也可正常使用

## 安装

克隆仓库：

```bash
git clone https://github.com/Hermon803/claude-obsidian-organizer.git ~/.claude/skills/organize
```

### 设置环境变量

在全局 Claude Code 配置中设置：

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

或者添加到 shell 配置文件（`~/.bashrc` / `~/.zshrc`）：

```bash
export VAULT_PATH="/path/to/your/vault"
export SKILL_PATH="$HOME/.claude/skills/organize"
```

## 知识库结构

`/organize` 适配以下结构。大部分文件按需创建——bootstrap 只创建 `templates/`。

```
your-vault/
├── _directory-map.md       # 目录分类对照表（自动维护）
├── _index.md               # 知识库索引
├── _tags.md                # 标签索引
├── _graph.md               # 关系图谱
├── CONVENTIONS.md          # 写作规范
├── templates/              # 笔记模板（bootstrap 自动创建）
│   ├── note.md             # 英文
│   ├── note.zh-CN.md       # 中文
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
├── areas/                  # 长期关注的领域
├── projects/               # 有明确目标的项目
├── resources/              # 参考资料和学习笔记
├── journal/                # 工作日志
└── ideas/                  # 想法草稿

脚本位于 `$SKILL_PATH/scripts/`（不在 vault 内）。
```

## 调用方式

```
/organize <内容>                          — 直接传入文本进行分类保存
/organize                                  — 将当前对话上下文整理为笔记
/organize --title "我的标题" <内容>         — 指定自定义标题
/organize --name "CustomFileName" <内容>   — 指定自定义文件名
/organize --title "X" --name "Y" <内容>    — 同时指定标题和文件名
```

---

## 1. 前置校验：启动检查

按顺序执行以下检查。任一失败须给出清晰的指引消息。

### 1.1 VAULT_PATH 是否已设置

读取 `$VAULT_PATH`。若未设置或为空：
- 提示："VAULT_PATH 未设置。请在 Claude Code 配置 (~/.claude/settings.local.json) 中配置，或在 shell 配置文件 (~/.bashrc / ~/.zshrc) 中导出，然后重试。"
- 终止。

### 1.2 Vault 目录是否存在

执行 `test -d "$VAULT_PATH"`。若不存在：
- 询问用户是否用 `mkdir -p "$VAULT_PATH"` 创建
- 是则创建，否则终止

### 1.3 Vault 目录是否可写

执行 `touch "$VAULT_PATH/.organize-write-test" && rm "$VAULT_PATH/.organize-write-test"`。若写入失败：
- 提示："VAULT_PATH ($VAULT_PATH) 不可写，请检查目录权限。"
- 终止。

### 1.4 解析绝对路径

用 `realpath "$VAULT_PATH"` 解析符号链接或相对路径。后续操作始终使用解析后的绝对路径。

---

## 2. 初始化：创建模板

检查 `$VAULT_PATH/templates/` 是否存在。若缺失或为空：
1. 创建 `$VAULT_PATH/templates/`
2. 写入全部 12 个模板文件（6 英文 + 6 中文），内容参考本 skill 仓库的 templates/ 目录
3. 提示："已创建 templates/ 目录，包含英文和中文笔记模板。"
4. 完成。

**不要创建** `_directory-map.md`、`_index.md`、`_tags.md`、`_graph.md`、`CONVENTIONS.md` 或任何 PARA 目录。这些全部在核心流程中按需生成。

### 标准模板内容

每个模板使用 `{{PLACEHOLDER}}` 语法。模板目录应包含两种语言版本。

**英文模板**（无后缀，如 `area.md`）：
- `note.md` — 最小 frontmatter，无章节标题
- `area.md` — 章节：Current Focus, Key Questions, Recent Progress（表格）, Resources
- `project.md` — 章节：Goal, Progress（表格）, TODO, Notes
- `resource.md` — 章节：Key Points, Notes, Related
- `idea.md` — 章节：The Idea, Why, Next Steps
- `journal.md` — 章节：Records, Ideas, Tomorrow + 前后日导航

**中文模板**（后缀 `.zh-CN.md`）：
- `note.zh-CN.md` — 同英文 frontmatter，无章节标题
- `area.zh-CN.md` — 章节：当前关注, 关键问题, 近期进展（表格）, 资源
- `project.zh-CN.md` — 章节：目标, 进度（表格）, 待办, 笔记
- `resource.zh-CN.md` — 章节：要点, 笔记, 相关
- `idea.zh-CN.md` — 章节：想法, 为什么, 下一步
- `journal.zh-CN.md` — 章节：记录, 想法, 明天计划 + 前后日导航

### 模板选择规则

创建笔记时，根据用户语言和内容语言选择模板：

| 条件 | 使用模板 |
|------|---------|
| 中文模板存在 且（用户使用中文 或 笔记内容为中文） | `{类型}.zh-CN.md` |
| 其他情况 | `{类型}.md` |

降级：若选中模板不存在，尝试另一种语言版本。若两者皆无，用标准 frontmatter 内联兜底。

---

## 4. 内置工具

Python 脚本位于 `$SKILL_PATH/scripts/`，提供可靠的 vault 操作。
优先使用这些工具而非临时的 `find`/`grep` 命令（除非工具无法满足需求）。

### search（搜索）

按关键词搜索笔记，返回文件路径和匹配行。

```
python3 "$SKILL_PATH/scripts/search.py" "$VAULT_PATH" <关键词> [--limit N] [--type TYPE]

# --type: 按笔记类型过滤 (area/project/resource/idea/journal)
# --limit: 最大结果数（默认 20）
```

### stats（统计）

vault 统计：各类型笔记数、标签数、孤岛笔记数、坏链接数。

```
python3 "$SKILL_PATH/scripts/stats.py" "$VAULT_PATH"
```

### orphans（孤岛检测）

列出没有其他笔记通过 `[[]]` 链接引用的孤岛笔记。

```
python3 "$SKILL_PATH/scripts/orphans.py" "$VAULT_PATH"
```

### backlinks（反向链接）

查找所有链接到指定笔记标题的笔记。

```
python3 "$SKILL_PATH/scripts/backlinks.py" "$VAULT_PATH" <笔记标题>
# 笔记标题：不带 .md 后缀的文件名
```

### 工具使用规则

1. **优先使用这些工具**而非临时 shell 命令
2. **解析输出格式**——工具返回 `key: value` 或基于行的结构化输出
3. **错误处理**：若工具退出码非零，读取 stderr 信息并报告用户
4. **脚本缺失**：若 `$SKILL_PATH` 未设置或脚本不存在，回退到手动命令并提示用户安装不完整

---

## 5. 核心工作流程

### 第一步：读取目录映射

读取 `_directory-map.md`，获取所有目录的分类定义和关键词映射表。
如果文件不存在，先扫描仓库目录结构并创建它。

### 第二步：内容分析 — 确定最佳目录

用以下**启发式方法**（非精确算法）找出最合适的目录：

启发式信号：
- **关键词命中**: 内容中包含某个目录 Keywords 列中的关键词 → 强信号
- **类型对齐**: 内容性质与目录类型（area/project/resource/idea/journal）匹配
- **部分匹配**: 内容主题相关但措辞不同
- **目录活跃度**: 最近有更新的目录优先

预估权重（参考）：
- 精准命中：+4
- 类型对齐：+3
- 部分匹配：+2
- 目录活跃度：+1
- 总分上限：10

**重要 — 评分验证（必做）：**
评分后必须写出验证过程：
1. "匹配到的关键词：{列出 _directory-map.md 中命中的关键词}"
2. "类型对齐：{笔记类型} ↔ {目录类型} — 是/否"
3. "局部匹配：{列出相关主题}"
4. "最终分数：{目录A}: {分数}, {目录B}: {分数}"

若无法为最高分目录找到至少一个关键词匹配或类型对齐，视为"无匹配"（分数 < 4）。

### 第三步：决策

| 情况（参考） | 操作 |
|------------|------|
| 强匹配（参考 >= 7） | 直接使用该目录，告知用户并给出理由 |
| 中等匹配（参考 4-7） | 列出 Top-2 候选，让用户选择 |
| 弱/无匹配（参考 < 4） | 告知用户无合适目录，询问是否创建新分类 |
| 多目录同分 | 优先级：project > area > resource > idea > journal |

### 第四步：创建新分类（如需要）

当无匹配目录时：
1. 告知用户无合适目录
2. 分析内容的核心主题，建议 2-3 个候选目录名
3. 让用户确认或自行输入
4. 确认后在 `_directory-map.md` 中添加新条目
5. 创建对应的物理目录和 `_index.md`

### 第五步：创建笔记

1. 读取对应类型的模板——按**模板选择规则**选择英文或中文版本
2. 替换所有 `{{}}` 占位符为实际值
3. 标题从内容提取（或使用 `--title` 参数）
4. 按以下命名规则确定文件名
5. 写入到选定目录

#### 文件命名规则

优先级：`--name` 参数 > 从标题自动推断

| 语言 | 风格 | 示例 |
|------|------|------|
| 英文（纯 ASCII 字符） | PascalCase，无空格 | `ReactHooksGuide.md`、`DockerComposeNotes.md` |
| 中文（含非 ASCII 字符） | 中文原文 | `RPA与影刀自动化工具.md`、`深度学习笔记.md` |
| 用户指定 | `--name` 值，英文自动 PascalCase | `/organize --name MyTitle ...` → `MyTitle.md` |
| 日记 | 固定日期格式 | `2026-04-30.md` |
| 中英混合 | 以主体语言为准 | 自行判断 |

净化规则（命名后执行）：
- 替换文件名非法字符（`/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`）为连字符
- 若净化后文件名为空，用 `untitled-{时间戳}.md`
- 若目标目录中文件名已存在，追加 `{YYYYMMDDHHmmss}` 时间戳

### 第六步：更新索引与链接

**顺序重要**——链接可能修改已有笔记，图谱必须最后更新。

#### 6.1 更新目录 `_index.md`
- 将新笔记添加到其目录的 `_index.md` 中
- 若 `_index.md` 不存在，创建它

#### 6.2 更新 `_tags.md`
- 将笔记 frontmatter 中的新标签添加到 `_tags.md`
- 按标签分组，标签下列出笔记
- 若 `_tags.md` 不存在，创建它

#### 6.3 双向链接

目的：如果新笔记提到了仓库中已有的其他笔记或主题，建立双向 `[[]]` 链接。

算法：
1. 从新笔记中提取最多 5 个链接关键词：
   a. 新笔记正文中已有的 `[[...]]` 引用
   b. 摘要或正文中可能匹配已有笔记标题的主题
   c. 笔记 frontmatter 中的标签
2. 对每个关键词，用 **search** 工具查找候选笔记：
   ```
   python3 "$SKILL_PATH/scripts/search.py" "$VAULT_PATH" "<关键词>"
   ```
3. 检查搜索结果。对每个有返回的候选：
   a. 阅读候选笔记的标题和首段，确认相关性
   b. 若相关，将 `[[候选笔记]]` 添加到新笔记的 `related:` 字段
   c. 在候选笔记中追加 `[[新笔记]]` 到其 `related:` 字段（保留现有条目）
   d. 更新候选笔记的 `updated:` 日期
4. 若未找到候选，保留 `related: []`

#### 6.4 更新 `_graph.md`

格式参考（每个节点遵循以下模板）：

```
## Node: {笔记标题}
- **related**: [[相关笔记1]], [[相关笔记2]]
- **tags**: #标签1 #标签2
```

规则：
- 每条有 `[[]]` 链接或非空 `related:` 的笔记对应一个 `## Node:` 标题
- `**related**:` 列出该笔记的所有双向链接（无链接填 `[]`）
- `**tags**:` 标签以 `#` 前缀、空格分隔
- 双向关系必须在图谱中都存在（A→B 和 B→A）
- 移除已删除笔记的节点
- 每次变更后更新 frontmatter 的 `updated:` 日期

步骤：
1. 读取当前 `_graph.md`（不存在则创建）
2. 列出所有包含 `[[]]` 或非空 `related:` 的笔记
3. 为每条笔记创建/更新 `## Node:` 条目
4. 移除已删除笔记的节点
5. 更新 frontmatter 中的 `updated:` 日期

### 第七步：Git 操作（可选）

按顺序执行预检。任一检查失败则优雅跳过。

```
# 检查 1：是否安装了 git？
git --version 2>/dev/null || { echo "未找到 git，跳过。"; exit 0; }

# 检查 2：vault 是否为 git 仓库？
git -C "$VAULT_PATH" rev-parse --is-inside-work-tree 2>/dev/null || { echo "非 git 仓库，跳过。"; exit 0; }

# 检查 3：暂存并提交
git -C "$VAULT_PATH" add "$VAULT_PATH/"
git -C "$VAULT_PATH" commit -m "整理笔记：<笔记标题>"

# 检查 4：有 remote 则推送
git -C "$VAULT_PATH" remote -v | grep -q . && git -C "$VAULT_PATH" push || echo "无远程仓库，本地提交已保留。"
```

关键规则：
- `git add` 始终限制在 `$VAULT_PATH/` 范围内（不用 `-A`，避免在 monorepo 中暂存父仓库的变更）
- 若 push 失败（网络/权限），保留本地提交并告知用户："Git 推送失败。提交已保存到本地，稍后手动推送。"
- 任一检查失败不影响后续操作——Git 是可选的

---

## 目录类型与模板对应

| 目录前缀 | 类型 | 英文模板 | 中文模板 | 说明 |
|---------|------|---------|---------|------|
| areas/ | area | `templates/area.md` | `templates/area.zh-CN.md` | 长期关注的领域 |
| projects/ | project | `templates/project.md` | `templates/project.zh-CN.md` | 有明确目标的项目 |
| resources/ | resource | `templates/resource.md` | `templates/resource.zh-CN.md` | 参考资料、学习笔记 |
| journal/ | journal | `templates/journal.md` | `templates/journal.zh-CN.md` | 工作日志 |
| ideas/ | idea | `templates/idea.md` | `templates/idea.zh-CN.md` | 想法草稿 |

## 内容-目录快速参考

| 内容特征 | 推荐目录 | 理由 |
|---------|---------|------|
| 编程技术、框架、语言特性 | `CodeNotebook/<子类>/` | 技术笔记专属 |
| AI/ML/深度学习 | `CodeNotebook/AI/` | 关键词匹配率最高 |
| 日常学习记录 | `resources/` | 参考资料 |
| 个人想法、灵感 | `ideas/` | 未成熟的想法 |
| 工作计划、进展 | `projects/` | 有目标的项目 |
| 长期关注领域 | `areas/` | 无截止日期的持续关注 |
| 每日记录、工作总结 | `journal/` | 时间线日志 |
| 考试备考 | `exam-notes/` | 备考专属 |
| 个人日记 | `diary/` | 私人记录 |

## 特殊处理规则

1. **日记/日志类**: 个人生活记录 → `diary/`；工作总结 → `journal/`
2. **代码片段**: 包含代码块的内容优先放入 `CodeNotebook/` 下子目录
3. **多主题混合**: 提取主要内容确定主分类，在 `related` 中链接次要主题
4. **内容过短（< 50 字）**: 建议用 `ideas/` 或 capture 而非 create note
5. **已有类似笔记**: 搜索仓库，询问是否追加到现有笔记而非新建

## 目录映射维护

每次 `/organize` 完成后，检查 `_directory-map.md`：
- 新建了目录？添加新条目
- 某个目录累积了较多笔记？更新其描述和关键词
- 某目录长期为空？询问用户是否保留

## _graph.md 格式参考

更新或创建 `_graph.md` 时使用以下格式：

```markdown
---
title: Graph
type: meta
updated: YYYY-MM-DD
---

# Knowledge Graph

## Node: {笔记标题}
- **related**: [[相关笔记1]], [[相关笔记2]]
- **tags**: #标签1 #标签2
```

- 每条有 `[[]]` 链接或 `related:` 的笔记对应一个 `## Node:`
- `**related**:` 列出所有双向链接（无链接填 `[]`）
- `**tags**:` 以 `#` 前缀、空格分隔
- 双向关系必须都在图谱中存在
- 移除已删除笔记的节点
- 更新 frontmatter `updated:` 日期

## 错误处理

| 错误 | 处理方式 |
|------|---------|
| 内容为空 | 提示用户提供内容 |
| VAULT_PATH 未设置 | 打印配置指引，终止 |
| VAULT_PATH 目录不存在 | 询问用户是否创建 |
| VAULT_PATH 不可写 | 打印权限指引，终止 |
| 目录不存在 | 按新建分类流程处理 |
| Git 未安装 | 跳过 git，告知用户 |
| 非 git 仓库 | 跳过 git，告知用户 |
| 无远程仓库 | 本地提交，告知用户 |
| Git push 失败 | 保留本地提交，告知用户 |
| 文件名冲突 | 追加时间戳 |
| 模板不存在 | 使用标准 frontmatter 模板 |
| 脚本未找到（$SKILL_PATH/scripts/） | 回退到手动命令，提示用户安装不完整 |
| Python3 未安装 | 回退到手动命令，建议安装 Python |
