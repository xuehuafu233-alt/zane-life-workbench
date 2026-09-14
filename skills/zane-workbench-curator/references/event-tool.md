# 本地事项工具

仅用于本包新建的独立工作台。职场版初始化使用 `--mode career`，组织经营版使用 `--mode work`，人生版使用 `--mode life`；事项格式相同。Python 3.9+，无第三方依赖、无网络。脚本相对整理器 Skill 目录。初始化要求父目录已存在、目标工作台尚不存在；需要时先建立用户授权位置的父目录，不在已有工作台上重新初始化。

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

## 按真实变化更新

先show读取当前revision和完整evidence，保存新来源，再制作局部更新JSON。只能改业务字段；id、revision、history由工具维护。evidence采用完整旧列表加新记录，不能原地改旧证据。

| 本次变化 | 更新必须包含的内容 |
|---|---|
| 新增feedback或correction证据 | 显式提交decision与outcome，即使outcome仍是unknown；同步修改受影响next_action，不能只追加日志 |
| 阶段推进到acted | 本次新增action证据，说明真实发生的动作 |
| 阶段推进到feedback | 本次新增feedback证据；correction不能替代这一类型 |
| 纠正原先误记的阶段、退回较早阶段 | 本次新增correction证据，说明为何撤回；没有真实新进展可保留原阶段 |
| 设为waiting | 已有action证据且阶段为acted或feedback；草稿就绪不构成等待对方回复 |
| 目标设为met | 有观察到的feedback证据且阶段为feedback；生成材料不代表现实目标实现 |
| completed或stopped | 清空next_action和review_on；后续新行动另建关联事项，不直接重开 |

例如只更正未实施方案的报价，当前仍为ready，可按下列形态更新；旧证据必须从实际事项复制，来源必须已落盘，示意内容不能直接冒充事实：

```json
{
  "decision": "依据新报价重算后的当前判断",
  "outcome": "unknown",
  "phase": "ready",
  "next_action": "新的必要动作或待本人选择的事项",
  "evidence": [
    {"kind": "input", "text": "原证据原文，实际使用时保留完整旧列表", "source": "资料/原来源.md", "at": "2026-01-01"},
    {"kind": "correction", "text": "新报价更正旧前提，尚未采购", "source": "资料/新来源.md", "at": "2026-01-02"}
  ]
}
```

用读取到的revision调用update；若冲突或拒绝，先回读当前源和错误，不改写证据来凑阶段。更新成功后回读事项、相关模型和接续入口，确认改动一致。completed/stopped可追加证据和改判断，但新行动需另建关联事项。到期仅提示核实。

工具更新前在 `.history/` 保留旧版本；视图失败时事项仍是真源，可重跑render。不要手改 `现在做什么.md`。概览仅显示ID、生命域、状态与阶段，不展示标题、原文、下一步或金额；详细内容按需show。备份同样属于用户材料，不随Skill分享。

## 日期与用户入口

证据 at 是该来源登记日期；事件发生日已知时在 text 或来源正文另写，只有“周一”“明天”而无法确定具体日期时保留原说法，不推造日历日期。review_on 未确定就为 null。

默认概览为保护敏感内容只显示 ID 和状态，用户日常从项目／生活事项入口或接续卡进入，链接回唯一事项源，不再维护第二套状态。脚本可来自已安装整理器，迁移电脑时需重新安装对应套装；脚本绝对路径不是可移植身份，恢复时重新定位当前安装位置。
