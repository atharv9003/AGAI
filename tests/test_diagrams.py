"""The report and the slide deck are built from these diagrams, so a diagram that drifts away
from the code is worse than no diagram. Each test pins one claim a diagram makes against the
thing it describes."""

from __future__ import annotations

import re

import pytest

from codefix.adk_side.pipelines import MERMAID
from codefix.diagrams import DEPLOYMENT, DIAGRAMS, MCP, MESSAGING


def _names(src: str) -> set[str]:
    """Every identifier-looking word inside the node labels of a Mermaid source."""
    return set(re.findall(r"[a-z_][a-z0-9_]{3,}", src))


def test_mcp_diagram_lists_only_real_tools():
    """Every tool the MCP diagram names must exist on the server, and vice versa."""
    from mcp_server import server

    served = {n for n in dir(server) if not n.startswith("_") and callable(getattr(server, n, None))}
    # the @mcp.tool() decorated functions are module-level callables with a docstring
    tools = {n for n in served if getattr(getattr(server, n), "__module__", "") == server.__name__}
    declared = {t for t in _names(MCP) if t in tools}
    missing = {t for t in tools if t not in _names(MCP)} - {"ctx", "main"}
    assert not missing, f"MCP diagram does not mention these server tools: {sorted(missing)}"
    assert len(declared) >= 16, f"expected >=16 tools named in the diagram, found {len(declared)}"


def test_mcp_diagram_tool_count_matches_the_server():
    """The '16 tools' caption must not go stale when a tool is added or removed."""
    from mcp_server import server

    n = len([n for n in dir(server)
             if not n.startswith("_") and callable(getattr(server, n, None))
             and getattr(getattr(server, n), "__module__", "") == server.__name__]) - 2  # ctx, main
    stated = int(re.search(r"(\d+) tools", MCP).group(1))
    assert stated == n, f"MCP diagram says '{stated} tools', server exposes {n}"


def test_diagnoser_tool_allowlist_is_what_the_diagram_shows():
    from codefix.agents.diagnoser import TOOLS

    for t in TOOLS:
        assert t in MCP, f"Diagnoser uses {t}; the MCP diagram does not show it"


def test_messaging_diagram_names_the_real_a2a_skills():
    """Slide 7 claims four A2A skills; they must be the ones the agent card actually publishes."""
    from codefix.crew_side.a2a_server import agent_card

    skills = {s.id for s in agent_card("http://x/").skills}
    assert skills, "agent card publishes no skills"
    for s in skills:
        assert s in MESSAGING, f"agent card publishes skill {s!r}; the messaging diagram omits it"


def test_messaging_diagram_names_the_auth_env_var():
    from codefix import a2a_link

    assert "CODEFIX_A2A_TOKEN" in MESSAGING
    assert "CODEFIX_A2A_TOKEN" in a2a_link.auth_headers.__doc__


def test_deployment_diagram_matches_the_deploy_script():
    """Service name, region and the secret must agree with deploy/deploy_cloudrun.ps1."""
    from codefix import config

    script = (config.ROOT / "deploy" / "deploy_cloudrun.ps1").read_text(encoding="utf-8")
    for token in ("codefix-ai", "asia-south1", "gemini-api-key"):
        assert token in script, f"{token} is not in the deploy script"
        assert token in DEPLOYMENT, f"{token} is in the deploy script but not the deployment diagram"


def test_deployment_diagram_mount_path_matches_the_web_app():
    from codefix import config

    app = (config.ROOT / "web" / "api" / "app.py").read_text(encoding="utf-8")
    assert "/a2a/crew" in app and "/a2a/crew/" in DEPLOYMENT


@pytest.mark.parametrize("name,src", sorted(DIAGRAMS.items()))
def test_every_diagram_is_parseable_mermaid(name, src):
    """Cheap structural check: a declared graph type and balanced brackets in every label."""
    assert src.startswith(("flowchart", "graph", "sequenceDiagram")), f"{name}: no graph type"
    for ch_open, ch_close in (("[", "]"), ("(", ")"), ("{", "}")):
        assert src.count(ch_open) == src.count(ch_close), f"{name}: unbalanced {ch_open}{ch_close}"


def test_graph_export_covers_architectures_and_diagrams():
    """`codefix graph` must write every diagram, so docs/ can never be partially regenerated."""
    assert set(DIAGRAMS) == {"mcp", "messaging", "deployment"}
    assert not set(DIAGRAMS) & set(MERMAID), "a diagram name collides with an architecture name"
