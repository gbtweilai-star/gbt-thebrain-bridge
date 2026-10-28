# thebrain_bridge

**One capability bit from GBT V8, packaged standalone.** No. 106 of 341,
`integration` domain (Integration).

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
</p>

> TheBrain 15 思维导图**接入桥**（把图集成进框架 + 把 AI 连上，**过变压器**）：`status` 探针（TheBrain 装/跑 · 数据面 Brain.db/MetaDB/AiConversations · Orion · 我们的 AI 端点 · 变压器，只读）· `graph`/`search`/`notes` 读思维导图（**离线直读 Brain.db（mode=ro）优先**，每个节点边都带 `source` 出处 —— 照 brain_graph 铁律：指不出的不画）· `ask`/`summarize` **把 AI 连接上且过变压器**：图上下文 → `transformer.compress`（省 token）→ `cache_get`（省调用）→ `llm/unified.ask`（真模型）→ `cache_put`，**给前后两个数** · `endpoint` 报告「TheBrain 的 AI 该填什么」+ 变压器前置端点形态 · `serve` 起**变压器前置的 OpenAI 兼容端点**（TheBrain 指向它 ⇒ 每次请求先过变压器，链路：TheBrain → 本端点 → 127.0.0.1:31716 桥 → 网关 → 模型）· `think`/`link` 写回（Orion）· `verify`/`where`。⚠️ 关键事实：TheBrain 后端带 OpenAI.dll/Anthropic.dll（OpenAI 兼容），框架**已有** OpenAI 兼容端点 127.0.0.1:31716（llm/genoffice_bridge）—— 但**不过变压器**；本模块补的就是这一环（这就是主人「用变压器连接上」的落点）。⚠️ 未订阅 ⇒ TheBrain 自带 AI 面不可用（preferences.message="No active subscription found."）。⚠️ 红线：**不改 Brain.db**（mode=ro）· **不写 TheBrain 配置** · **不回显凭据明文**（只给指纹）。写面/真调 = 出网/触外部 ⇒ `ask` 挂 `external_llm`、`think`/`link`/`serve` 挂 `process_execute`；policy.py 无本位分支（owner-only，AI 无权改）⇒ 门在模块内自闸（auth_gate 唯一校验入口），缺授权如实报缺。safe=false。type=internal

That description is copied verbatim from the registry. `tests/test_spec.py` pins it,
so documentation drift fails the build instead of shipping quietly.

## What this package actually is

It is the **contract** for one capability: its name, its parameters, the values it
accepts, and whether it can change state that cannot be restored. It is not the
implementation — that lives in the runtime this bit was extracted from.

So `run()` goes through a narrow `Backend` protocol, and the default backend is a
stub that **says so**:

```
status="validated"   backend="stub"   data={"executed": false}
```

Never `status="ok"`. A stub that reports success is worse than no stub, because the
caller stops looking for the real thing.

## Install

```bash
git clone https://github.com/gbtweilai-star/gbt-thebrain-bridge.git
cd gbt-thebrain-bridge
python -m pip install -e ".[dev]"
```

## Use

```bash
python -m gbt_thebrain_bridge info                  # capability card
python -m gbt_thebrain_bridge spec --json           # machine-readable contract
python -m gbt_thebrain_bridge check --payload '{}'
python -m gbt_thebrain_bridge run   --payload '{}'
```

Real `info` output from this machine:

```text
thebrain_bridge  (integration)  v1.0.0
----------------------------------------
TheBrain 15 思维导图**接入桥**（把图集成进框架 + 把 AI 连上，**过变压器**）：`status` 探针（TheBrain 装/跑 · 数据面 Brain.db/MetaDB/AiConversations · Orion · 我们的 AI 端点 · 变压器，只读）· `graph`/`search`/`notes` 读思维导图（**离线直读 Brain.db（mode=ro）优先**，每个节点边都带 `source` 出处 —— 照 brain_graph 铁律：指不出的不画）· `ask`/`summarize` **把 AI 连接上且过变压器**：图上下文 → `transformer.compress`（省 token）→ `cache_get`（省调用）→ `llm/unified.ask`（真模型）→ `cache_put`，**给前后两个数** · `endpoint` 报告「TheBrain 的 AI 该填什么」+ 变压器前置端点形态 · `serve` 起**变压器前置的 OpenAI 兼容端点**（TheBrain 指向它 ⇒ 每次请求先过变压器，链路：TheBrain → 本端点 → 127.0.0.1:31716 桥 → 网关 → 模型）· `think`/`link` 写回（Orion）· `verify`/`where`。⚠️ 关键事实：TheBrain 后端带 OpenAI.dll/Anthropic.dll（OpenAI 兼容），框架**已有** OpenAI 兼容端点 127.0.0.1:31716（llm/genoffice_bridge）—— 但**不过变压器**；本模块补的就是这一环（这就是主人「用变压器连接上」的落点）。⚠️ 未订阅 ⇒ TheBrain 自带 AI 面不可用（preferences.message="No active subscription found."）。⚠️ 红线：**不改 Brain.db**（mode=ro）· **不写 TheBrain 配置** · **不回显凭据明文**（只给指纹）。写面/真调 = 出网/触外部 ⇒ `ask` 挂 `external_llm`、`think`/`link`/`serve` 挂 `process_execute`；policy.py 无本位分支（owner-only，AI 无权改）⇒ 门在模块内自闸（auth_gate 唯一校验入口），缺授权如实报缺。safe=false。type=internal

gated      : True   <- needs explicit consent
external   : False
multi-op   : False
params     : (none)
```

Wire a real implementation:

```python
from gbt_thebrain_bridge import run

class MyBackend:
    name = "my-backend"
    def invoke(self, cap, payload):
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"
```

## Parameters

| name | required | notes |
|---|---|---|
| — | no | the registry declares no required parameters |

Registry hint (`params_hint`): (empty)

Types are deliberately absent: the registry does not declare them, and an invented
type is worse than no type, because callers believe it.

## Boundaries

- Gated: this bit is marked `safe: false` in the registry — it can change state that no inverse action restores.
- No external service dependency declared.
- Single-action bit.
- No implementation ships here. Bring a backend; the protocol is one method.

## What this is not

Not a wrapper around a hosted API. Not a model. Not a promise that calling it does
anything on its own. It is the typed seam plus the validation, which is the part that
stays correct even when the implementation changes.

## Tests

```bash
python -m pytest
```

```text
20 passed, 3 skipped in 0.09s
```

## Provenance

| field | value |
|---|---|
| capability | `thebrain_bridge` |
| domain | `integration` |
| handler | `thebrain_bridge` |
| safe | `False` (gated = `True`) |
| external | `False` |
| atlas page | [integration/thebrain_bridge](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/integration/thebrain_bridge.md) |
| full index | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

The parent README says 348 capabilities; an AST pass over the registry enumerates
`341 + 0 unimplemented + 0 disabled = 341`. The extra 7 are historical duplicates.
Numbering here follows 341 and matches the `gbt-caps` index one-to-one.

## License

MIT.
