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
- Python 3.6+
- 一个 Obsidian 知识库（任意本地目录）
- Git（推荐但非必需）

## 安装

克隆仓库：

```bash
git clone https://github.com/Hermon803/claude-obsidian-organizer.git ~/.claude/skills/organize
```

### 设置环境变量

在全局 Claude Code 配置中设置 `VAULT_PATH` 和 `SKILL_PATH`：

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

### 准备知识库结构

技能在首次使用时自动创建模板，无需手动准备。

只需将 `VAULT_PATH` 指向任意目录（即使是空目录），即可开始整理。

所有索引文件（`_directory-map.md`、`_index.md`、`_tags.md`、`_graph.md`）和 PARA 目录（`areas/`、`projects/`、`resources/`、`journal/`、`ideas/`）都在整理内容时按需自动创建。

## 使用方法

在 Claude Code 中使用：

```
/organize <内容>                              — 直接分类保存文本
/organize                                      — 整理当前对话内容
/organize --title "我的标题" <内容>             — 指定自定义标题
/organize --name "FileName" <内容>              — 指定自定义文件名
/organize --title "X" --name "Y" <内容>         — 同时指定标题和文件名
```

### 分类评分机制

技能使用启发式方法（非精确算法）对内容评分，并在决策前显式验证关键词匹配：

| 参考 | 行为 |
|------|------|
| 强匹配（≈≥7） | 自动分类 |
| 中等匹配（≈4-6） | 显示 Top-2 候选 |
| 弱/无匹配（≈<4） | 询问是否创建新分类 |

## 文件结构

```
claude-obsidian-organizer/
├── SKILL.md               # Skill 定义（英文）
├── SKILL.zh-CN.md         # Skill 定义（中文）
├── README.md              # 本文档（英文）
├── README.zh-CN.md        # 本文档（中文）
├── CONVENTIONS.md         # 写作规范指南
├── scripts/               # Python 工具
│   ├── search.py          # 全文搜索
│   ├── stats.py           # Vault 统计
│   ├── orphans.py         # 孤岛笔记检测
│   └── backlinks.py       # 反向链接查询
├── templates/             # Obsidian 笔记模板
│   ├── note.md            # 通用笔记（英文）
│   ├── note.zh-CN.md      # 通用笔记（中文）
│   ├── area.md            # 长期关注的领域
│   ├── area.zh-CN.md      # 中文版
│   ├── project.md         # 有明确目标的项目
│   ├── project.zh-CN.md   # 中文版
│   ├── resource.md        # 参考资料
│   ├── resource.zh-CN.md  # 中文版
│   ├── idea.md            # 想法草稿
│   ├── idea.zh-CN.md      # 中文版
│   ├── journal.md         # 每日日志
│   └── journal.zh-CN.md   # 中文版
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
- **内置工具** — Python 脚本提供可靠的搜索、统计和链接分析

## 许可证

MIT
