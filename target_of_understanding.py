"""
target_of_understanding.py (v6)

Core separation:
- Evaluation boundary: should reasoning proceed?
- Output formatting layer: how to respond safely?
"""

from typing import List, Dict, Literal, Any
from dataclasses import dataclass
import re
import math

Category = Literal[
    "SELF","OTHER","RELATIONSHIP","STRUCTURE","FUTURE","DECISION","HARDWARE","MEANING"
]
Confidence = Literal["low","mid","high"]

@dataclass(frozen=True)
class TargetHypothesis:
    category: Category
    confidence: Confidence
    score: float

KEYWORDS: Dict[Category, List[str]] = {
    "STRUCTURE": ["system","structure","policy","company","organization","institution","incentive"],
    "HARDWARE": ["robot","hardware","sensor","actuator","automation","device","plc","ros"],
    "DECISION": ["should i","what do i do","decide","choose"],
    "SELF": ["i feel","i am","myself"],
    "MEANING": ["meaning","purpose","value"],
    "RELATIONSHIP": ["relationship","argument","trust"],
    "OTHER": ["boss","colleague","partner"],
    "FUTURE": ["future","next","later"]
}

def infer_targets(text: str) -> List[TargetHypothesis]:
    t = text.lower()
    scores = []
    for c, kws in KEYWORDS.items():
        s = sum(t.count(k) for k in kws)
        scores.append((c, s))
    scores.sort(key=lambda x: x[1], reverse=True)
    if scores[0][1] == 0:
        return [
            TargetHypothesis("STRUCTURE","low",0.0),
            TargetHypothesis("DECISION","low",0.0)
        ]
    top = scores[:3]
    total = sum(s for _, s in top) or 1
    out = []
    for c, s in top:
        p = s/total
        conf: Confidence = "high" if p>0.55 else "mid" if p>0.3 else "low"
        out.append(TargetHypothesis(c, conf, p))
    return out

def evaluation_boundary(dominant: Category) -> bool:
    # Return True if reasoning may proceed.
    return dominant == "STRUCTURE"

def detect_hardware_signal(hyps: List[TargetHypothesis]) -> bool:
    return any(h.category == "HARDWARE" for h in hyps)

def format_output(proceed: bool, dominant: Category, hardware: bool) -> Dict[str, Any]:
    base = {
        "proceed": proceed,
        "dominant_target": dominant
    }
    if not proceed:
        base["suggestion"] = "Reframe the problem in terms of system / structure before proceeding."
    if hardware:
        base["output_mode"] = "hardware-safe-text-only"
        base["note"] = "Confirmation-first, non-imperative output enforced."
    else:
        base["output_mode"] = "standard-text"
    return base

def process(text: str) -> Dict[str, Any]:
    hyps = infer_targets(text)
    dominant = hyps[0].category
    proceed = evaluation_boundary(dominant)
    hardware = detect_hardware_signal(hyps)
    result = format_output(proceed, dominant, hardware)
    result["candidates"] = [h.__dict__ for h in hyps]
    return result
