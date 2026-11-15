"""Mermaid sources for the explanatory diagrams that are not per-architecture flow graphs.

`codefix/adk_side/pipelines.py::MERMAID` holds one diagram per orchestration architecture
(hierarchical / sequential / p2p) because those *are* the pipelines. The diagrams here describe
cross-cutting structure instead: how agents reach tools through MCP, how the two frameworks
exchange messages, and how the whole thing is deployed.

`codefix graph` exports every diagram in both dicts to `docs/`.

Each diagram is kept truthful by `tests/test_diagrams.py`, which checks the tool names against
the live MCP server, the A2A skill names against the agent card, and the per-agent tool sets
against the agents that call them.
"""

from __future__ import annotations

# Slide 6 (Agent-Tool Communication / MCP). Every tool call in either framework goes through the
# one MCP server, so the sandbox, the secrets blocklist, the timeouts and the PR confirmation
# guard cannot be bypassed by an agent in either framework.
MCP = """flowchart LR
    subgraph ADK["Google ADK"]
      DG["Diagnoser<br/>LlmAgent (ReAct)"]
    end
    subgraph CREW["CrewAI"]
      FX["Fixer<br/>Agent + Task"]
      TS["Tester<br/>Flow step"]
      PR["PR agent<br/>Flow step"]
    end
    DG -->|"MCP tools wrapped as<br/>ADK BaseTool (adk_side/tools.py)"| GB
    FX --> GB
    TS --> GB
    PR --> GB
    GB{{"guardrails<br/>before_tool: per-agent allow-list + arg shape<br/>after_tool: Pydantic type check + untrusted-content wrap"}}
    GB -->|"JSON-RPC over stdio"| S["MCP server (FastMCP)<br/>mcp_server/server.py - 16 tools"]
    S --> T1["read_file · list_tree · code_search<br/>parse_stacktrace · static_analysis"]
    S --> T2["rag_retrieve · index_repo · record_fix<br/>(ChromaDB + all-MiniLM-L6-v2)"]
    S --> T3["create_workspace · discard_workspace<br/>apply_patch · diff_workspace · run_tests"]
    S --> T4["git_branch · git_commit<br/>open_pull_request (needs confirmed=true)"]
    T1 --> SBX["sandbox: repo-root path jail,<br/>secrets blocklist, subprocess timeouts"]
    T3 --> SBX
    T4 --> SBX"""

# Slide 7 (Messaging pattern / A2A). Two distinct mechanisms, deliberately: the Blackboard is the
# shared-state channel *within* the ADK orchestration, and A2A is the wire *between* frameworks.
MESSAGING = """flowchart LR
    subgraph ADKS["ADK service - orchestration"]
      direction TB
      M["Manager<br/>ADK custom agent"]
      D["Diagnoser<br/>ADK LlmAgent"]
    end
    subgraph CREWS["CrewAI service - workers (separate A2A service)<br/>auth: bearer CODEFIX_A2A_TOKEN"]
      direction TB
      F["Fixer + Reviewer"]
      T["Tester"]
      P["PR agent"]
    end
    BB[("<b>Blackboard</b> - shared state<br/>SQLite runs.db<br/><br/>typed Pydantic Envelopes<br/>append-only message log<br/>dispatches carry artifact_refs,<br/>never artifact bodies")]
    M -->|"A2A: fix / test / pr_prepare<br/>JSON-RPC, bearer token"| CREWS
    CREWS -->|"A2A reply: result ids only"| M
    D -->|"A2A: p2p_repair<br/>(p2p architecture only)"| F
    ADKS <==>|"read / write state"| BB
    CREWS <==>|"write Patch / TestReport / PRResult"| BB"""

# Report §Methodology (deployment/platform/service diagram) and Slide 4's deployment context.
DEPLOYMENT = """flowchart LR
    U(["developer's<br/>browser"]) -->|HTTPS| W
    subgraph GCP["Google Cloud - project &lt;gcp-project&gt;"]
      direction LR
      subgraph CR["Cloud Run: codefix-ai (asia-south1, 2 vCPU / 4Gi)"]
        direction LR
        subgraph CT["one container - Dockerfile, built by Cloud Build"]
          direction TB
          W["FastAPI web app<br/>/ · /api/* · run view · dashboard"]
          A["ADK orchestration<br/>Manager + Diagnoser"]
          X["CrewAI A2A service at /a2a/crew/<br/>card: /.well-known/agent-card.json"]
          MS["MCP tool server<br/>stdio subprocess"]
          W --> A
          A -->|"A2A JSON-RPC<br/>+ bearer token"| X
          A --> MS
          X --> MS
        end
      end
      SM[("Secret Manager<br/>zai-api-key")]
      AR[("Artifact Registry<br/>container image")]
    end
    SM -->|"mounted as ZAI_API_KEY,<br/>never baked into the image"| CT
    AR -->|"deployed revision"| CR
    A -->|HTTPS| G["Z.AI<br/>GLM API"]
    X -->|HTTPS| G
    MS -->|"git push / REST"| GH["GitHub<br/>pull request,<br/>after human approval"]
    MS -.->|"runs.db + traces in /tmp:<br/>not durable across restarts"| NOTE["ephemeral<br/>run storage"]"""

DIAGRAMS = {"mcp": MCP, "messaging": MESSAGING, "deployment": DEPLOYMENT}
