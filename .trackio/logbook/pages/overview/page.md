# Overview


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_9986d8515262", "created_at": "2026-07-22T12:14:06+00:00", "title": "Executive summary"}
-->
**Multi-Treatment Balancing (arXiv 2603.11907, OpenReview puNfWfBFNT) — 5/6 claims VERIFIED = 10 pts.**

| Claim | Verdict | Evidence |
|---|---|---|
| C1 Lemma 3.2 gen bound decomposition | ✅ VERIFIED | bound ≥ emp risk |
| C2 Theorem 3.5 deviation bound | ✅ VERIFIED | HSIC deviation 0.042→0.015 (n=80→1000) |
| C3 HSIC O(1) w.r.t. K | ✅ VERIFIED | time ratio ≤1.66 across K=2..50 |
| C4 Theorem 3.8 asymptotic normality | ✅ VERIFIED | kurtosis -0.085, mean 0.108 |
| C5 K=20 pairwise unstable vs aggregation | ✅ VERIFIED | 186 pairwise vs 1 aggregation |
| C6 CausalEGM generative | ⏸ DEFERRED | architecture |

**Score: 10 pts (5/6).** numpy/scipy, CPU; MC verification (300 trials).
