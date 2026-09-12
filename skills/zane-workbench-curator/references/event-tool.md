# 本地事项工具

仅用于本包新建的独立工作台。职场版初始化使用 `--mode career`，组织经营版使用 `--mode work`，人生版使用 `--mode life`；事项格式相同。Python 3.9+，无第三方依赖、无网络。脚本相对整理器 Skill 目录。

```bash
python3 scripts/workbench.py init --root <新目录> --mode work
python3 scripts/workbench.py add --root <工作台> --file <事项JSON>
python3 scripts/workbench.py update --root <工作台> --id CASE-001 --expect-revision 1 --patch <更新JSON> --reason '本人补充实际反馈'
python3 scripts/workbench.py show --root <工作台> --id CASE-001
python3 scripts/workbench.py render --root <工作台>
python3 scripts/workbench.py check --root <工作台>
```

事项字段：

```json
{
  "id": "CASE-001",
  "revision": 1,
  "title": "自行填写当前事项",
  "goal": "希望发生的变化",
  "domain": "使用者自行命名",
  "status": "active",
  "phase": "ready",
  "outcome": "unknown",
  "decision": "当前判断及必要依据",
  "next_action": "已选择的下一步或当前交付",
  "baseline": "原来怎样做；未测量则如实注明",
  "expected_change": "想观察到什么",
  "cost": "已确定投入或实际成本；未知不写零",
  "review_on": null,
  "evidence": [
    {"kind": "input", "text": "本人提供的事实摘要", "source": "资料/当前背景.md", "at": "2026-01-01"}
  ],
  "history": []
}
```

上方是格式示意，日期与内容必须改成当前任务事实；工具不把示例当真实事项。source 指向本工作台内已有的最小来源文件；不允许引用工作台外的私人文件或软链。工具核验来源存在，不核验内容的真实性。无需复制完整原件，可以先保存用户已授权的必要摘要。

- status：`active` / `waiting` / `completed` / `stopped`。
- phase：`judged` / `ready` / `acted` / `feedback`，分别对应判断、方案、动作和反馈。
- outcome：`unknown` / `partial` / `met` / `not_met`。完成交付与目标实现分别记录。
- evidence.kind：`input` / `action` / `feedback` / `correction`。

update 使用局部 JSON 字段替换，evidence 更新时必须带上完整的旧证据并在末尾追加。revision 与 history 由工具维护；当前判断、下一步和结果要与反馈一起更新。新增动作或反馈阶段需要相应的新证据，已有证据不能静默改写。

completed/stopped 仍可追加新证据并改当前判断，但不能直接重开；新行动另建事项并在证据中引用前序文件。终态必须清空 next_action 和 review_on。到期只提示核实，不自动修改状态。工具不会自动将用户所说的“完成了”解释为长期目标已实现。

更新前保存旧版本到本工作台的 `.history/`；视图失败时原事件仍是真源，可重跑 render。不要手改 `现在做什么.md`。视图只显示 ID、生命域、状态与阶段，不显示事项标题、原文、下一步或金额；详细内容按需 show。安全备份也属于私人材料，不能随 Skill 分享。

## 日期与用户入口

证据 at 是该来源登记日期；事件发生日已知时在 text 或来源正文另写，只有“周一”“明天”而无法确定具体日期时保留原说法，不推造日历日期。review_on 未确定就为 null。

默认概览为保护敏感内容只显示 ID 和状态，用户日常从项目／生活事项入口或接续卡进入，链接回唯一事项源，不再维护第二套状态。脚本可来自已安装整理器，迁移电脑时需重新安装对应套装；脚本绝对路径不是可移植身份，恢复时重新定位当前安装位置。
