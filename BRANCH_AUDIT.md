# Branch audit

## Normalization

- Source tip before standardization: `0af4f3f155e081723b18dd55c775626590695bd2`.
- The source repository exposed `master`; the live repository now exposes
  only `main`.
- Recovery bundle SHA-256:
  `2d292e9e85a63014996690a8976ce28e8944c28fc2ec01e4c5c12f7aa2a5e73b`.
- The recovery bundle preserves the complete pre-normalization history.

## Current branch policy

- `main` is the canonical documentation and verifier branch.
- No branch is presented as a learned causal-representation or CausalEGM
  reproduction.
- New evidence should use a descriptive `audit/...` branch and record the
  paper version, command, inputs, outputs, controls, and limitations before
  merging.

## Attribution policy

All reachable commits in the published history use:

`MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>`

The old `master` name and numeric GitHub identity are retained only in the
recovery bundle and history notes, not as live branch or commit metadata.
