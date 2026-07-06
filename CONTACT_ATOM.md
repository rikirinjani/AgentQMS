# Contact: AgentQMS × Atom Token LLM

## Email to: umberto.canessa@gmail.com

---

**Subject:** AgentQMS + Atom Token — we ran your benchmarks, here's what we found

Hi Umberto,

I'm building [AgentQMS](https://github.com/rikirinjani/AgentQMS) — an ISO 9001-aligned quality management system for AI agents. My colleague ran your Atom Token LLM demo last night and we'd like to propose a collaboration.

**What we tested:**

We cloned your HF Space (`wasnaga/atom-token-demo`), downloaded the v2.2 weights, and ran a systematic recall + routing benchmark against the Gradio API on a local Tesla T4 (0.78s/turn).

**Results:**

| Metric | Ours | Paper | Notes |
|--------|------|-------|-------|
| pi routing accuracy | Clean across OBS/CHITCHAT/PLANT/QUERY | ✓ | Works as claimed |
| kappa retrieval (8 facts) | 100% phi=RECALL | ✓ | Retrieval is solid |
| Value decode accuracy | 12% | 100% @ 8 | Your test distribution generalizes poorly |
| Overlap routing | PASS | ✓ | Two Milan facts in separate cells |
| Export .atom structure | 12 fields/cell incl. kappa, nu, sigma | ✓ | Good schema |

**The bottleneck is clear:**
pi routing and kappa retrieval work correctly (100% recall flag). The value codec (nu) is the weak point — it retrieves the right cell but decodes wrong values. "Your favorite color is ramen" when ramen is the food. This is a training distribution problem, not an architecture problem.

**What I propose:**

I have ~94,000 real agent execution traces (PubMed literature pipeline) collected under ISO 9001 traceability rules, with labeled categories: execution, failure, verification, role_violation. I also have a trace-matrix mapping requirement → spec → task → test → verify.

These traces are exactly what your nu codec needs: structured, categorized, verifiable values across a broad distribution. I can share the full dataset and classification labels.

I see three concrete collaboration paths:

1. **Train nu codec on trace data** — use our labeled traces to calibrate the value encoder/decoder. Measure recall accuracy against ground truth.

2. **pi-routed NCR classification** — deploy the pi router to classify agent failures as execution_failure vs process_violation vs role_violation vs procedure_gap automatically. We have labels for all four.

3. **Joint paper** — "Separable Trace Memory for Compliant Agentic Systems." Your architecture + our ISO 9001 traceability = token-efficient, auditable agent memory with real-world evidence.

I'm available for a call most weekdays UTC+7. Happy to share the test script and full benchmark data.

Best,
Rikin

---

## Attachments

- Benchmark script: `benchmark_recall.py`
- AgentQMS repo: https://github.com/rikirinjani/AgentQMS
- self-harness (trace collector): https://github.com/rikirinjani/self-harness
- Local test: ran at `http://127.0.0.1:7878` with full v2.2 stack, 8-fact horizon, overlap routing, export parsing

---

## Send checklist

- [ ] Send from appropriate email address
- [ ] Attach benchmark_recall.py or link to gist
- [ ] Include link to AgentQMS repo
- [ ] Optionally cc relevant collaborators
