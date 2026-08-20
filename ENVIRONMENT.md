# Environment and reproduction entry points

## Runtime

- Python: 3.x
- Numerical dependency: NumPy
- Data: generated in memory by `repro/src/core.py`
- Hardware: CPU is sufficient for the bounded diagnostics
- Paper contract: arXiv 2603.11907 v2, 2026-05-02

There is no author training environment, external dataset download, or
dependency lockfile in this audit snapshot.

## Audit commands

~~~text
python3 repro/src/verify.py
python3 verify_final.py
~~~

`repro/src/verify.py` writes `outputs/verdict.json`. It uses fixed random
seeds for the finite diagnostics, but C3 records local wall-clock values and
those timings can vary by machine.

`verify_final.py` validates repository structure, branch names, commit
attribution, required metadata, and the conservative claim boundary. It does
not rerun the scientific verifier.

## Interpretation

Passing the local command means that the bounded diagnostic completed. It
does not upgrade any `PROXY_PASS` to a paper claim. Reproduction of C6
requires implementing or obtaining the missing CausalEGM and geodesic
pipeline, with its data, training configuration, and reported metrics.
