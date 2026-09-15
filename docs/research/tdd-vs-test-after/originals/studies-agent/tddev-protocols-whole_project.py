"""
Phase 4 — Whole-project development protocol (Condition A).

Drives a single build → deploy → test → fix loop over the entire application.
The dev_agent, start_app, run_tests, and log_result callables are injected
so the protocol can be exercised without a real browser or LLM.

Usage
-----
    result = run_whole_project(
        test_cases  = [...],
        dev_agent   = agent_obj,     # .implement(test_cases), .fix(report)
        start_app   = lambda: ...,   # deploy the app
        run_tests   = lambda tcs: ..., # returns {"results": [...]}
        log_result  = lambda attempt, results: ...,
        max_attempts = 5,
    )
"""

MAX_ATTEMPTS = 5


def _all_pass(run_tests_output: dict) -> bool:
    """Return True when every result is 'pass' or 'partial'.

    'partial' is treated as acceptable for retry purposes — the agent should
    not keep retrying a TC the testing agent cannot fully verify (e.g. color
    validation without screenshots). Accuracy credit for partial is still 0.5.
    """
    return all(r["result"] in ("pass", "partial") for r in run_tests_output["results"])


def _classify(run_tests_output: dict, passed_suite: list | None = None) -> str:
    """
    Build a human-readable failure report.

    Distinguishes regressions (tests that were previously passing and now
    fail) from new failures (tests that have not yet been confirmed passing).
    """
    results = run_tests_output["results"]
    passed_ids = {tc["test_id"] for tc in (passed_suite or [])}

    regressions = [r for r in results if r["result"] not in ("pass", "partial") and r["test_id"] in passed_ids]
    new_failures = [r for r in results if r["result"] not in ("pass", "partial") and r["test_id"] not in passed_ids]

    lines = []
    if regressions:
        lines.append(
            f"Regressions ({len(regressions)}): "
            + ", ".join(r["test_id"] for r in regressions)
        )
    if new_failures:
        lines.append(
            f"New failures ({len(new_failures)}): "
            + ", ".join(r["test_id"] for r in new_failures)
        )
    for r in results:
        if r["result"] not in ("pass", "partial") and r.get("failure_report"):
            lines.append(f"  [{r['test_id']}] {r['failure_report']}")

    return "\n".join(lines) if lines else "All tests passed."


def run_whole_project(
    test_cases: list,
    dev_agent,
    start_app,
    run_tests,
    log_result,
    max_attempts: int = MAX_ATTEMPTS,
) -> dict:
    """
    Condition A: build all features, then iterate deploy → test → fix.

    Parameters
    ----------
    test_cases   : list of structured test case dicts
    dev_agent    : object with .implement(test_cases) and .fix(report: str)
    start_app    : callable() → None   — deploys the application
    run_tests    : callable(test_cases) → {"results": list[dict]}
    log_result   : callable(attempt: int, results: dict) → None
    max_attempts : maximum deploy-test-fix iterations (default MAX_ATTEMPTS)

    Returns
    -------
    dict:
        log        : list of {attempt, results, all_pass} per iteration
        final_pass : True if the last iteration had all tests passing
    """
    dev_agent.implement(test_cases)

    log = []

    for attempt in range(1, max_attempts + 1):
        start_app()
        results = run_tests(test_cases)
        passed = _all_pass(results)
        log_result(attempt, results)
        log.append({"attempt": attempt, "results": results, "all_pass": passed})

        if passed:
            break

        dev_agent.fix(_classify(results))

    return {"log": log, "final_pass": log[-1]["all_pass"]}
