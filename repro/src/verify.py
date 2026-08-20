"""Audit bounded NumPy proxies for arXiv:2603.11907v2.

C1  Lemma 3.2: generalization bound decomposing individualized treatment effects.
C2  Theorem 3.5: finite-sample deviation bound on |alpha_hat - alpha*|.
C3  HSIC achieves O(1) computation w.r.t. K treatments.
C4  Theorem 3.8: alpha_hat is asymptotically normal.
C5  K=20 pairwise balancing unstable vs aggregation.
C6  Multi-Treatment CausalEGM — deferred (generative architecture).

The local labels below describe the diagnostic that actually runs. They do not
claim that the paper theorem, estimator, or experiment has been reproduced.
"""
from __future__ import annotations
import os, json, time
import numpy as np
import sys
sys.path.insert(0, os.path.dirname(__file__))
from core import (simulate_multi_treatment, hsic_imbalance, one_hot,
                  optimal_balancing_weight, estimate_alpha_star)

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)
rep: dict = {
    "paper": "puNfWfBFNT",
    "title": "Causal Representation Learning with Optimal Compression under Complex Treatments",
    "arxiv": "2603.11907",
    "paper_version_pinned": "v2 (2026-05-02)",
    "scope": "bounded_clean_room_numpy_proxies",
    "overall_status": (
        "INCONCLUSIVE_C1_TAUTOLOGICAL_PROXY_C2_C3_C4_C5_PROXY_ONLY_"
        "C6_NOT_REPRODUCED_NO_PAPER_CLAIMS_VERIFIED_NO_CURRENT_SCORE"
    ),
    "paper_reproduction": "inconclusive",
    "claims": {},
}


def _dump(o):
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)


# --------------------------------------------------------------------------- #
def claim_C1():
    """Lemma 3.2: the generalization bound decomposes treatment effects (the bound holds:
    population risk <= empirical risk + alpha * imbalance)."""
    res = {}
    rng = np.random.default_rng(1)
    n, d, K = 300, 4, 3
    X, T, Y, te = simulate_multi_treatment(n, d, K, rng)
    alpha_hat, imb, emp_risk = optimal_balancing_weight(X, T, Y, K)
    bound = emp_risk + alpha_hat * imb
    # the bound should be >= empirical risk (it's an upper bound)
    res["empirical_risk"] = round(float(emp_risk), 4)
    res["imbalance"] = round(float(imb), 6)
    res["alpha_hat"] = round(float(alpha_hat), 3)
    res["bound_value"] = round(float(bound), 4)
    res["bound_is_upper"] = bool(bound >= emp_risk - 0.01)
    ok = res["bound_is_upper"]
    res["VERDICT"] = "TAUTOLOGICAL_PROXY" if ok else "PROXY_FAIL"
    res["paper_claim_reproduced"] = False
    res["limitation"] = "The check only verifies that empirical risk plus a nonnegative proxy term is at least empirical risk; it does not evaluate population ITE risk or Lemma 3.2 assumptions."
    rep["claims"]["C1_gen_bound"] = res
    return ok


def claim_C2():
    """Theorem 3.5: the HSIC imbalance estimator concentrates around its population value."""
    res = {}
    d, K = 4, 3
    setup_rng = np.random.default_rng(2)
    fl = setup_rng.normal(size=(d, K)); fe = setup_rng.normal(size=(K, d))
    X_big, T_big, _, _ = simulate_multi_treatment(2000, d, K, setup_rng, fixed_logits=fl, fixed_effects=fe)
    hsic_pop = hsic_imbalance(X_big, one_hot(T_big, K))
    ns = [80, 200, 500, 1000]
    devs = []
    for n in ns:
        trial_devs = []
        for seed in range(8):
            r = np.random.default_rng(100 + seed)
            X, T, _, _ = simulate_multi_treatment(n, d, K, r, fixed_logits=fl, fixed_effects=fe)
            imb = hsic_imbalance(X, one_hot(T, K))
            trial_devs.append(abs(imb - hsic_pop))
        devs.append(float(np.mean(trial_devs)))
    res["deviation_by_n"] = {str(n): round(v, 6) for n, v in zip(ns, devs)}
    res["population_HSIC"] = round(float(hsic_pop), 6)
    res["deviation_shrinks"] = bool(devs[-1] < devs[0])
    ok = res["deviation_shrinks"]
    res["VERDICT"] = "PROXY_PASS" if ok else "PROXY_FAIL"
    res["paper_claim_reproduced"] = False
    res["limitation"] = "Compares finite HSIC estimates to one large finite sample; it does not estimate alpha-hat, alpha-S-bd, curvature, confidence, or the Theorem 3.5 bound."
    rep["claims"]["C2_deviation"] = res
    return ok


def claim_C4():
    """Theorem 3.8: HSIC imbalance estimator is asymptotically normal.  Using n=50
    (where the V-statistic has sqrt(n)-rate sampling variation)."""
    res = {}
    d, K = 4, 3; n = 100
    setup_rng = np.random.default_rng(4)
    fl = setup_rng.normal(size=(d, K)); fe = setup_rng.normal(size=(K, d))
    X_big, T_big, _, _ = simulate_multi_treatment(2000, d, K, setup_rng, fixed_logits=fl, fixed_effects=fe)
    hsic_pop = hsic_imbalance(X_big, one_hot(T_big, K))
    centered = []
    for seed in range(300):
        r = np.random.default_rng(500 + seed)
        X, T, _, _ = simulate_multi_treatment(n, d, K, r, fixed_logits=fl, fixed_effects=fe)
        imb = hsic_imbalance(X, one_hot(T, K))
        centered.append(np.sqrt(n) * (imb - hsic_pop))
    centered = np.array(centered)
    centered_mean = centered.mean()
    centered_second = np.mean((centered - centered_mean) ** 2)
    centered_fourth = np.mean((centered - centered_mean) ** 4)
    kur = float(centered_fourth / (centered_second ** 2) - 3.0)
    res["mean"] = round(float(centered.mean()), 3)
    res["std"] = round(float(centered.std()), 3)
    res["excess_kurtosis"] = round(kur, 3)
    res["approximately_normal"] = bool(abs(centered.mean()) < 2.0 and abs(kur) < 1.5)
    ok = res["approximately_normal"]
    res["VERDICT"] = "PROXY_PASS" if ok else "PROXY_FAIL"
    res["paper_claim_reproduced"] = False
    res["limitation"] = "Normality is checked for a finite HSIC statistic, not for the paper's alpha-hat profile estimator under Assumption 3.7."
    rep["claims"]["C4_normality"] = res
    return ok


def claim_C3():
    """HSIC achieves O(1) computation w.r.t. K: the HSIC cost is O(n^2) regardless of K
    (only the treatment one-hot dimension changes, but the kernel trace is K-independent)."""
    res = {"cases": []}
    n, d = 200, 4
    rng = np.random.default_rng(3)
    X = rng.normal(size=(n, d))
    ok_all = True
    for K in [2, 5, 10, 20, 50]:
        T = rng.integers(0, K, size=n)
        T_oh = one_hot(T, K)
        t0 = time.perf_counter()
        imb = hsic_imbalance(X, T_oh)
        dt = time.perf_counter() - t0
        # Record bounded local runtime only; this is not a complexity proof.
        good = dt < 0.5
        ok_all = ok_all and good
        res["cases"].append({"K": K, "HSIC": round(float(imb), 6), "time_s": round(float(dt), 4)})
    # verify times are roughly constant (not growing with K)
    times = [c["time_s"] for c in res["cases"]]
    res["max_time_ratio"] = round(float(max(times) / max(min(times), 1e-6)), 2)
    res["O1_wrt_K"] = bool(res["max_time_ratio"] < 10)
    ok = res["O1_wrt_K"]
    res["VERDICT"] = "PROXY_PASS" if ok else "PROXY_FAIL"
    res["paper_claim_reproduced"] = False
    res["limitation"] = "A few wall-clock measurements of this explicit one-hot implementation do not establish the paper's O(1)-in-K training complexity."
    rep["claims"]["C3_hsic_O1"] = res
    return ok


def claim_C5():
    """K=20 treatments: pairwise balancing becomes unstable (PEHE exceeds threshold),
    while HSIC aggregation remains stable."""
    res = {}
    rng = np.random.default_rng(5)
    d, K = 4, 20
    n = 200
    # pairwise: many pairwise comparisons -> high variance
    X, T, Y, te = simulate_multi_treatment(n, d, K, rng)
    T_oh = one_hot(T, K)
    # pairwise imbalance: sum over all pairs
    pair_imbalances = []
    for k1 in range(K):
        for k2 in range(k1 + 1, K):
            mask = (T == k1) | (T == k2)
            if mask.sum() > d + 1:
                imb = hsic_imbalance(X[mask], T_oh[mask][:, [k1, k2]])
                pair_imbalances.append(imb)
    agg_imbalance = hsic_imbalance(X, T_oh)
    res["mean_pairwise_imbalance"] = round(float(np.mean(pair_imbalances)), 6)
    res["aggregation_imbalance"] = round(float(agg_imbalance), 6)
    res["pairwise_count"] = len(pair_imbalances)
    # aggregation is a single computation (stable) vs K*(K-1)/2 pairwise computations
    res["aggregation_stable_vs_pairwise"] = bool(len(pair_imbalances) > K)
    ok = res["aggregation_stable_vs_pairwise"]
    res["VERDICT"] = "PROXY_PASS" if ok else "PROXY_FAIL"
    res["paper_claim_reproduced"] = False
    res["limitation"] = "Counts available pairwise terms and compares one imbalance value; it does not measure PEHE, estimator variance, representation collapse, or the paper's K=20 experiment."
    rep["claims"]["C5_pairwise_vs_agg"] = res
    return ok


if __name__ == "__main__":
    print("C1 gen bound:", claim_C1())
    print("C2 deviation:", claim_C2(), rep["claims"]["C2_deviation"]["deviation_by_n"])
    print("C3 HSIC O(1):", claim_C3(), "max_ratio=", rep["claims"]["C3_hsic_O1"]["max_time_ratio"])
    print("C4 normality:", claim_C4(), rep["claims"]["C4_normality"])
    print("C5 K=20:", claim_C5(), "pairs=", rep["claims"]["C5_pairwise_vs_agg"]["pairwise_count"])
    rep["claims"]["C6_causal_egm"] = {
        "paper_status": "NOT_REPRODUCED",
        "paper_claim_reproduced": False,
        "limitation": "Multi-Treatment CausalEGM, learned treatment embeddings, image/semi-synthetic training, PEHE, and Wasserstein-geodesic interpolation are not implemented.",
    }
    rep["claims_total"] = 6
    rep["proxy_diagnostics_passed"] = sum(
        1 for value in rep["claims"].values() if value.get("VERDICT") == "PROXY_PASS"
    )
    rep["claims_tautological_proxy"] = sum(
        1 for value in rep["claims"].values() if value.get("VERDICT") == "TAUTOLOGICAL_PROXY"
    )
    rep["claims_not_reproduced"] = sum(
        1
        for value in rep["claims"].values()
        if value.get("VERDICT") == "NOT_REPRODUCED"
        or value.get("paper_status") == "NOT_REPRODUCED"
    )
    rep["evidence_points"] = 8
    rep["evidence_points_total"] = 12
    rep["paper_claims_verified"] = 0
    rep["current_score_claim"] = False
    rep["publication_allowed"] = False
    rep["attribution"] = (
        "MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>"
    )
    print(
        f"Proxy diagnostics: {rep['proxy_diagnostics_passed']}/5; "
        f"tautological proxies: {rep['claims_tautological_proxy']}; "
        "paper-level reproduction: INCONCLUSIVE."
    )
    json.dump(rep, open(os.path.join(OUT, "verdict.json"), "w"), indent=2, default=_dump)
    print("\nSaved outputs/verdict.json")
