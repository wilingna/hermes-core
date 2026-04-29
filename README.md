<div align="center">

# 🚀 Hermes Core

### The minimum middle layer that keeps your AI agents from dropping the baton.
### AI 接力赛里的"翻译官"——让多个 AI 之间不掉棒的最小中间层。

**One prompt + 30 lines of code. You can use it today.**
**一段 prompt + 30 行代码，今天就能用。**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Minimal](https://img.shields.io/badge/code-30%20lines-blue.svg)](https://github.com/wilingna/hermes-core)
[![Pattern](https://img.shields.io/badge/pattern-context%20routing-purple.svg)](https://github.com/wilingna/hermes-core)
[![Stars](https://img.shields.io/github/stars/wilingna/hermes-core?style=social)](https://github.com/wilingna/hermes-core)

[English TL;DR](#english-tldr) · [30 秒看懂](#-30-秒看懂有没有-hermes-的差别) · [5 分钟 Quick Start](#-5-分钟-quick-start真的能跑) · [Case Study](#-case-studyhermes-不是空想是从真项目里抽出来的)

</div>

---

<a name="english-tldr"></a>
> **🌍 English TL;DR** — Most AI workflows don't fail because the models are bad. They fail because **Agent A's output is shaped wrong for Agent B to consume**. Hermes is the layer you slot between two agents to **compress, align, constrain, and hand off**. It's not a framework — it's one prompt + 30 lines of glue code, orthogonal to LangChain/MCP. Pulled from production multi-agent systems (PPTFlux's 4-agent pipeline, FLUX's 7-agent pipeline). If you've ever felt your multi-agent flow "starts breaking around step 3," this is what you're missing.

---

大部分 AI 工作流不是死在模型不行，是死在 **Agent A 的输出，Agent B 根本不会用**。
Hermes 就是塞在两个 AI 中间的那一层，负责压缩、对齐、加约束、转交。

一段 prompt + 30 行代码，今天就能用。

---

## 📺 30 秒看懂：有没有 Hermes 的差别

> 下面是一个**示意性例子**（不是真实会议），为了让你一眼看出"加 Hermes"和"不加 Hermes"在 handoff 那一刻的差别。真实的工程化案例见后面 [Case Study](#-case-studyhermes-不是空想是从真项目里抽出来的)。

**场景**：让 Agent A 总结一段会议纪要，然后让 Agent B 基于总结写 PPT 大纲。

### ❌ 不加 Hermes（直接把 A 的输出丢给 B）

Agent A 输出：
```
今天的会议大概一个半小时,讨论的东西还挺杂的。CEO 一上来就说
Q3 业绩不太理想,尤其是华东区,他说同比下滑了大概 18% 左右
(具体数字我没记清),然后老李那边市场部反馈说市场预算之前
被砍了 30%,所以投放节奏跟不上,产品部张总回应说新版本因为
人手不够可能要再推迟一个月。后半段大家就在聊要不要把 SaaS
那条线砍掉,有人支持有人反对,最后没拍板,会议就这么散了,
整体氛围我感觉还是有点紧张的……
```

Agent B 拿到这段后写出来的 PPT：**主线散、重点乱、每页讲什么完全靠猜**。

### ✅ 加上 Hermes（中间过一道结构化 handoff）

Hermes 把 A 的输出转成：
```yaml
[Goal]      为高管做 10 分钟决策汇报
[Audience]  CEO + 业务负责人
[Core]      Q3 业绩压力 → SaaS 业务线去留待决
[Structure] 1.业绩现状  2.压力来源  3.三条路径  4.建议
[Constraints] 每页一个观点 / 不出现"整体氛围"等模糊词
[Next Step] 基于以上结构,生成 4 页 PPT 大纲
```

Agent B 拿到这段后写出来的 PPT：**结构稳、重点准、可以直接讲**。

差别不在模型，在中间这一层。

---

## 🧠 Hermes 是什么

Hermes Core 是一个**轻量级 context-routing 层**，坐在两个 AI agent 之间，做四件事：

1. **压缩**——去掉冗余、口水、解释性废话
2. **对齐**——把上一步输出的结构，改成下一步能直接消费的结构
3. **加约束**——告诉下一个 agent 边界在哪（字数、口吻、禁忌词）
4. **转交**——给一个明确的 Next Step Instruction

> 💡 **关于 "Hermes" 这个名字**
>
> Hermes 在希腊神话里是众神的信使，负责在不同世界之间传递信息。
> 把这个比喻用到 AI agent 协作上，不是我首创的——社区里早有人提过类似的 "messenger / router" 思路。
> 我做的不是发明这个概念，而是**把它产品化**：抽出一段可复用的 prompt、一个 30 行的最小实现、几个真实跑通的案例，让任何人 5 分钟就能用上。
>
> **⚠️ 不要和 Nous Research 的 hermes-agent 搞混**
> AI 圈已经有一个非常知名的同名项目 [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)（20k+ stars），那是一个完整的 self-improving agent 框架，有 skills、memory、多平台 gateway 一整套。
> 我这个 `hermes-core` 是**完全不同的东西**——不是 agent 框架，而是夹在两个 agent 之间的**一层最小胶水**。
> 如果你要找的是"独立运行的智能 agent"，请去 Nous 那边；
> 如果你要的是"让多个 AI 之间不掉棒的最小翻译层"，留下来。

---

## ⚡ 5 分钟 Quick Start（真的能跑）

### 方式 A：零代码，直接用 Prompt（适合小白）

复制下面这段 prompt，粘贴到 ChatGPT / Claude / Gemini 任意一个里：

```
你是一个 Hermes Agent。
你的任务是：把上一步 AI 的输出，转换成下一步 AI 可以直接使用的结构化输入。

请按以下步骤处理：
1. 压缩信息（去掉冗余和口水）
2. 标准化结构（让格式统一）
3. 保留核心意图（不要篡改原意）
4. 添加约束（给下一步明确边界）
5. 准备 handoff（让下一步可以直接消费）

输出必须是以下格式：
[Goal]
[Audience]
[Core Content]
[Structure]
[Constraints]
[Next Step Instruction]

待处理的内容：
{{把上一个 AI 的输出粘贴在这里}}
```

把 `{{...}}` 换成你的真实内容，运行，你就拿到了一个干净的 handoff，可以直接喂给下一个 AI。

### 方式 B：30 行代码版（适合工程师）

```bash
git clone https://github.com/wilingna/hermes-core
cd hermes-core
export OPENAI_API_KEY=sk-...   # 或 OPENROUTER_API_KEY
python hermes.py "你的上一步 AI 输出" "下一步要做什么"
```

`hermes.py` 的实现见仓库根目录，30 行，无依赖（除了 `openai` SDK）。

---

## 🧩 什么时候用 Hermes / 什么时候别用

**该用**：
- 输出要传给另一个 agent（尤其换了模型 / 换了任务类型）
- 你发现工作流"第三步开始翻车"
- 多个 AI 协作，但每次结果都不稳定

**别用**：
- 同一个 agent 内部的反复打磨（rewrite → rewrite）
- 单步生成就能搞定的简单任务
- 你的整个流程只有一个 AI

---

## 🔬 Hermes vs LangChain vs MCP（给科技党）

经常有人问："这玩意儿和 LangChain / MCP / A2A 是什么关系？"

| | 解决的问题 | 形态 | 心智负担 |
|---|---|---|---|
| **LangChain / LlamaIndex** | 编排 agent、管 chain、接工具 | 框架 | 高（要学 API） |
| **MCP / A2A 协议** | 不同 agent / 工具之间的通信标准 | 协议 | 高（要实现 server） |
| **Hermes** | 两个 agent 之间的**语义转交** | 一段 prompt + 30 行胶水 | 极低（复制粘贴） |

Hermes 不是替代品，是**正交的一层**。
你完全可以在 LangChain 里把 Hermes 当成一个 node，也可以在 MCP server 之间夹一层 Hermes。
它是"无论你用什么框架，两个 AI 之间都需要的那道翻译"。

---

## 🏭 Case Study：Hermes 不是空想，是从真项目里抽出来的

我自己有两个跑了几个月的多 agent 项目，Hermes 思路就是从里面抽出来的：

### 📊 [PPTFlux](https://github.com/wilingna/PPTFlux)——4 Agent 把乱资料变成可演示 PPT

代码里实际跑的 4 个 Agent：
**Agent 1 · 资料理解 → Agent 2 · 结构大纲 → Agent 3 · PPT 内容 → Agent 4 · HTML 渲染**

每两个 Agent 之间都有一道 Hermes 风格的转交：

- **Agent 1 → Agent 2**：只把"资料理解结果"打包传过去，原始资料不再透传，避免下游 agent 重新做一遍判断
- **Agent 2 → Agent 3**：把"结构大纲"作为主输入，资料理解标注成"仅供参考，不要重复"，这是典型的 **加约束 + 防止内容漂移**
- **Agent 3 → Agent 4**：这一道是整个项目里 Hermes 含量最高的一段——不是单纯传文本，而是**结构化转交 + 工程化兜底**：
  - `sanitizeAgentSlide()` 清洗 Agent 4 的 HTML（去重复签名、修破损 section）
  - `slotMap` 用 page id 给每页寻址，处理 Agent 4 错位 / 漏页
  - `isValidSlideHtml()` 校验"是不是真的渲染出内容"（catch `<section></section>` 这种空壳）
  - `retrySinglePage()` 单页重试
  - `buildLocalSlide()` 本地兜底

换句话说：**Agent 3 → Agent 4 之间不是一个 prompt，是一整层"翻译 + 校验 + 重试"的中间件**。这就是把 Hermes 从一段 prompt 升级成"工程化中间层"长什么样。

如果你怀疑 "Hermes 只是噱头"，看 PPTFlux 的 `sanitizeAgentSlide / slotMap / retrySinglePage` 这几个函数，就知道为什么没有 Hermes 这一层，4 Agent 流水线根本跑不稳。

### 🤖 [ai-content-pipeline (FLUX)](https://github.com/wilingna/ai-content-pipeline)——7 个 Agent 自动跑内容生产
每个 Agent 之间都是独立 API 调用 + JSON 字段 handoff，本质上每一次 handoff 都是一个 Hermes：
`01_trend.json → 02_topic.json → ... → 07_publish.json`

这个 repo 里的 `runs/<timestamp>/*.json` 就是 Hermes 落地的"物证"——每一个 JSON 都是一次结构化转交。

---

## 🎯 一句话总结

> AI 不是被生成能力限制的，是被**协作能力**限制的。
> Hermes 解决的就是协作那一层。

> **AI isn't bottlenecked by generation. It's bottlenecked by collaboration. Hermes fixes the collaboration layer.**

---

## 📦 The wilingna Methodology Family · 同系列项目

All built on the same idea: **AI as a system, not a chatbot.**
都基于同一个想法：**AI 是系统，不是聊天机器人。**

| Repo | What it does |
|---|---|
| **hermes-core** (this repo) | The glue between two agents · Agent 间的翻译层 |
| [PPTFlux](https://github.com/wilingna/PPTFlux) | 4-agent pipeline → interactive HTML decks · 4 Agent 闭环出 PPT |
| [ai-content-pipeline](https://github.com/wilingna/ai-content-pipeline) | 7-agent content production pipeline · 7 Agent 内容生产线 |
| [ai-decision-5steps](https://github.com/wilingna/ai-decision-5steps) | 5-tool decision framework · 5 工具决策框架 |
| [ai-ppt-toolkit](https://github.com/wilingna/ai-ppt-toolkit) | The original 3-tool methodology · 三件套原版 |

---

## 🔓 License

MIT — 自由使用、修改、分发，注明来源即可。

---

## ⭐ 如果对你有启发

Star 一下，然后去你正在做的某个 AI 工作流里，试着加一道 Hermes。
你大概率会感觉到"咦，稳定多了"。

> Drop a star, then slot Hermes into a multi-agent flow you're already building. You'll feel the difference.
