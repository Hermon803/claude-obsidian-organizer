# Claude Obsidian Organizer

一个 **Claude Code 自定义斜杠命令**，能将对话内容智能分类到 Obsidian 知识库中。自动分析内容、匹配最佳目录、创建格式规范的笔记、更新索引并提交到 Git。

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Slash%20Command-8A2BE2)](https://claude.ai/code)
[![Obsidian](https://img.shields.io/badge/Obsidian-Knowledge%20Base-7C3AED)](https://obsidian.md)

## 功能特性

- **智能分类** — 基于 AI 的内容分析，结合关键词评分、类型匹配和上下文感知
- **模板化笔记** — 使用可自定义的 Obsidian 模板，生成规范的 YAML frontmatter 笔记
- **自动索引** — 每次操作后自动更新 `_index.md`、`_tags.md` 和 `_graph.md`
- **Git 集成** — 自动提交并推送变更到知识库的 Git 仓库
- **双向链接** — 搜索并建立笔记间的 `[[related]]` 关联
- **新分类支持** — 检测到内容不匹配现有目录时，帮助创建新分类

## 前置条件

- 已安装 [Claude Code](https://claude.ai/code)
- 一个 Obsidian 知识库（任意本地目录）
- 知识库已初始化 Git 仓库

## 安装

### 1. 安装 skill 文件

```bash
# 创建 skills 目录
mkdir -p ~/.claude/skills/organize

# 复制 skill 文件
cp SKILL.zh-CN.md ~/.claude/skills/organize/SKILL.md
```

### 2. 准备知识库结构

确保你的 Obsidian 知识库包含以下结构：

```
your-vault/
├── _directory-map.md       # 目录分类对照表
├── _index.md               # 知识库索引
├── _tags.md                # 标签索引
├── _graph.md               # 关系图谱
├── CONVENTIONS.md          # 写作规范
├── templates/              # 笔记模板（从本仓库复制）
├── areas/                  # 长期关注的领域
├── projects/               # 有明确目标的项目
├── resources/              # 参考资料和学习笔记
├── journal/                # 工作日志
└── ideas/                  # 想法草稿
```

### 3. 配置知识库路径

在知识库目录下的 Claude Code 项目配置中设置路径（`.claude/settings.local.json`）：

```json
{
  "env": {
    "VAULT_PATH": "/path/to/your/vault"
  }
}
```

或者直接在 `SKILL.md` 中将 `$VAULT_PATH` 替换为你的实际路径。

### 4. 设置模板

将本仓库的 `templates/` 目录复制到你的知识库中，按需自定义。

### 5. 初始化索引

参考本仓库 `examples/` 中的示例，创建初始的 `_directory-map.md`，然后开始使用！

## 使用方法

在 Claude Code 中使用：

```
/organize <内容>                       — 直接分类保存文本
/organize                               — 整理当前对话内容
/organize --title "我的标题" <内容>     — 指定自定义标题
```

### 分类评分机制

技能会根据你的目录对内容进行评分：

| 分数 | 行为 |
|------|------|
| ≥ 7  | 自动分类 |
| 4–6  | 显示 Top-2 候选目录，供你选择 |
| < 4  | 询问是否需要创建新分类 |

## 文件结构

```
claude-obsidian-organizer/
├── SKILL.md               # 核心斜杠命令文件（英文）
├── SKILL.zh-CN.md         # 核心斜杠命令文件（中文）
├── README.md              # 本文档（英文）
├── README.zh-CN.md        # 本文档（中文）
├── CONVENTIONS.md         # 写作规范指南
├── templates/             # Obsidian 笔记模板
│   ├── note.md            # 通用笔记
│   ├── area.md            # 长期关注的领域
│   ├── project.md         # 有明确目标的项目
│   ├── resource.md        # 参考资料
│   ├── idea.md            # 想法草稿
│   └── journal.md         # 每日日志
└── examples/              # 示例知识库文件
    ├── _directory-map.md  # 分类映射（示例）
    ├── _index.md          # 知识库索引（示例）
    ├── _tags.md           # 标签索引（示例）
    └── _graph.md          # 关系图谱（示例）
```

## 使用场景示例

### 场景 1：学习新技术

```
你：我刚看完一个 React 教程，想保存笔记。
Claude: /organize 我刚看完 React hooks 教程。要点：useState 管理本地状态、useEffect 处理副作用、useContext 实现依赖注入...
```

技能会自动识别为 `resource` 类型，匹配到 `resources/` 或 `CodeNotebook/React/`，创建格式化笔记并更新所有索引。

### 场景 2：规划项目

```
你：/organize 我计划用 Astro 搭一个个人网站。目标：作品集 + 博客，月底前完成。
```

自动识别为 `project` 类型，归档到 `projects/`，frontmatter 中包含目标和截止日期。

## 自定义

- **模板**：编辑 `templates/*.md` 文件以匹配你的笔记风格
- **目录映射**：编辑 `_directory-map.md` 添加与你内容领域匹配的关键词
- **评分规则**：如需调整敏感度，可修改 `SKILL.md` 中的评分逻辑

## 为什么用这个方案

不同于需要运行 Obsidian 的插件，本技能通过 Claude Code 在文件系统层面工作：

- **无需插件** — 即使不打开 Obsidian，也能与任何知识库配合使用
- **AI 驱动分类** — 超越简单的关键词匹配，理解内容的上下文
- **版本控制** — Git 集成确保每条笔记都有备份
- **纯提示驱动** — 除 Claude Code 自身外，无外部二进制依赖

## 许可证

MIT
