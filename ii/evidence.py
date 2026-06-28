"""Motif UX Evidence Graph: load, validate, index, and deterministically query.

A version-controlled evidence layer (flat JSON under ux-evidence/), not a graph database
and not a UX encyclopedia. The query engine takes a screen/workflow context vector and
returns applicable claims with explicit merge rules, conflicts, sources, and limitations.
Evidence never becomes authority without a matching context, a source, a tier, a
confidence, limitations, and a validation method.
"""
from __future__ import annotations
import json
import pathlib
import datetime
from motif import registry, jsonschema_min

ROOT = registry.ROOT
UXE = ROOT / "ux-evidence"
SCHEMAS = UXE / "schemas"

KINDS = {
    "claims": "evidence-claim.schema.json",
    "sources": "source.schema.json",
    "myths": "myth.schema.json",
    "contradictions": "contradiction.schema.json",
    "validations": "validation-method.schema.json",
    "packs": "evidence-pack.schema.json",
}

_DIMS = ("product_forms", "purposes", "workflows", "expertise", "abilities",
         "devices", "environments", "audience_roles")


def _load(kind):
    d = UXE / kind
    if not d.exists():
        return []
    return [json.loads(p.read_text()) for p in sorted(d.glob("*.json"))]


def load_claims():
    return _load("claims")


def _schema(name):
    return json.loads((SCHEMAS / name).read_text())


def validate() -> tuple[dict, list[str]]:
    counts, errors = {}, []
    for kind, schema_name in KINDS.items():
        schema = _schema(schema_name)
        recs = _load(kind)
        counts[kind] = len(recs)
        seen = set()
        for r in recs:
            rid = r.get("id", "?")
            for e in jsonschema_min.validate(r, schema):
                errors.append(f"{kind}/{rid}: {e}")
            if rid in seen:
                errors.append(f"{kind}/{rid}: duplicate id")
            seen.add(rid)
    # referential: claim sources exist; pack claim_ids/myths exist
    src_ids = {s["id"] for s in _load("sources")}
    claim_ids = {c["id"] for c in load_claims()}
    for c in load_claims():
        for s in c.get("evidence", {}).get("sources", []):
            if s not in src_ids:
                errors.append(f"claims/{c['id']}: source '{s}' not found")
    return counts, errors


def _today():
    return datetime.date.today().isoformat()


def is_stale(claim) -> bool:
    fr = claim.get("freshness", {})
    if fr.get("status") != "current":
        return True
    ra = fr.get("review_after")
    return bool(ra and ra < _today())


def _ctx_risks(ctx):
    out = {}
    for r in ctx.get("risks", []) or []:
        if isinstance(r, dict):
            out[r["type"]] = max(out.get(r["type"], 0), int(r.get("severity", 0)))
        else:
            out[r] = max(out.get(r, 0), 0)
    return out


def _claim(claim_id):
    return next((x for x in load_claims() if x["id"] == claim_id), None)


def _restrict_dims(claim) -> set:
    """Dimensions a claim hard-filters on. Default empty = universal (every dimension wildcard).

    A claim that lists `applicability.restrict` is excluded when one of those dimensions is
    constrained by both claim and context with no intersection. All other dimensions are soft:
    they refine ranking (specificity) but never exclude a claim.
    """
    return set(claim.get("applicability", {}).get("restrict", []) or [])


def match(claim, ctx) -> dict:
    """Match a claim against a context vector.

    Corrected semantics:
      - empty/omitted claim dimension = wildcard (applies to all values on that dimension);
      - existing dimension values are soft relevance signals used only for ranking;
      - a dimension excludes only when it is listed in the claim's `restrict` set and both
        sides constrain it with no set-intersection;
      - more matched dimensions = higher specificity (specific ranks above universal).
    Returns applies, specificity, match_type, matched/wildcard dimensions, reason, and (when
    excluded) the dimension responsible.
    """
    ap = claim.get("applicability", {})
    restrict = _restrict_dims(claim)
    matched, wildcard, spec = [], [], 0
    restricted_hit = False

    for dim in _DIMS:
        cv = set(ap.get(dim, []) or [])
        ctxv = set(ctx.get(dim, []) or [])
        if not cv:
            wildcard.append(dim)
            continue
        if not ctxv:
            # context silent: claim still applies (rule 10: do not invent incompatibility)
            wildcard.append(dim)
            continue
        if cv & ctxv:
            matched.append(dim)
            spec += 1
            if dim in restrict:
                restricted_hit = True
        elif dim in restrict:
            return {"applies": False, "specificity": 0, "match_type": "excluded",
                    "matched_dimensions": [], "wildcard_dimensions": [],
                    "excluded_because": f"{dim}: {sorted(cv)} has no intersection with {sorted(ctxv)}",
                    "reason": f"restricted on {dim} which does not match the context"}
        # soft mismatch on a non-restricted dimension: ignored (does not exclude)

    # typed risk: intersection of types adds specificity; severity refines it
    cr = set(ap.get("risks", []) or [])
    ctxr = _ctx_risks(ctx)
    if cr and ctxr:
        hit = cr & set(ctxr)
        if hit:
            matched.append("risks")
            spec += 1 + (1 if max(ctxr[t] for t in hit) >= 4 else 0)
            if "risks" in restrict:
                restricted_hit = True
        elif "risks" in restrict:
            return {"applies": False, "specificity": 0, "match_type": "excluded",
                    "matched_dimensions": [], "wildcard_dimensions": [],
                    "excluded_because": f"risks: {sorted(cr)} has no intersection with {sorted(ctxr)}",
                    "reason": "restricted on risks which does not match the context"}

    mtype = "restricted-match" if restricted_hit else ("specific" if spec else "universal")
    if mtype == "universal":
        reason = "universal claim (no restricting dimensions); applies to every context"
    elif mtype == "restricted-match":
        reason = f"matches restricted dimension(s) and {spec} context dimension(s): {matched}"
    else:
        reason = f"applies universally; refined by {spec} matching context dimension(s): {matched}"
    return {"applies": True, "specificity": spec, "match_type": mtype,
            "matched_dimensions": matched, "wildcard_dimensions": wildcard, "reason": reason}


def applies(claim, ctx) -> tuple[bool, int]:
    """Backward-compatible thin wrapper over match()."""
    m = match(claim, ctx)
    return m["applies"], m["specificity"]


def _blocking(claim) -> bool:
    """Whether a claim COULD block if a violation were detected (capability, not a verdict)."""
    ev = claim.get("evidence", {})
    return (claim["claim"]["force"] == "normative" and ev.get("tier") == 1
            and ev.get("confidence") == "high" and not is_stale(claim))


# detector finding rule -> the evidence-claim category it can substantiate. Only these rules
# provide machine evidence that an applicable claim is actually violated.
DETECTOR_RULE_CATEGORY = {
    "status-colour-only": "use-of-colour",
    "focus-outline-removed": "focus-indicator",
    "missing-reduced-motion": "reduced-motion",
}
_MIN_BLOCK_CONFIDENCE = 0.7


def _machine_detectable(claim) -> bool:
    d = claim.get("detection", {})
    return bool(d.get("static") or d.get("browser"))


def enforcement_mode(claim) -> str:
    """The enforcement a claim would take IF a violation is detected. This is a capability of
    the claim, never an assertion that the interface currently violates it.

      blocking        normative tier-1 high-confidence and machine-detectable
      warning         other normative / strong-recommendation, machine-detectable
      human_review    not machine-detectable (needs a human or model reviewer)
      informational   contextual / hypothesis guidance
    """
    if not _machine_detectable(claim):
        return "human_review"
    force = claim["claim"]["force"]
    ev = claim.get("evidence", {})
    if force == "normative" and ev.get("tier") == 1 and ev.get("confidence") == "high" and not is_stale(claim):
        return "blocking"
    if force in ("normative", "strong-recommendation"):
        return "warning"
    return "informational"


def _unresolved_contradiction(claim_id) -> bool:
    for ct in _load("contradictions"):
        if claim_id in ct.get("competing_claims", []) and ct.get("human_decision_required"):
            return True
    return False


def evaluate(ctx: dict, findings: list[dict] | None = None) -> dict:
    """Separate applicable claims from actual findings and enforcement.

    An applicable claim is not a finding. A finding is not automatically a blocking
    violation. A normative claim blocks only when a detector provides sufficient evidence
    that the interface violates it, the enforcement mode is machine-supported, and no
    unresolved contradiction prevents enforcement.
    """
    q = query(ctx)
    findings = findings or []
    # correlate detector findings to claim categories (evidence of an actual violation)
    detected: dict[str, list] = {}
    for f in findings:
        cat = DETECTOR_RULE_CATEGORY.get(f.get("rule"))
        if cat:
            detected.setdefault(cat, []).append(f)

    blocking, warnings_out, human_review, needs_eval, informational = [], [], [], [], []
    seen_block_cat = set()
    for cid in q["applicable_claims"]:
        c = _claim(cid)
        mode = enforcement_mode(c)
        cat = c["claim"]["category"]
        evid = detected.get(cat, [])
        base = {"claim": cid, "category": cat, "enforcement_mode": mode,
                "statement": c["claim"]["statement"]}
        if mode == "human_review":
            human_review.append({**base, "finding_status": "human_review_required",
                                 "claim_status": "needs_evaluation"})
            continue
        if not evid:
            # applicable but no detector evidence: a requirement to evaluate, NOT a violation
            (needs_eval if mode in ("blocking", "warning") else informational).append(
                {**base, "claim_status": "needs_evaluation", "enforcement_if_violated": mode})
            continue
        conf = max(f.get("confidence", 0) for f in evid)
        ev_ids = [f["id"] for f in evid]
        unresolved = _unresolved_contradiction(cid)
        confirmed = conf >= _MIN_BLOCK_CONFIDENCE and not unresolved
        entry = {**base, "claim_status": "applicable", "evidence_findings": ev_ids,
                 "evidence_confidence": round(conf, 2),
                 "finding_status": "confirmed" if confirmed else "suspected"}
        if mode == "blocking" and confirmed and cat not in seen_block_cat:
            seen_block_cat.add(cat)
            blocking.append({**entry, "enforcement": "blocking"})
        elif mode == "blocking" and confirmed:
            warnings_out.append({**entry, "enforcement": "warning",
                                 "note": "same root issue as an existing blocking violation"})
        else:
            warnings_out.append({**entry, "enforcement": "warning"})

    return {
        "applicable_claims": len(q["applicable_claims"]),
        "blocking_violations": blocking,
        "warnings": warnings_out,
        "needs_evaluation": needs_eval,
        "human_review_required": human_review,
        "informational": informational,
        "confidence": q["confidence"],
        "summary": {"applicable": len(q["applicable_claims"]),
                    "detected_findings": sum(len(v) for v in detected.values()),
                    "blocking": len(blocking), "warnings": len(warnings_out),
                    "needs_evaluation": len(needs_eval),
                    "human_review_required": len(human_review)},
    }


def query(ctx: dict, explain: bool = False) -> dict:
    claims = load_claims()
    matched, excluded = [], []
    for c in claims:
        m = match(c, ctx)
        if m["applies"]:
            matched.append((m, c))
        elif explain:
            excluded.append({"claim": c["id"], "excluded_because": m.get("excluded_because", ""),
                             "reason": m["reason"]})
    # rank: specificity desc, then tier asc (stronger sources first), then id for stability
    matched.sort(key=lambda x: (-x[0]["specificity"], x[1]["evidence"]["tier"], x[1]["id"]))

    applicable, recs, warnings, requirements, validations, sources, limitations = [], [], [], [], set(), set(), []
    for m, c in matched:
        force = c["claim"]["force"]
        stale = is_stale(c)
        spec = m["specificity"]
        applicable.append(c["id"])
        sources.update(c.get("evidence", {}).get("sources", []))
        limitations.extend(c.get("evidence", {}).get("limitations", []))
        validations.update(c.get("validation", {}).get("methods", []))
        do = c.get("recommendation", {}).get("do", [])
        mode = enforcement_mode(c)
        # an applicable normative requirement is something to evaluate, NOT a current violation
        claim_status = "needs_evaluation" if mode in ("blocking", "warning", "human_review") else "applicable"
        if force == "hypothesis":
            warnings.append({"claim": c["id"], "why": "hypothesis (never blocks)"})
        elif stale:
            warnings.append({"claim": c["id"], "why": "stale claim cannot newly block"})
        if mode == "blocking":
            requirements.append({"claim": c["id"], "category": c["claim"]["category"],
                                 "requirement": c["claim"]["statement"],
                                 "claim_status": "needs_evaluation",
                                 "enforcement_if_violated": "blocking"})
        recs.append({"claim": c["id"], "force": force, "specificity": spec,
                     "tier": c["evidence"]["tier"], "do": do,
                     "match_type": m["match_type"], "matched_dimensions": m["matched_dimensions"],
                     "wildcard_dimensions": m["wildcard_dimensions"],
                     "claim_status": claim_status, "enforcement_if_violated": mode,
                     "sources": c.get("evidence", {}).get("sources", []),
                     "limitations": c.get("evidence", {}).get("limitations", []),
                     "reason": m["reason"]})

    # conflicts: contradictions whose topic-category appears among matched categories
    cats = {c[1]["claim"]["category"] for c in matched}
    conflicts = []
    for ct in _load("contradictions"):
        if any(cat in (ct.get("topic", "") + " ".join(ct.get("competing_claims", []))) for cat in cats):
            conflicts.append({"id": ct["id"], "topic": ct["topic"],
                              "resolution_type": ct.get("resolution_type"),
                              "human_decision_required": ct.get("human_decision_required", False)})

    # confidence: high if any tier-1 normative applies and no critical assumption
    assumptions = set(ctx.get("_assumptions", []) or [])
    critical_assumed = bool(assumptions & {"risks", "abilities"})
    has_norm = any(_blocking(c) for _, c in matched)
    overall = "high" if (has_norm and not critical_assumed) else ("medium" if matched else "low")

    return {
        "applicable_claims": applicable,
        "ranked_recommendations": recs[:30],
        "warnings": warnings,
        # applicable normative requirements to evaluate; NOT detected violations. Actual
        # blocking violations come only from evaluate(ctx, findings) with detector evidence.
        "normative_requirements": requirements,
        "blocked_patterns": [],
        "required_validations": sorted(validations),
        "confidence": {"overall": overall,
                       "note": "lowered: critical context (risk/abilities) is an assumption" if critical_assumed else ""},
        "conflicts": conflicts,
        "sources": sorted(sources),
        "limitations": limitations[:20],
        **({"excluded_claims": excluded} if explain else {}),
    }


def explain(claim_id: str) -> dict:
    c = next((x for x in load_claims() if x["id"] == claim_id), None)
    if not c:
        return {"error": f"no claim '{claim_id}'"}
    return {
        "id": c["id"], "statement": c["claim"]["statement"],
        "force": c["claim"]["force"], "category": c["claim"]["category"],
        "tier": c["evidence"]["tier"], "sources": c["evidence"]["sources"],
        "confidence": c["evidence"]["confidence"], "stale": is_stale(c),
        "limitations": c["evidence"].get("limitations", []),
        "validation": c.get("validation", {}).get("methods", []),
        "blocking": _blocking(c),
        "legal": c.get("legal", {}),
    }


def check_myth(text: str) -> dict:
    t = text.lower().replace("-", " ")
    for m in _load("myths"):
        hay = (m["id"] + " " + m["statement"]).lower().replace("-", " ")
        if t in hay or any(w in hay for w in t.split() if len(w) > 4):
            return {"id": m["id"], "statement": m["statement"], "disposition": m["disposition"],
                    "replacement": m["replacement_principle"],
                    "evidence_against": m.get("evidence_against", []),
                    "still_applies_when": m.get("still_applies_when", [])}
    return {"match": None, "note": "no matching myth in the register"}


def stale_claims() -> list[str]:
    return [c["id"] for c in load_claims() if is_stale(c)]


def build_index() -> pathlib.Path:
    idx = {"counts": {k: len(_load(k)) for k in KINDS},
           "by_category": {}, "by_tier": {}, "by_force": {}}
    for c in load_claims():
        idx["by_category"].setdefault(c["claim"]["category"], []).append(c["id"])
        idx["by_tier"].setdefault(str(c["evidence"]["tier"]), []).append(c["id"])
        idx["by_force"].setdefault(c["claim"]["force"], []).append(c["id"])
    (UXE / "indexes").mkdir(parents=True, exist_ok=True)
    out = UXE / "indexes" / "index.json"
    out.write_text(json.dumps(idx, indent=2) + "\n")
    return out
