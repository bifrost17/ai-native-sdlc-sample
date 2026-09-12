"""
Phase 5 — Experiment metrics.

Reads JSONL experiment logs produced by runner.py and computes accuracy@k
for k = 1..5.

Log entry format (one JSON object per line):
    {
        "case_id":        str,   # WebGen-Bench item id, e.g. "000001"
        "condition":      str,   # "A" | "B" | "C" | "D"
        "tc_id":          str,   # test case id, e.g. "TC-01"
        "attempt":        int,   # 1-based attempt number
        "result":         str,   # "pass" | "fail" | "partial"
        "failure_report": str,   # empty string on pass
    }

accuracy@k definition
---------------------
For each unique tc_id in the log, determine the best result achieved by
attempt ≤ k.  Priority: pass > partial > fail.

    accuracy@k = (N_pass + 0.5 × N_partial) / N_total × 100

This matches the WebGen-Bench accuracy formula and yields a value in [0, 100].
N_total is the number of unique tc_id values in the log.

Usage
-----
    from experiment.metrics import load_log, compute_accuracy_at_k, summarize

    entries = load_log("results/case_000001_condA.jsonl")
    print(summarize(entries))
    # {"accuracy@1": 60.0, "accuracy@2": 60.0, "accuracy@3": 80.0, ...}
"""

import json


def load_log(log_path: str) -> list:
    """Load a JSONL experiment log file and return a list of entry dicts."""
    entries = []
    with open(log_path) as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def _best_result(results: list) -> str:
    """
    Given a list of result strings, return the best one.
    Priority: pass > partial > fail.
    """
    if "pass" in results:
        return "pass"
    if "partial" in results:
        return "partial"
    return "fail"


def compute_accuracy_at_k(log_entries: list, k: int) -> float:
    """
    Compute accuracy@k over all test cases in the log.

    Parameters
    ----------
    log_entries : list of log entry dicts (see module docstring)
    k           : attempt budget (only entries with attempt ≤ k are considered)

    Returns
    -------
    Accuracy as a float in [0.0, 100.0].
    Returns 0.0 for an empty log.
    """
    tc_ids = sorted({e["tc_id"] for e in log_entries})
    if not tc_ids:
        return 0.0

    score = 0.0
    for tc_id in tc_ids:
        results = [
            e["result"]
            for e in log_entries
            if e["tc_id"] == tc_id and e["attempt"] <= k
        ]
        best = _best_result(results) if results else "fail"
        if best == "pass":
            score += 1.0
        elif best == "partial":
            score += 0.5

    return score / len(tc_ids) * 100.0


def summarize(log_entries: list, max_k: int = 5) -> dict:
    """
    Compute accuracy@k for k = 1..max_k.

    Returns
    -------
    dict with keys "accuracy@1" through "accuracy@{max_k}", values in [0, 100].
    """
    return {
        f"accuracy@{k}": compute_accuracy_at_k(log_entries, k)
        for k in range(1, max_k + 1)
    }


def append_log_entry(log_path: str, entry: dict) -> None:
    """Append one JSON entry to a JSONL log file (creates the file if needed)."""
    import os
    os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


# ---------------------------------------------------------------------------
# Token metrics  (mirrors accuracy@k but for cost analysis)
# ---------------------------------------------------------------------------


def compute_tokens_at_k(log_entries: list, k: int) -> dict:
    """
    Compute cumulative token usage up to attempt *k*.

    Log entries are expected to carry ``input_tokens`` and ``output_tokens``
    fields that represent the **cumulative** snapshot at the time of logging.
    For each unique ``tc_id``, we take the entry with the highest attempt ≤ k
    and sum across all test cases.

    Returns
    -------
    dict with keys ``input_tokens``, ``output_tokens``, ``total_tokens``.
    Returns all zeros for an empty log or if no token fields are present.
    """
    tc_ids = sorted({e["tc_id"] for e in log_entries})
    if not tc_ids:
        return {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}

    total_inp = 0
    total_out = 0
    for tc_id in tc_ids:
        # Find the entry with the highest attempt ≤ k for this tc_id
        candidates = [
            e for e in log_entries
            if e["tc_id"] == tc_id and e["attempt"] <= k
        ]
        if not candidates:
            continue
        best = max(candidates, key=lambda e: e["attempt"])
        total_inp += best.get("input_tokens", 0)
        total_out += best.get("output_tokens", 0)

    return {
        "input_tokens": total_inp,
        "output_tokens": total_out,
        "total_tokens": total_inp + total_out,
    }


def summarize_tokens(log_entries: list, max_k: int = 5) -> dict:
    """
    Compute token usage totals for k = 1..max_k.

    Returns
    -------
    dict with keys ``"tokens@1"`` through ``"tokens@{max_k}"``.
    """
    return {
        f"tokens@{k}": compute_tokens_at_k(log_entries, k)
        for k in range(1, max_k + 1)
    }
