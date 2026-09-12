# 安装、更新与回滚

## 推荐：让 Agent 从 GitHub 安装

在支持 Skills 的 Agent 中直接说：

```text
请从 https://github.com/xuehuafu233-alt/zane-dialogue-skills 安装 ZANE 人生经营工作台，安装全部五个 Skill。安装完成后告诉我怎样开始第一个问题。
```

支持 `skills` 命令的宿主可执行：

```bash
npx -y skills add xuehuafu233-alt/zane-dialogue-skills -g --all
```

安装后重载 Agent（如果宿主需要），输入：

```text
使用 ZANE 人生经营工作台，先帮我处理眼前这个问题：……
```

安装器或 Skill 管理器应从仓库的 `skills/` 目录读取五个组件，并保留组件依赖。若宿主显示安装范围或权限提示，按你的实际使用范围选择；本仓库不要求上传个人资料。

## 五个组件

| Skill | 作用 | 什么时候直接调用 |
|---|---|---|
| `zane-workbench` | 人生总控 | 日常从一个真实问题开始 |
| `zane-workbench-curator` | 搭建与维护 | 需要保存、接续或适配资料时 |
| `zane-question-intent-translator` | 问题意图转译 | 说不清进展或多个意图混在一起时 |
| `zane-agent-identity-card-builder` | AI 伙伴设定 | 想定义长期伙伴的工作方式时 |
| `zane-self-insight` | 自我认识 | 想理解价值、动机和反复选择时 |

已经知道任务时，也可以直接告诉 Agent：“调用 `zane-question-intent-translator`，帮我把这件事问清楚”，或“调用 `zane-self-insight`，一起看看我为什么反复犹豫”。通常不需要先选择，人生总控会按问题判断是否联动其他组件。

## 需要上传 ZIP 的宿主

不能从 GitHub 安装、但支持上传自定义 Skill 的宿主，才使用[组件清单](skill-inventory.md)中的五个 ZIP。下载包是兼容入口，不是推荐的首次安装路径。

## 本地文件安装与升级

需要本地文件和 Python 的宿主，可以下载完整包后运行：

```bash
python3 install.py --skills-dir "<宿主实际Skill目录>"
```

升级前先让 Agent 比较已有安装。由本安装器管理且没有本地修改的旧版可用 `--upgrade`；未知来源或被修改的目录会停止并保留原文件。更新包时从 GitHub 重新安装也可以由宿主的 Skill 管理器完成。

## 回滚与能力边界

本地安装器会输出检查点，可用新版安装器的 `--rollback` 恢复；网页上传和宿主内置安装器由宿主负责回滚。个人工作台资料始终与 Skill 安装位置分开。

纯聊天可以体验方法，但不能据此承诺自动保存或跨会话记忆。模型、文件访问和执行能力由宿主决定；本仓库不提供后台服务。

[返回首页](../README.md)
