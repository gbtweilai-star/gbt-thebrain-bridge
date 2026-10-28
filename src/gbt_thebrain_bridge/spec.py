"""The capability contract, copied verbatim from the GBT V8 registry.

Do not hand-edit: ``tests/test_spec.py`` pins every field against the
registry snapshot so drift fails the build instead of shipping quietly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

_RAW = r"""{
 "name": "thebrain_bridge",
 "domain": "integration",
 "desc": "TheBrain 15 思维导图**接入桥**（把图集成进框架 + 把 AI 连上，**过变压器**）：`status` 探针（TheBrain 装/跑 · 数据面 Brain.db/MetaDB/AiConversations · Orion · 我们的 AI 端点 · 变压器，只读）· `graph`/`search`/`notes` 读思维导图（**离线直读 Brain.db（mode=ro）优先**，每个节点边都带 `source` 出处 —— 照 brain_graph 铁律：指不出的不画）· `ask`/`summarize` **把 AI 连接上且过变压器**：图上下文 → `transformer.compress`（省 token）→ `cache_get`（省调用）→ `llm/unified.ask`（真模型）→ `cache_put`，**给前后两个数** · `endpoint` 报告「TheBrain 的 AI 该填什么」+ 变压器前置端点形态 · `serve` 起**变压器前置的 OpenAI 兼容端点**（TheBrain 指向它 ⇒ 每次请求先过变压器，链路：TheBrain → 本端点 → 127.0.0.1:31716 桥 → 网关 → 模型）· `think`/`link` 写回（Orion）· `verify`/`where`。⚠️ 关键事实：TheBrain 后端带 OpenAI.dll/Anthropic.dll（OpenAI 兼容），框架**已有** OpenAI 兼容端点 127.0.0.1:31716（llm/genoffice_bridge）—— 但**不过变压器**；本模块补的就是这一环（这就是主人「用变压器连接上」的落点）。⚠️ 未订阅 ⇒ TheBrain 自带 AI 面不可用（preferences.message=\"No active subscription found.\"）。⚠️ 红线：**不改 Brain.db**（mode=ro）· **不写 TheBrain 配置** · **不回显凭据明文**（只给指纹）。写面/真调 = 出网/触外部 ⇒ `ask` 挂 `external_llm`、`think`/`link`/`serve` 挂 `process_execute`；policy.py 无本位分支（owner-only，AI 无权改）⇒ 门在模块内自闸（auth_gate 唯一校验入口），缺授权如实报缺。safe=false。type=internal",
 "handler": "thebrain_bridge",
 "safe": false,
 "external": false,
 "requires_params": false,
 "params": [],
 "params_hint": "",
 "multi_op": false,
 "ops": [],
 "ops_hint": ""
}"""


@dataclass(frozen=True)
class CapSpec:
    """Immutable description of one capability bit."""

    name: str
    domain: str
    desc: str
    handler: str
    safe: bool
    external: bool
    requires_params: bool
    params: Tuple[str, ...] = ()
    params_hint: str = ""
    multi_op: bool = False
    ops: Tuple[str, ...] = ()
    ops_hint: str = ""

    @property
    def gated(self) -> bool:
        """True when the registry marks this bit ``safe: false``.

        Gated does not mean "dangerous"; it means the action can change state
        that cannot be restored by running the inverse action.
        """
        return not self.safe

    @property
    def summary(self) -> str:
        """First clause of the description, for one-line listings."""
        for sep in ("\uff08", "\uff1b", "\u3002", ";"):
            if sep in self.desc:
                head = self.desc.split(sep, 1)[0].strip()
                if head:
                    return head
        return self.desc.strip()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "desc": self.desc,
            "handler": self.handler,
            "safe": self.safe,
            "gated": self.gated,
            "external": self.external,
            "requires_params": self.requires_params,
            "params": list(self.params),
            "params_hint": self.params_hint,
            "multi_op": self.multi_op,
            "ops": list(self.ops),
            "ops_hint": self.ops_hint,
        }


_data = json.loads(_RAW)

SPEC = CapSpec(
    name=_data["name"],
    domain=_data["domain"],
    desc=_data["desc"],
    handler=_data["handler"],
    safe=_data["safe"],
    external=_data["external"],
    requires_params=_data["requires_params"],
    params=tuple(_data["params"]),
    params_hint=_data["params_hint"],
    multi_op=_data["multi_op"],
    ops=tuple(_data["ops"]),
    ops_hint=_data["ops_hint"],
)
