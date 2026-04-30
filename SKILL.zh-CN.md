---
name: organize
version: 1.0.0
description: |
  将对话内容整理到 Obsidian 笔记仓库 — 自动分类、智能归档、更新索引、Git 推送。
  当用户说"整理"、"归类"、"保存到仓库"、"归档笔记"、"分类保存"时触发。
Triggers: organize, 整理, 归类, 保存笔记, 存到仓库, 归档, 分类保存, 整理当前对话, save to vault, organize notes, categorize
---

# /organize — 笔记整理助手

将对话内容或指定文本整理到 Obsidian 知识库。自动分析内容、匹配最佳目录、创建规范笔记、更新索引、提交 Git。

> 这是一个 **Claude Code 自定义斜杠命令**。安装到你的项目 `.claude/skills/organize/SKILL.md` 即可使用。

## 前置条件

- 已安装 [Claude Code](https://claude.ai/code)
- 一个 Obsidian 知识库（任意本地目录）
- 知识库已初始化 Git 仓库

## 安装步骤

1. 创建 skills 目录：

   ```bash
   mkdir -p ~/.claude/skills/organize
   ```

2. 将此文件复制到 `~/.claude/skills/organize/SKILL.md`

3. 将文件中的 `$VAULT_PATH` 替换为你的 Obsidian 知识库绝对路径

## 知识库结构要求

`/organize` 期望你的知识库有以下结构：

```
your-vault/
├── _directory-map.md       # 目录分类对照表（本 skill 自动维护）
├── _index.md               # 知识库索引
├── _tags.md                # 标签索引
├── _graph.md               # 关系图谱
├── CONVENTIONS.md          # 写作规范
├── templates/              # 笔记模板
│   ├── note.md
│   ├── area.md
│   ├── project.md
│   ├── resource.md
│   ├── idea.md
│   └── journal.md
├── areas/                  # 长期关注的领域
├── projects/               # 有明确目标的项目
├── resources/              # 参考资料和学习笔记
├── journal/                # 工作日志
└── ideas/                  # 想法草稿
```

## 调用方式

```
/organize <内容>            — 直接传入文本进行分类保存
/organize                    — 将当前对话上下文整理为笔记
/organize --title "xxx" <内容>  — 指定自定义标题
```

## 核心工作流程

### 第一步：读取目录映射

先读取 `_directory-map.md`，获取所有目录的分类定义和关键词映射表。
如果文件不存在，先扫描仓库目录结构并创建它。

### 第二步：内容分析 — 确定最佳目录

用以下评分逻辑找出最合适的目录：

1. **关键词匹配**: 将内容中的关键词与 `_directory-map.md` 中每个目录的 Keywords 做匹配
2. **语义判断**: 根据内容性质判定笔记类型（area/project/resource/idea/journal）
3. **上下文线索**: 如果内容来自对话，注意用户描述的场景（"我在学…" → resource, "我计划…" → project）

评分规则（总分 10）：
- **精准命中**（关键词直接匹配）+4 分
- **类型匹配**（内容性质与目录 type 一致）+3 分
- **部分匹配**（关键词部分相关）+2 分
- **目录活跃度**（最近有更新的目录优先）+1 分

### 第三步：决策

| 情况 | 操作 |
|------|------|
| 最高分 ≥ 7 | 直接使用该目录，告知用户 |
| 4 ≤ 最高分 < 7 | 列出 Top-2 候选，让用户选择 |
| 最高分 < 4 | 告知用户无合适目录，询问是否创建新分类 |
| 多个目录同分 | 优先级：project > area > resource > idea > journal |

### 第四步：创建新分类（如需要）

当无匹配目录时：
1. 告知用户无合适目录
2. 分析内容的核心主题，建议 2-3 个候选目录名
3. 让用户确认或自行输入
4. 确认后在 `_directory-map.md` 中添加新条目
5. 创建对应的物理目录和 `_index.md`

### 第五步：创建笔记

按照 `CONVENTIONS.md` 和模板创建笔记：

1. 读取对应类型的模板（`templates/{type}.md`）
2. 替换所有 `{{}}` 占位符为实际值
3. 标题从内容提取（或使用 `--title` 参数）
4. 文件名：小写连字符（英文）或原文（中文），无空格
5. 写入到选定目录

### 第六步：更新索引

1. 更新目录的 `_index.md`（添加文件条目）
2. 更新 `_tags.md`（添加新标签）
3. 更新 `_graph.md`（如果有关联笔记）
4. 搜索相关笔记并建立双向链接

### 第七步：Git 提交与推送

```bash
cd $VAULT_PATH
git add -A
git commit -m "整理笔记：<标题>"
git push
```

如果 git push 失败（网络/权限），保留本地提交，告知用户稍后手动推送。

## 目录类型与模板对应

| 目录前缀 | 类型 (type) | 模板 | 说明 |
|---------|------------|------|------|
| areas/ | area | `templates/area.md` | 长期关注的领域 |
| projects/ | project | `templates/project.md` | 有明确目标的项目 |
| resources/ | resource | `templates/resource.md` | 参考资料、学习笔记 |
| journal/ | journal | `templates/journal.md` | 工作日志 |
| ideas/ | idea | `templates/idea.md` | 想法草稿 |

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

1. **日记/日志类**: 如果内容明显是日记（个人生活记录），用 `diary/`；如果是工作总结，用 `journal/`
2. **代码片段**: 包含代码块的内容优先放入 `CodeNotebook/` 下的子目录
3. **多主题混合**: 提取主要内容确定主分类，在 `related` 中链接次要主题
4. **内容过短 (< 50 字)**: 建议用 `ideas/` 或 capture 而非 create note
5. **已有类似笔记**: 搜索仓库，询问是否追加到现有笔记而非新建

## 目录映射维护

每次 `/organize` 完成后，检查 `_directory-map.md` 是否需要更新：
- 新建了目录？添加新条目
- 某个目录累积了较多笔记？更新其描述和关键词
- 某目录长期为空？询问用户是否保留

## 错误处理

| 错误 | 处理方式 |
|------|---------|
| 内容为空 | 提示用户提供内容 |
| 目录不存在 | 按新建分类流程处理 |
| Git push 失败 | 保留本地提交，告知用户 |
| 文件名冲突 | 添加时间戳后缀 |
| 模板不存在 | 使用标准 frontmatter 模板 |
