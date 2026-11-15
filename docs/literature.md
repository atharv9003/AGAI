# Literature review, gaps, and the requirements they produced

> Source material for report §3 (Literature Review) and §4 (Requirements for MAS), and for
> slides 2 and 3. Every row cites a primary source — a peer-reviewed/arXiv paper, an official
> specification, or vendor documentation. Numbers that are **self-reported by the system's own
> authors or vendor** are marked *(self-reported)*; they are not independent measurements and are
> quoted only to characterise a system, never to compare against our results.

## 1. Literature review (one table)

| # | System / work | Kind | Input it starts from | Approach | Reported capability | What it does **not** do |
|---|---|---|---|---|---|---|
| L1 | **SWE-bench** — Jimenez et al., ICLR 2024 [1] | Benchmark | GitHub issue + repo | 2,294 real issues from 12 Python repos; a fix counts only if the repo's own tests pass | Claude 2 / GPT-4 resolved **4.8% / 1.7%** with an oracle retriever *(self-reported)* | Measures *resolve rate only* — no cost, wall-clock, per-agent latency, or run-to-run variance |
| L2 | **SWE-agent** — Yang et al., 2024 [2] | Research agent | GitHub issue + repo | **Single** LLM agent with a purpose-built agent–computer interface (ACI) for navigating, editing, running tests | **12.47%** of SWE-bench full, **18.00%** of SWE-bench Lite (GPT-4 Turbo) *(self-reported)* | One agent plays every role; no independent verifier, no manager, no orchestration alternatives compared |
| L3 | **AutoCodeRover** — Zhang et al., 2024 [3] | Research agent | GitHub issue + repo | Two stages: context retrieval over the **AST** (not a flat file collection) + patch generation | ~**22%** of SWE-bench Lite; **$0.43** average cost per issue *(self-reported; figures shift between arXiv versions)* | Single pipeline; Python-AST assumptions; no cross-framework interop; no human approval gate |
| L4 | **GitHub Copilot Autofix** — GitHub docs [4] | Commercial product | A **CodeQL code-scanning alert** (already localised) | LLM turns the alert + its location into a suggested diff on the pull request | GitHub states it cannot fix every alert and that reviewers must edit before accepting | Does not start from a free-text bug report; the suggestion is **not** verified by running the suite — the human is the verifier |
| L5 | **Getafix / SapFix (Meta)** — Bader et al., 2019 [5] | Industrial, deployed | A **static-analyser (Infer) or Sapienz crash** finding | Mines fix patterns from past human fixes by hierarchical clustering over edits | Top-1 prediction of the human fix up to **91%** *(self-reported)* | Only repairs bug *classes* the analyser already reports; needs a huge proprietary corpus of past fixes; no reasoning over natural language |
| L6 | **Devin (Cognition)** — vendor + independent coverage [6] | Commercial, closed | Natural-language task | Autonomous end-to-end SWE agent | Vendor claims are not independently reproducible; independent testing reported low completion on realistic tasks | Closed system: orchestration, state and provenance cannot be inspected or audited |
| L7 | **MCP** — Model Context Protocol specification [7] | Open standard | — | Standardises how a model reaches **tools and data** | Adopted across vendors as the tool-access layer | Says nothing about how *agents* coordinate with each other |
| L8 | **A2A** — Agent2Agent protocol [8] | Open standard | — | Standardises **agent-to-agent** discovery (agent cards) and messaging across frameworks; complementary to MCP | Official SDKs; ADK and CrewAI named as supporting frameworks | A transport and discovery standard only — it does not prescribe an orchestration topology |
| L9 | **Google ADK** [9] and **CrewAI** [10] | Agent frameworks | — | ADK: workflow + custom agents, tool & model callbacks. CrewAI: role-based Agents/Tasks/Crews and Flows | Both ship A2A integrations | Neither prescribes how to *combine* two frameworks, nor how to evaluate the resulting system |

## 2. Gap from the literature

**LG1 — Repair starts after localisation, not before it.** The deployed systems (L4, L5) are
driven by a static analyser or a crash that has *already* pinpointed the defect. The hard,
everyday case — a human writes "discounts are wrong for bulk orders" and the defect must first be
*found* — is addressed only by the research agents (L2, L3), which are not deployed.

**LG2 — One agent plays every role.** L2 and L3 are single-agent loops. The component that writes
the patch is also the component that judges whether it worked, so there is no independent
verification inside the system.

**LG3 — The orchestration topology is fixed and never evaluated.** Every system in the table
commits to one control flow and reports a resolve rate for it. None reports what its topology
*costs* — in messages, tokens, latency or retries — or whether a different topology would do
better on the same bugs.

**LG4 — Retries discard the evidence.** Where a retry exists it restarts the task. The failure log
that explains *why* the patch was wrong is not routed back to the component that produced it.

**LG5 — Framework lock-in.** Each system is a single stack. MCP (L7) and A2A (L8) now make
cross-framework agent systems possible, but the automated-repair literature predates them and
does not use them.

**LG6 — Safety and auditability are thin.** Research harnesses execute model-written code with no
guardrails; commercial systems (L4, L6) are closed, so provenance cannot be inspected. Human
oversight, where present, is a UI affordance rather than an enforced gate.

**LG7 — Evaluation is one-dimensional.** L1 established resolve rate as *the* metric. L3 is a
partial exception in that it reports average cost per issue, but across the table wall-clock time,
*per-agent* latency, variance over repeated runs, and sensitivity to prompt strategy or to how the
user phrased the report are not reported at all. Where an LLM judge is used, it is seldom
cross-checked against objective test outcomes, so the judge itself is never validated.

**LG8 — Not deployable by a third party.** The research agents are local harnesses; the
commercial ones are closed services.

## 3. Problem statement, restated as testable claims

- **PS1** A developer pastes a free-text bug report (optionally a stack trace) and points at a Git
  repo. The system must **locate** the defect, **explain** the root cause, **write** a patch and
  **prove** it.
- **PS2** A patch nobody verified is a liability: correctness must be demonstrated by the
  *project's own* test suite, not asserted by the model that wrote it.
- **PS3** Nothing may be written to a real repository without explicit human approval.
- **PS4** After the fact, a reviewer must be able to reconstruct what was tried, what it cost, and
  why the run stopped where it did.

## 4. Requirements for the MAS, traced to their origin

Each requirement cites the literature gap (LG) and/or the problem-statement claim (PS) that forced
it, and the agent or mechanism it produced.

| Req | Requirement | Traced to | Agent / mechanism it created |
|---|---|---|---|
| **R1** | Localise a defect from natural language + an optional stack trace, using tools rather than a pre-computed alert | LG1, PS1 | **Diagnoser** (ADK `LlmAgent`, explicit ReAct over MCP tools) |
| **R2** | Separate the agent that *writes* the patch from the agent that *judges* it | LG2, PS2 | **Fixer** (CrewAI Agent+Task) and an independent **Tester** (CrewAI Flow step) that runs the real suite in a fresh clone |
| **R3** | Decide routing, retries and termination in one auditable place | LG2, LG4 | **Manager** (ADK custom agent) with an attempt counter enforced in code |
| **R4** | Make the orchestration topology a *variable*, and measure it | LG3 | Three interchangeable architectures behind `--arch`: hierarchical, sequential, p2p |
| **R5** | On failure, retry the failed stage **with the failure evidence attached**, bounded | LG4, PS2 | Manager re-dispatches to the Fixer with the `TestReport` by reference; `max_attempts`, then a written escalation |
| **R6** | Share state through one inspectable store rather than ad-hoc message passing | LG6, PS4 | **Blackboard** (SQLite, typed Pydantic envelopes, append-only message log) |
| **R7** | Reach every tool through one standard, guarded boundary | LG5, LG6 | **MCP server** (16 tools); sandbox, secrets blocklist and timeouts live in the server, so no agent in either framework can bypass them |
| **R8** | Let agents built on *different* frameworks cooperate over an open protocol | LG5 | **A2A** between the ADK side and the CrewAI side (official `a2a-sdk`, public agent card, bearer-token auth) |
| **R9** | Refuse unsafe input, unsafe tool output and unsafe patches at the boundaries | LG6 | **Guardrails**: input screening, per-agent tool allow-list, Pydantic tool-output checks, patch-safety task guardrail |
| **R10** | Never write to a real repository without a human decision | LG6, PS3 | **Human-in-the-loop gate** before the PR, enforced in the runner, the PR agent *and* the MCP tool (`confirmed=true`, branch must be `codefix/*`) |
| **R11** | Make every run reconstructable after the fact | LG6, PS4 | **Callbacks** (ADK agent/model/tool hooks, CrewAI event bus) → JSONL trace, `runs.db`, Blackboard snapshots, A2A message ids, validated RAG citations |
| **R12** | Evaluate on more than resolve rate, over repeated runs | LG7, PS2 | `codefix bench`: objective re-test in a fresh clone **+** reference-fix comparison **+** LLM-as-judge with agreement scoring; cost, wall-clock, per-agent latency and std-dev across architectures × prompt variants × agent personas × reporter personas |
| **R13** | Be deployable and reachable by someone who is not us | LG8 | Container + **Google Cloud Run**; A2A agent card published at a public URL |

## References

1. C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, K. Narasimhan. *SWE-bench: Can
   Language Models Resolve Real-World GitHub Issues?* ICLR 2024. arXiv:2310.06770.
   https://arxiv.org/abs/2310.06770
2. J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan, O. Press. *SWE-agent:
   Agent-Computer Interfaces Enable Automated Software Engineering.* 2024. arXiv:2405.15793.
   https://arxiv.org/abs/2405.15793
3. Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, Abhik Roychoudhury (National University of Singapore).
   *AutoCodeRover: Autonomous Program Improvement.* 2024. arXiv:2404.05427.
   https://arxiv.org/abs/2404.05427
4. GitHub. *Copilot Autofix for code scanning* (product documentation).
   https://docs.github.com/en/code-security/concepts/code-scanning/copilot-autofix-for-code-scanning
5. J. Bader, A. Scott, M. Pradel, S. Chandra. *Getafix: Learning to Fix Bugs Automatically.*
   OOPSLA 2019. arXiv:1902.06111. https://arxiv.org/abs/1902.06111 — and Meta Engineering,
   *Getafix: How Facebook tools learn to fix bugs automatically*, 2018.
   https://engineering.fb.com/2018/11/06/developer-tools/getafix-how-facebook-tools-learn-to-fix-bugs-automatically/
6. Cognition. *Devin.* https://cognition.ai/ — characterised here only as a closed commercial
   system; no vendor performance claim is relied upon.
7. Anthropic. *Model Context Protocol specification.* https://modelcontextprotocol.io
8. *Agent2Agent (A2A) protocol.* https://a2a-protocol.org — repository:
   https://github.com/a2aproject/A2A
9. Google. *Agent Development Kit (ADK) documentation.* https://google.github.io/adk-docs/
10. CrewAI. *CrewAI documentation.* https://docs.crewai.com
