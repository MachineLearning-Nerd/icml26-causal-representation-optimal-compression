# ICML 2026 — Causal Representation and Optimal Compression

Paper-level status: INCONCLUSIVE.

This repository is an independent, clean-room evidence audit for [Causal Representation Learning with Optimal Compression under Complex Treatments](https://arxiv.org/abs/2603.11907). It contains bounded NumPy simulations for selected HSIC and multi-treatment diagnostics. It does not reproduce the paper's profile-optimized representation learner, formal theorem guarantees, Multi-Treatment CausalEGM generator, or reported PEHE experiments.

## Paper

- Title: Causal Representation Learning with Optimal Compression under Complex Treatments
- Authors: Wanting Liang, Haoang Chi, and Zhiheng Zhang
- Paper identifier: arXiv:2603.11907
- Claim contract pinned here: v2, revised 2026-05-02
- [arXiv record](https://arxiv.org/abs/2603.11907)
- [Paper HTML](https://arxiv.org/html/2603.11907)
- [OpenReview page](https://openreview.net/forum?id=puNfWfBFNT)

The paper frames multi-treatment causal representation learning as controlled compression. It studies pairwise, one-vs-all, and treatment-aggregation balancing; derives a generalization bound and a finite-sample/asymptotic analysis for a bound-optimized balancing weight alpha; and proposes HSIC-based treatment aggregation with claimed O(1) scaling in the treatment cardinality. Its generative extension, Multi-Treatment CausalEGM, uses treatment embeddings and Wasserstein-geodesic structure for counterfactual generation.

## Version and evidence boundary

The included paper PDF is v2. The local code uses identity representations Phi(X) = X, linear kernels, explicit one-hot treatment matrices, simplified OLS risk, and finite synthetic samples. Those choices are useful for smoke tests but do not implement the paper's learned representation, treatment embedding map, profile criterion, complexity term, or CausalEGM architecture.

## Claim ledger

| ID | Paper claim or artifact | Local evidence | Honest status |
| --- | --- | --- | --- |
| C1 | Lemma 3.2 multi-treatment generalization bound | Checks that empirical risk plus a nonnegative proxy term is at least empirical risk | TAUTOLOGICAL_PROXY |
| C2 | Theorem 3.5 finite-sample deviation of alpha-hat | Compares finite HSIC estimates with one larger finite sample at several n values | PROXY_PASS; alpha-hat theorem not reproduced |
| C3 | Treatment aggregation O(1) in K | Five small wall-clock checks of the explicit one-hot HSIC function | PROXY_PASS; no training-complexity proof |
| C4 | Theorem 3.8 asymptotic normality of alpha-hat | Finite normality diagnostic for a centered HSIC statistic | PROXY_PASS; alpha-hat profile CLT not reproduced |
| C5 | K=20 pairwise instability versus aggregation | Counts 186 pairwise terms and compares one proxy imbalance value | PROXY_PASS; PEHE and instability experiment not reproduced |
| C6 | Multi-Treatment CausalEGM and Wasserstein-geodesic validation | No generator, treatment embeddings, image training, PEHE, or interpolation pipeline | NOT_REPRODUCED |

The local verifier reports four proxy diagnostics and one tautological proxy. It reports zero independently verified paper claims.

## How each claim is produced

Run:

~~~text
python3 repro/src/verify.py
~~~

The command writes outputs/verdict.json.

1. C1 simulates confounded multi-treatment data, fits the simplified proxy, and evaluates empirical risk plus alpha times HSIC. Since alpha is nonnegative and the comparison target is empirical risk itself, this is not a population generalization check.
2. C2 generates one finite reference sample and compares HSIC estimates from smaller samples under fixed assignment logits and treatment effects. The decreasing deviations are a finite concentration smoke test, not the theorem's alpha-hat deviation bound.
3. C3 measures the explicit dense one-hot HSIC function for K in 2, 5, 10, 20, and 50. The code records stable small timings, but the matrix implementation is not evidence of the paper's learned embedding or O(1)-in-K training complexity.
4. C4 centers finite HSIC estimates from 300 trials and computes an excess-kurtosis diagnostic using NumPy moments. The measured statistic is not the paper's optimized alpha estimator.
5. C5 computes all available pairwise HSIC values for K=20 and compares their mean with one aggregated HSIC value. This checks bookkeeping and a proxy contrast, not PEHE, variance, or representation collapse.
6. C6 records the missing Multi-Treatment CausalEGM and geodesic experiment as NOT_REPRODUCED.

## Repository map

- docs/paper.pdf — the pinned arXiv v2 paper.
- repro/src/core.py — multi-treatment simulator, linear-kernel HSIC proxy, one-hot encoding, and simplified alpha grid.
- repro/src/verify.py — deterministic finite audit and explicit C6 negative evidence.
- outputs/verdict.json — canonical structured verdict.
- outputs/gate.json — documentation gate metadata.
- STATUS.md — current reproduction status.
- GATE_READY.md — scope and publication gate statement.
- BRANCH_AUDIT.md — branch normalization and policy.
- outputs/verify_run.log — local verifier output when generated.

## Scope limitations

- No population ITE risk, counterfactual outcome distributions, or causal identification guarantee is evaluated.
- The simplified alpha grid omits the paper's complexity term, learned representation optimization, curvature assumptions, and profile score.
- The literal one-hot HSIC path does not implement the paper's learnable treatment embeddings.
- Timing five small matrix calculations cannot establish asymptotic O(1) training complexity in K.
- The normality diagnostic is for HSIC, not the alpha-hat M-estimator.
- The K=20 check does not reproduce the paper's semi-synthetic PEHE or runtime results.
- Multi-Treatment CausalEGM, UCI Digits training, image reconstruction, treatment-manifold geometry, and Wasserstein interpolation are absent.

## Citation

~~~bibtex
@article{liang2026causal,
  title={Causal Representation Learning with Optimal Compression under Complex Treatments},
  author={Liang, Wanting and Chi, Haoang and Zhang, Zhiheng},
  journal={arXiv preprint arXiv:2603.11907},
  year={2026}
}
~~~

## Thank you

Thank you to Wanting Liang, Haoang Chi, and Zhiheng Zhang for making this work available and for articulating the connection between causal representation learning, controlled compression, and multi-treatment balancing. This repository is an independent learning and evidence-audit effort and is not affiliated with or endorsed by the authors.

## Attribution

Approved repository documentation and commits are attributed to MachineLearning-Nerd using the GitHub noreply identity. The repository name and branch names are normalized for the ICML 2026 collection.
