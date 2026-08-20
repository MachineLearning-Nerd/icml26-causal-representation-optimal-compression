# Source audit

## Paper identity

- Title: Causal Representation Learning with Optimal Compression under Complex Treatments
- Authors: Wanting Liang; Haoang Chi; Zhiheng Zhang
- arXiv: 2603.11907
- OpenReview: puNfWfBFNT
- Pinned version: v2, 2026-05-02
- Paper: https://arxiv.org/abs/2603.11907
- HTML: https://arxiv.org/html/2603.11907

## Available source

The repository includes the pinned paper PDF, the clean-room multi-treatment
simulator, finite HSIC diagnostics, structured outputs, and the negative
evidence record for CausalEGM. The local paper copy has SHA-256:

`2c938c655bae4ed5d90fa106d1f1f893130696966c53382b64033f42017b36a3`

No author implementation is represented as having been imported or run.

## Evidence boundary

The local code uses the identity representation Phi(X) = X, linear kernels,
explicit one-hot treatment matrices, simplified OLS risk, and finite
synthetic samples. It omits the paper's learned representation, treatment
embedding map, profile criterion, complexity term, generator architecture,
external data, and PEHE experiments.

The finite outputs are evidence about this implementation and these seeded
inputs. They are not formal proofs, population guarantees, or complete
paper-level reproductions.

## Audit conclusion

The paper identity and six-claim contract are pinned. C1 is a tautological
proxy, C2-C5 are bounded finite diagnostics, and C6 is not reproduced. No
complete paper claim is independently verified.
