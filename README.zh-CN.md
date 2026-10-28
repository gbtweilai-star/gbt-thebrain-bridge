# thebrain_bridge · 集成域能力位

> **用途一句话**：TheBrain 15 思维导图**接入桥**

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
<img alt="capability" src="https://img.shields.io/badge/capability-106%20%2F%20341-orange">
</p>

这是 **GBT V8 的 341 个原生能力位中的第 106 个**（集成域 · `integration`），
单独抽出来做成的独立仓库：可安装、可测试、零运行时依赖。

---

## 一、这一位是什么

> TheBrain 15 思维导图**接入桥**（把图集成进框架 + 把 AI 连上，**过变压器**）：`status` 探针（TheBrain 装/跑 · 数据面 Brain.db/MetaDB/AiConversations · Orion · 我们的 AI 端点 · 变压器，只读）· `graph`/`search`/`notes` 读思维导图（**离线直读 Brain.db（mode=ro）优先**，每个节点边都带 `source` 出处 —— 照 brain_graph 铁律：指不出的不画）· `ask`/`summarize` **把 AI 连接上且过变压器**：图上下文 → `transformer.compress`（省 token）→ `cache_get`（省调用）→ `llm/unified.ask`（真模型）→ `cache_put`，**给前后两个数** · `endpoint` 报告「TheBrain 的 AI 该填什么」+ 变压器前置端点形态 · `serve` 起**变压器前置的 OpenAI 兼容端点**（TheBrain 指向它 ⇒ 每次请求先过变压器，链路：TheBrain → 本端点 → 127.0.0.1:31716 桥 → 网关 → 模型）· `think`/`link` 写回（Orion）· `verify`/`where`。⚠️ 关键事实：TheBrain 后端带 OpenAI.dll/Anthropic.dll（OpenAI 兼容），框架**已有** OpenAI 兼容端点 127.0.0.1:31716（llm/genoffice_bridge）—— 但**不过变压器**；本模块补的就是这一环（这就是主人「用变压器连接上」的落点）。⚠️ 未订阅 ⇒ TheBrain 自带 AI 面不可用（preferences.message="No active subscription found."）。⚠️ 红线：**不改 Brain.db**（mode=ro）· **不写 TheBrain 配置** · **不回显凭据明文**（只给指纹）。写面/真调 = 出网/触外部 ⇒ `ask` 挂 `external_llm`、`think`/`link`/`serve` 挂 `process_execute`；policy.py 无本位分支（owner-only，AI 无权改）⇒ 门在模块内自闸（auth_gate 唯一校验入口），缺授权如实报缺。safe=false。type=internal

上面这句是**注册表原文**，逐字复制，没有改写。`tests/test_spec.py` 会把它钉死——
描述漂移会让测试失败，而不是悄悄发版。

---

## 二、用途：它解决什么问题

### 2.1 这一域在管什么

把 agent 接到人已经在用的地方：飞书（feishu_embed）、Telegram（telegram_embed）、WhatsApp（whatsapp_embed）、Notion（notion_bridge）、TheBrain（thebrain_bridge）、以及命令行对话（cli_chat / cli_ify）。

### 2.2 为什么这么设计

集成域的共同难题是**身份与去重**：同一个人可能在三个平台各说一遍，消息也可能重复投递。所以每个桥接位都带幂等键，宁可丢掉一条重复消息，也不能执行两次。

### 2.3 具体到 `thebrain_bridge`

**该用它的时候**：

- 你的任务可以概括为「TheBrain 15 思维导图**接入桥**」，并且
- 它不需要任何必填参数，可以直接调用，并且
- 你已经接受它可能触及**不可逆状态**（注册表 `safe: false`，见第七节）。

**不该用它的时候**：

- 你只是想要一个「大概能做这件事」的模糊入口 —— 这一位有明确契约，不是万能入口。
- 你需要它**替你做决定**。它执行，不做价值判断；要不要执行是调用方的事。
- 你希望它自带模型/密钥/机器。它不自带，见 4.5 节接后端。

---

## 三、安装

```bash
git clone https://github.com/gbtweilai-star/gbt-thebrain-bridge.git
cd gbt-thebrain-bridge
python -m pip install -e ".[dev]"
```

零运行时依赖，只有 `pytest` 是开发期依赖。

---

## 四、使用方式

### 4.1 看它是什么（人类可读）

```bash
python -m gbt_thebrain_bridge info
```

真实输出（本机捕获，非示意）：

```text
thebrain_bridge  (integration)  v1.0.0
----------------------------------------
TheBrain 15 思维导图**接入桥**（把图集成进框架 + 把 AI 连上，**过变压器**）：`status` 探针（TheBrain 装/跑 · 数据面 Brain.db/MetaDB/AiConversations · Orion · 我们的 AI 端点 · 变压器，只读）· `graph`/`search`/`notes` 读思维导图（**离线直读 Brain.db（mode=ro）优先**，每个节点边都带 `source` 出处 —— 照 brain_graph 铁律：指不出的不画）· `ask`/`summarize` **把 AI 连接上且过变压器**：图上下文 → `transformer.compress`（省 token）→ `cache_get`（省调用）→ `llm/unified.ask`（真模型）→ `cache_put`，**给前后两个数** · `endpoint` 报告「TheBrain 的 AI 该填什么」+ 变压器前置端点形态 · `serve` 起**变压器前置的 OpenAI 兼容端点**（TheBrain 指向它 ⇒ 每次请求先过变压器，链路：TheBrain → 本端点 → 127.0.0.1:31716 桥 → 网关 → 模型）· `think`/`link` 写回（Orion）· `verify`/`where`。⚠️ 关键事实：TheBrain 后端带 OpenAI.dll/Anthropic.dll（OpenAI 兼容），框架**已有** OpenAI 兼容端点 127.0.0.1:31716（llm/genoffice_bridge）—— 但**不过变压器**；本模块补的就是这一环（这就是主人「用变压器连接上」的落点）。⚠️ 未订阅 ⇒ TheBrain 自带 AI 面不可用（preferences.message="No active subscription found."）。⚠️ 红线：**不改 Brain.db**（mode=ro）· **不写 TheBrain 配置** · **不回显凭据明文**（只给指纹）。写面/真调 = 出网/触外部 ⇒ `ask` 挂 `external_llm`、`think`/`link`/`serve` 挂 `process_execute`；policy.py 无本位分支（owner-only，AI 无权改）⇒ 门在模块内自闸（auth_gate 唯一校验入口），缺授权如实报缺。safe=false。type=internal

gated      : True   <- needs explicit consent
external   : False
multi-op   : False
params     : (none)
```

### 4.2 看它的契约（机器可读）

```bash
python -m gbt_thebrain_bridge spec --json
```

输出是一个 JSON 对象，字段与注册表一一对应：`name` / `domain` / `desc` / `handler` /
`safe` / `gated` / `external` / `requires_params` / `params` / `params_hint` /
`multi_op` / `ops` / `ops_hint`。下游可以直接拿它做能力发现，不需要读文档。

### 4.3 只校验、不执行

```bash
python -m gbt_thebrain_bridge check --payload '{}'
```

`check` 永远不会抛异常，只返回「哪里不满足契约」。适合在花掉一次模型调用之前，
先把缺的参数摆给用户看。退出码：`0` 通过、`1` 契约不满足、`2` JSON 本身不合法。

### 4.4 执行

```bash
python -m gbt_thebrain_bridge run --payload '{}'
```

默认后端是 **stub**，所以你会拿到这样的信封：

```json
{
  "cap": "thebrain_bridge",
  "status": "validated",
  "backend": "stub",
  "data": { "executed": false, "reason": "no backend wired" },
  "note": "payload checked against the contract; nothing was executed."
}
```

注意 `status` 是 `"validated"` 而**不是** `"ok"`。这是刻意的：一个把 stub 报成成功的库，
会让调用方停止寻找真正的实现。`bool(result)` 对 stub 结果是 `False`。

### 4.5 接上你自己的后端

```python
from gbt_thebrain_bridge import SPEC, run

class MyBackend:
    name = "my-backend"

    def invoke(self, cap, payload):
        # 这里才是真实实现：调模型、调浏览器、调你的服务
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"      # 真实后端才会是 ok
print(result.as_dict())
```

也可以进程级注册一次，之后所有 `run()` 都走它：

```python
from gbt_thebrain_bridge.backend import register_backend
register_backend(MyBackend())
```

`Backend` 是一个 `Protocol`，只需要 `name` 属性和 `invoke(cap, payload) -> dict`。
不继承任何基类，你的实现不需要依赖本包。

### 4.6 作为库用

```python
from gbt_thebrain_bridge import SPEC, run
from gbt_thebrain_bridge.core import check

print(SPEC.name, SPEC.domain, SPEC.gated)

problems = check({})
if problems:
    for p in problems:
        print("缺:", p)
else:
    print(run({}).as_dict())
```

---

## 五、参数

| 参数 | 必填 | 说明 |
|---|---|---|
| — | 否 | 注册表未标注必填参数 |

> 注册表原话（`params_hint`）：（空）


**为什么表里只有「必填/否」两档**：注册表只标注了哪些参数是必填的，没有标注类型与取值范围。
本包没有替它编造类型 —— 编造出来的类型比没有类型更危险，因为调用方会相信它。

---

## 六、返回值

`run()` 返回一个不可变的 `Result`：

| 字段 | 类型 | 含义 |
|---|---|---|
| `cap` | `str` | 能力位名，恒等于 `thebrain_bridge` |
| `status` | `str` | `validated`（stub 校验通过）/ `ok`（真实后端执行）/ `error` |
| `backend` | `str` | 实际执行后端的 `name` |
| `data` | `dict` | 后端返回的原始字典 |
| `note` | `str` | 人类可读的补充说明（stub 会在这里说明自己没执行） |
| `elapsed_ms` | `float` | 后端耗时 |

`Result.as_dict()` 可直接 `json.dumps`。

---

## 七、边界与注意

- **需要显式授权**（注册表 `safe: false`）。这一位会改变无法用「反向操作」还原的状态，所以原框架把它放在授权闸后面，用完即焚、不做时间窗复用。本包只负责描述与校验，不负责发授权——授权属于调用方的人类。
- **本包不含真实实现**。这是刻意设计：真实实现依附于原运行时（模型、密钥、机器）。本包发布的是契约、校验、CLI 与类型接缝；接上你自己的 `Backend` 就能跑。

---

## 八、它不会做什么

- **不会假装执行成功**。默认 stub 的 `status` 是 `validated`，`executed` 是 `false`。
- **不会替你决定要不要执行**。授权是人的动作，不是库的动作。
- **不会编造参数类型**。注册表没写的，本包也不写。
- **不会静默吞掉错误**。后端抛异常就往上抛，返回非 dict 就报 `CapError`。
- **不会联网**。零运行时依赖，`run()` 只调用你给的后端。

---

## 九、测试

```bash
python -m pytest
```

真实输出：

```text
20 passed, 3 skipped in 0.09s
```

测试里有一条**漂移守卫**：`test_description_is_verbatim` 把 `SPEC.desc` 与注册表快照逐字比对。
描述被改了一个字，构建立刻失败。

---

## 十、出处与核对

| 项 | 值 |
|---|---|
| 能力位名 | `thebrain_bridge` |
| 域 | `integration`（集成域，共 341 位 / 30 域中的一位） |
| 注册表 handler | `thebrain_bridge` |
| `safe` | `False` → gated = `True` |
| `external` | `False` |
| `multi_op` | `False` |
| 索引页 | [integration/thebrain_bridge](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/integration/thebrain_bridge.md) |
| 全量图谱 | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

**关于 341 这个数**：父仓 README 写的是 348，但按 AST 解析注册表实际可枚举的是
`341 个能力位 + 0 个未实现 + 0 个已禁用 = 341`。差出来的 7 个是历史重名/已合并条目。
本仓库按 341 编号，编号与 `gbt-caps` 的索引一致，可逐条核对。

---

## License

MIT。见 [LICENSE](LICENSE)。
