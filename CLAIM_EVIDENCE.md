# Claim-to-evidence ledger

This ledger separates the paper target from the finite computation that is
actually present in this repository. A `PROXY_PASS` is evidence that the
local diagnostic completed under its stated inputs; it is not a reproduced
paper theorem, estimator, or experiment.

## Evidence accounting

The audit records 8 of 12 scoped evidence points:

- C1: 1 point for the recorded tautological inequality.
- C2: 2 points for the finite HSIC estimates and their decreasing deviation
  diagnostic.
- C3: 2 points for the K sweep and bounded timing ratio.
- C4: 2 points for the centered finite-statistic moments.
- C5: 1 point for the pair-count and aggregate comparison.
- C6: 0 points because the generative experiment is absent.

The count is an audit accounting device. It is not a paper score.

## C1 — Lemma 3.2 generalization bound

- Paper target: a causal generalization bound relating population risk to
  empirical risk, imbalance, and its assumptions.
- Production path: `repro/src/verify.py:claim_C1` calls
  `repro/src/core.py:simulate_multi_treatment`,
  `optimal_balancing_weight`, and `hsic_imbalance`.
- Inputs: 300 synthetic observations, four covariates, three treatments, and
  seed 1.
- Output fields: `empirical_risk`, `imbalance`, `alpha_hat`,
  `bound_value`, and `bound_is_upper` in
  `outputs/verdict.json:C1_gen_bound`.
- Status: `TAUTOLOGICAL_PROXY`.
- Boundary: alpha is selected from a nonnegative grid and the local
  comparison is empirical risk plus a nonnegative term versus empirical
  risk. No population ITE risk, theorem assumptions, or learned
  representation is evaluated.

## C2 — Theorem 3.5 finite-sample deviation

- Paper target: the deviation behavior and bound for the optimized
  balancing weight alpha-hat.
- Production path: `claim_C2` fixes assignment logits and treatment effects,
  generates samples at four sizes, computes `hsic_imbalance`, and averages
  eight seeded absolute deviations per size.
- Inputs: n = 80, 200, 500, and 1000; one finite reference sample of size
  2000; seeds 100 through 107.
- Output fields: `deviation_by_n`, `population_HSIC`, and
  `deviation_shrinks`.
- Status: `PROXY_PASS` only.
- Boundary: the code does not calculate alpha-hat, alpha-star, confidence
  bounds, curvature, or the theorem's constants.

## C3 — Treatment aggregation scaling

- Paper target: the treatment-aggregation construction and its claimed
  O(1)-in-K scaling.
- Production path: `claim_C3` creates one fixed covariate matrix, calls
  `one_hot` and `hsic_imbalance` for five K values, and records elapsed
  time.
- Inputs: n = 200, four covariates, K = 2, 5, 10, 20, and 50, seed 3.
- Output fields: `cases`, `max_time_ratio`, and `O1_wrt_K`.
- Status: `PROXY_PASS` only.
- Boundary: this is a literal dense NumPy one-hot implementation. Five
  small wall-clock values are not a complexity proof and do not measure
  learned treatment embeddings or training.

## C4 — Theorem 3.8 asymptotic normality

- Paper target: asymptotic normality of the optimized alpha-hat estimator.
- Production path: `claim_C4` runs 300 seeded finite trials, centers each
  HSIC value against one larger finite reference, and computes moments with
  NumPy.
- Inputs: n = 100, reference n = 2000, 300 trials, seeds 500 through 799.
- Output fields: `mean`, `std`, `excess_kurtosis`, and
  `approximately_normal`.
- Status: `PROXY_PASS` only.
- Boundary: the statistic is finite HSIC, not the paper's profile
  alpha-hat M-estimator; no asymptotic theorem or regularity condition is
  established.

## C5 — K = 20 pairwise versus aggregation

- Paper target: the paper's multi-treatment comparison in which pairwise
  balancing becomes unstable relative to aggregation.
- Production path: `claim_C5` simulates K = 20, enumerates treatment pairs,
  computes available pairwise HSIC values, and compares their mean with one
  aggregate value.
- Inputs: n = 200, four covariates, K = 20, seed 5.
- Output fields: `mean_pairwise_imbalance`,
  `aggregation_imbalance`, `pairwise_count`, and
  `aggregation_stable_vs_pairwise`.
- Status: `PROXY_PASS` only.
- Boundary: this does not measure PEHE, variance, learned representations,
  or the paper's reported semi-synthetic experiment.

## C6 — Multi-Treatment CausalEGM and geodesic validation

- Paper target: the generative extension with treatment embeddings,
  counterfactual generation, PEHE, and Wasserstein-geodesic interpolation.
- Production path: `outputs/verdict.json:C6_causal_egm` records the explicit
  negative evidence and missing implementation scope.
- Status: `NOT_REPRODUCED`.
- Missing: learned treatment embeddings, CausalEGM training, image or
  semi-synthetic data path, PEHE calculation, and geodesic interpolation.

## Recheck commands

~~~text
python3 repro/src/verify.py
python3 verify_final.py
~~~

The output JSON is an auditable local record. It should not be edited to
upgrade a status without adding the corresponding code, inputs, controls,
and evidence.
