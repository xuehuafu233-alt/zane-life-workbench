# 安装、更新与回滚

## 推荐：让 Agent 从 GitHub 安装

在支持 Skills 的 Agent 中直接说：

```text
请从 https://github.com/xuehuafu233-alt/zane-life-workbench 安装 ZANE 人生经营工作台，安装全部五个 Skill。安装完成后告诉我怎样开始第一个问题。
```

支持 `skills` 命令的宿主可执行：

```bash
npx -y skills add xuehuafu233-alt/zane-life-workbench -g --all
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

## 直接使用

安装全部五个 Skill 后，直接对 Agent 说：

```text
使用 ZANE 人生经营工作台，先帮我处理眼前这个问题：……
```

通常不需要先选择具体组件。已经知道任务时，也可以直接说“调用 `zane-question-intent-translator`，帮我把这件事问清楚”。

## 更新

更新时再次执行安装命令，Skill 管理器会从 GitHub 获取当前版本。

## 使用说明

个人工作台资料由你选择位置保存。文件访问和执行能力由宿主决定；没有文件能力时，也可以先在聊天中获得当前帮助。

[返回首页](../README.md)
