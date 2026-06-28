"""Motif MCP server.

A dependency-free JSON-RPC 2.0 server over stdio (newline-delimited messages) that
exposes Motif's deterministic engines as MCP tools and resources. Read-only by default;
write tools require an explicit --allow-write flag and are audit-logged. No arbitrary
shell, no secret exposure, no network ingestion outside the source-refresh workflow.
"""
from __future__ import annotations
import json
import sys
import datetime
from motif import registry
from . import data, graph as graph_mod, genome as genome_mod, debt as debt_mod
from . import originality as orig_mod, runtime, findings as findings_mod, recommend as rec_mod

SERVER_INFO = {"name": "motif", "version": "3.0.0"}

# name -> (description, handler(args) -> result, write?)
def _tools():
    return {
        "motif.inspect_project": ("Detect framework, routes, components of a target repo.",
                                  lambda a: runtime.model_project(a.get("target", ".")).to_dict(), False),
        "motif.get_design_genome": ("Return a Product Design Genome by name.",
                                    lambda a: genome_mod.load(a.get("name", "")) or {"error": "not found"}, False),
        "motif.query_interaction_graph": ("Run a named interaction-graph query.",
                                          lambda a: {"query": a.get("query"), "findings": graph_mod.query(a.get("query"))}, False),
        "motif.search_atlas": ("Search registry records by substring.",
                               lambda a: _search(a.get("q", "")), False),
        "motif.recommend_pattern": ("Recommend a pattern for a context.",
                                    lambda a: rec_mod.recommend(a.get("pattern", ""), a.get("profile", "saas-balanced")), False),
        "motif.calculate_debt": ("Interface Debt score over a target path.",
                                 lambda a: _debt(a.get("target", ".")), False),
        "motif.audit_originality": ("Aesthetic Convergence score over a path.",
                                    lambda a: _orig(a.get("target", ".")), False),
        "motif.list_findings": ("List unified findings for a target.",
                                lambda a: {"findings": findings_mod.load(a.get("target", "."))}, False),
        "motif.calculate_states": ("Required states for a component type.",
                                   lambda a: _states(a.get("component_type", "")), False),
        "motif.record_decision": ("Record a design decision (write).",
                                  lambda a: {"recorded": a.get("id"), "note": "stub write tool"}, True),
        "motif.plan_change": ("Plan a controlled change (write-class, dry-run).",
                              lambda a: {"plan": "dry-run", "target": a.get("target", "."), "note": "use the installer for apply"}, True),
    }


def _search(q):
    hits = []
    for kind in ("sources", "components", "patterns", "effects"):
        for r in registry.load_records(kind):
            d = r.data
            if q.lower() in (d.get("name", "") + d.get("id", "")).lower():
                hits.append({"kind": kind, "id": d["id"], "name": d.get("name")})
    return {"query": q, "results": hits[:50]}


def _debt(target):
    d = debt_mod.calculate(target)
    return {"score": d.score, "band": debt_mod.band(d.score), "by_category": d.by_category}


def _orig(target):
    _f, score, band = orig_mod.audit_path(target)
    return {"score": score, "band": band}


def _states(ct):
    from . import states as states_mod
    return states_mod.required_map().get(ct, {"error": f"unknown component_type '{ct}'"})


RESOURCES = {
    "motif://registry/sources": lambda: [r.data for r in registry.load_records("sources")],
    "motif://registry/patterns": lambda: [r.data for r in registry.load_records("patterns")],
    "motif://registry/components": lambda: [r.data for r in registry.load_records("components")],
    "motif://atlas/index": lambda: {k: v for k, v in data.validate_all_data()[0].items()},
}


def _audit(method, params):
    try:
        runtime.ensure_state(".")
        log = runtime.state_root(".") / "runs" / "mcp-audit.jsonl"
        with log.open("a") as f:
            f.write(json.dumps({"method": method, "params": params}) + "\n")
    except OSError:
        pass


def dispatch(method: str, params: dict, allow_write: bool) -> dict:
    tools = _tools()
    if method == "initialize":
        return {"protocolVersion": "2024-11-05", "serverInfo": SERVER_INFO,
                "capabilities": {"tools": {}, "resources": {}}}
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": [{"name": n, "description": d,
                           "inputSchema": {"type": "object"}} for n, (d, _h, _w) in tools.items()]}
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {}) or {}
        if name not in tools:
            return {"isError": True, "content": [{"type": "text", "text": f"unknown tool {name}"}]}
        desc, handler, write = tools[name]
        if write and not allow_write:
            return {"isError": True, "content": [{"type": "text",
                    "text": f"tool '{name}' is a write action; restart with --allow-write to enable"}]}
        _audit(name, args)
        result = handler(args)
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
    if method == "resources/list":
        return {"resources": [{"uri": u, "name": u} for u in RESOURCES]}
    if method == "resources/read":
        uri = params.get("uri")
        if uri not in RESOURCES:
            return {"contents": [], "isError": True}
        return {"contents": [{"uri": uri, "mimeType": "application/json",
                              "text": json.dumps(RESOURCES[uri](), indent=2)}]}
    raise KeyError(method)


def serve(allow_write: bool = False) -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        rid = req.get("id")
        try:
            result = dispatch(req.get("method", ""), req.get("params", {}) or {}, allow_write)
            resp = {"jsonrpc": "2.0", "id": rid, "result": result}
        except KeyError as e:
            resp = {"jsonrpc": "2.0", "id": rid,
                    "error": {"code": -32601, "message": f"Method not found: {e}"}}
        except Exception as e:  # noqa: BLE001
            resp = {"jsonrpc": "2.0", "id": rid, "error": {"code": -32603, "message": str(e)}}
        if rid is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
    return 0
