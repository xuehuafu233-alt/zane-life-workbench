# 安装与更新

## 安装整套方法

在 Claude Code、Codex 等支持 Agent Skills 的工具中，可以让 Agent 从本仓库安装，也可以执行：

```bash
npx -y skills add xuehuafu233-alt/zane-life-workbench -g --all
```

`-g` 表示全局安装；安装到当前项目时省略 `-g`。按安装界面选择要使用的 Agent，完成后按宿主要求重载。

输入“请使用 zane-workbench，帮我处理这件事：……”开始。

## 更新

告诉 Agent：“比较本仓库与我已安装的版本，更新人生经营工作台。”保留自己修改过的方法，再按所用 Skill 管理器的更新流程操作。

需要指定版本时，先在 GitHub 的 Tags 中选择版本，让 Agent 安装对应标签的内容。切换前备份自己修改的文件。

## 手动安装

从仓库 `skills/` 目录取得各个 Skill 文件夹，按宿主说明放入它的 Skill 目录。每个文件夹以 `SKILL.md` 为入口，相关方法和模板随目录一起保留。

## 开始保存工作

告诉 Agent 想使用的工作台文件夹。它会读取已有导航，或从本次成果建立记录。Skill 安装目录存放方法，个人工作台文件夹存放自己的资料和进展。

[返回首页](../README.md)
