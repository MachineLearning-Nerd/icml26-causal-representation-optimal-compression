# ICML 2026 — Causal Representation Learning with Optimal Compression

Paper-level result: INCONCLUSIVE.

This repository is an independent, clean-room evidence audit of [Causal
Representation Learning with Optimal Compression under Complex
Treatments](https://arxiv.org/abs/2603.11907). It contains bounded NumPy
diagnostics for selected balancing, HSIC, and multi-treatment bookkeeping
ideas. It does not reproduce the paper's learned representation, formal
theorems, Multi-Treatment CausalEGM generator, or reported PEHE experiments.

The audit package is publishable as documentation of what was checked. It
must not be presented as a complete reproduction: 0/6 complete paper claims
are independently verified, no current external score is claimed, and the
authors did not endorse this repository.

## Paper

- Title: Causal Representation Learning with Optimal Compression under Complex Treatments
- Authors: Wanting Liang, Haoang Chi, and Zhiheng Zhang
- Paper: [arXiv:2603.11907](https://arxiv.org/abs/2603.11907)
- HTML: [arXiv HTML](https://arxiv.org/html/2603.11907)
- OpenReview: [puNfWfBFNT](https://openreview.net/forum?id=puNfWfBFNT)
- Version pinned: arXiv v2, dated 2026-05-02
- Local paper copy: [docs/paper.pdf](docs/paper.pdf)

The paper treats multi-treatment causal representation learning as
controlled compression. Its claims cover balancing constructions, a
generalization bound, finite-sample and asymptotic behavior of a selected
balancing weight, treatment aggregation, and a Multi-Treatment CausalEGM
extension with treatment-manifold geometry.

## Claim ledger

| ID | Paper target | What this repository runs | Status |
| --- | --- | --- | --- |
| C1 | Lemma 3.2 generalization bound | Empirical risk plus a nonnegative HSIC proxy term | TAUTOLOGICAL_PROXY |
| C2 | Theorem 3.5 deviation of alpha-hat | Finite HSIC deviation across sample sizes | PROXY_PASS only |
| C3 | Treatment aggregation scaling | Five small timings of an explicit one-hot HSIC function | PROXY_PASS only |
| C4 | Theorem 3.8 asymptotic normality | Finite normality diagnostic for centered HSIC | PROXY_PASS only |
| C5 | K=20 pairwise instability versus aggregation | Pair-count and one proxy imbalance contrast | PROXY_PASS only |
| C6 | Multi-Treatment CausalEGM and geodesic validation | Explicit negative-evidence record; no generator or PEHE path | NOT_REPRODUCED |

These labels describe the local diagnostics, not successful reproduction of
the corresponding paper claims. The machine-readable contract is in
[claims.json](claims.json), and the detailed production paths are in
[CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md).

## Reproduce the local audit

The dependency-light verifier uses Python and NumPy:

~~~text
python3 repro/src/verify.py
python3 verify_final.py
~~~

The first command writes [outputs/verdict.json](outputs/verdict.json). The
second command checks the published documentation contract, required files,
branch vocabulary, commit attribution, and conservative claim boundary. It
does not turn a proxy diagnostic into a paper-level result.

## How each claim is produced

1. C1 calls `simulate_multi_treatment`, `one_hot`, and
   `optimal_balancing_weight` in `repro/src/core.py`. It records empirical
   risk, imbalance, alpha, and their sum. Because alpha is selected from a
   nonnegative grid and the comparison target is empirical risk itself, the
   upper-bound check is tautological.
2. C2 fixes assignment logits and treatment effects, generates samples at
   n = 80, 200, 500, and 1000, averages eight seeded HSIC deviations per
   size, and stores `deviation_by_n`. This is a finite concentration smoke
   test, not the theorem's alpha-hat deviation bound.
3. C3 evaluates the explicit dense one-hot HSIC function for K = 2, 5, 10,
   20, and 50 and stores the small local timings and their ratio. A handful
   of timings cannot establish the paper's learned training complexity.
4. C4 runs 300 seeded trials at n = 100, centers each finite HSIC statistic
   against one larger finite reference, and records mean, standard
   deviation, and excess kurtosis. It does not estimate the paper's
   profile-optimized alpha-hat.
5. C5 creates a K = 20 synthetic problem, evaluates the available pairwise
   terms, and compares their count and mean proxy imbalance with one
   aggregated HSIC value. It does not measure PEHE, estimator variance, or
   representation collapse.
6. C6 is deliberately recorded as `NOT_REPRODUCED`. There is no local
   Multi-Treatment CausalEGM implementation, treatment-embedding training,
   image/semi-synthetic experiment, PEHE calculation, or
   Wasserstein-geodesic interpolation path.

## Branches

The source repository had one branch, `master`. It is normalized to the
collection's canonical `main` branch. There are no experiment branches in
this snapshot.

- `main` — canonical paper metadata, claim ledger, verifier, and bounded
  NumPy diagnostics.

See [BRANCH_AUDIT.md](BRANCH_AUDIT.md) for the branch policy and history
normalization record.

## Repository map

- `docs/paper.pdf` — pinned arXiv v2 paper copy.
- `repro/src/core.py` — simulator, one-hot treatment encoding, linear-kernel
  HSIC proxy, and simplified balancing-weight grid.
- `repro/src/verify.py` — deterministic finite diagnostics and C6 negative
  evidence.
- `outputs/verdict.json` — measured local values and claim statuses.
- `outputs/gate.json` — conservative documentation and paper-reproduction
  gate metadata.
- `CLAIM_EVIDENCE.md` — claim-to-code-to-output production ledger.
- `SOURCE_AUDIT.md` — source provenance and evidence boundary.
- `ENVIRONMENT.md` — runtime assumptions and commands.
- `REPORT.md` — publication boundary and unblockers.
- `verify_final.py` — fail-closed repository-state verifier.

## Explicit limitations

- The representation is the identity map Phi(X) = X; the learned
  representation and profile objective are absent.
- The simplified alpha grid omits the paper's complexity term, curvature
  assumptions, and population target.
- Linear-kernel, one-hot HSIC is only a finite proxy for treatment balancing.
- Local wall-clock measurements do not prove asymptotic O(1) complexity in K.
- The normality check concerns HSIC, not the alpha-hat M-estimator.
- The K = 20 check does not reproduce the paper's semi-synthetic PEHE or
  runtime study.
- Multi-Treatment CausalEGM, treatment-manifold geometry, image
  reconstruction, and Wasserstein interpolation are absent.

## Citation

~~~bibtex
@article{liang2026causal,
  title={Causal Representation Learning with Optimal Compression under Complex Treatments},
  author={Liang, Wanting and Chi, Haoang and Zhang, Zhiheng},
  journal={arXiv preprint arXiv:2603.11907},
  year={2026}
}
~~~

Please cite the paper for the research claims and this repository for the
independent audit artifacts.

## Thank you

Thank you to Wanting Liang, Haoang Chi, and Zhiheng Zhang for making the
paper available and for developing a thoughtful connection between causal
representation learning, controlled compression, and multi-treatment
balancing. This independent audit is intended for learning and transparent
reproduction accounting; it is not affiliated with or endorsed by the
authors.

## Attribution

Repository documentation and commits are attributed to
MachineLearning-Nerd using
MachineLearning-Nerd@users.noreply.github.com.
