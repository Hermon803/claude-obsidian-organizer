---
title: Directory Map
type: meta
updated: 2026-04-01
---

# Directory Map

笔记分类对照表。本文件由 `/organize` skill 自动维护，根据内容关键词匹配合适的存储目录。

## Core Categories

| 目录 | 类型 | 用途 | 关键词 |
|------|------|------|--------|
| areas/ | area | 长期关注的领域（无截止日期） | 领域, focus, ongoing, 持续关注, roadmap |
| projects/ | project | 有明确目标的项目 | 项目, 计划, goal, milestone, deadline, 进度 |
| resources/ | resource | 参考资料、学习笔记 | 参考, 教程, guide, 学习, 笔记, 总结 |
| journal/ | journal | 工作日志、每日记录 | 日报, 日志, log, 工作总结, 今日, timesheet |
| ideas/ | idea | 灵感、想法草稿 | 想法, 灵感, brainstorm, maybe, 可能 |

## Tech Notes

| 目录 | 类型 | 用途 | 关键词 |
|------|------|------|--------|
| CodeNotebook/Frontend/ | resource | 前端技术笔记 | React, Vue, CSS, HTML, JavaScript, TypeScript, 前端, UI |
| CodeNotebook/Backend/ | resource | 后端技术笔记 | API, 后端, server, database, 数据库, REST, GraphQL |
| CodeNotebook/DevOps/ | resource | DevOps 相关笔记 | Docker, Kubernetes, CI/CD, deploy, 部署, 运维 |
| CodeNotebook/Python/ | resource | Python 编程笔记 | Python, pip, venv, Django, Flask, async |
| CodeNotebook/Git/ | resource | Git 版本控制 | git, commit, branch, merge, rebase, remote |

## Personal

| 目录 | 类型 | 用途 | 关键词 |
|------|------|------|--------|
| diary/ | journal | 个人日记、生活记录 | 日记, 生活, 个人, 心情, 日常 |
| readings/ | resource | 读书笔记 | 书, 阅读, 读书, 读后感, book, reading |
| fitness/ | area | 健身与健康 | 健身, 运动, 跑步, 健康, exercise, workout |

## 分类决策树

```
内容来了
├─ 包含代码或技术术语？
│  ├─ 前端相关 → CodeNotebook/Frontend/
│  ├─ 后端相关 → CodeNotebook/Backend/
│  ├─ DevOps 相关 → CodeNotebook/DevOps/
│  ├─ Python 相关 → CodeNotebook/Python/
│  ├─ Git 相关 → CodeNotebook/Git/
│  └─ 其他技术 → CodeNotebook/
├─ 个人生活/心情？
│  └─ diary/
├─ 读书/阅读？
│  └─ readings/
├─ 健身/健康？
│  └─ fitness/
├─ 工作日志/每日总结？
│  └─ journal/
├─ 灵感/想法？
│  └─ ideas/
├─ 学习笔记/教程总结？
│  └─ resources/
├─ 有明确目标/计划？
│  └─ projects/
├─ 长期关注？
│  └─ areas/
└─ 都不匹配？
   └─ 询问用户 → 创建新分类
```
