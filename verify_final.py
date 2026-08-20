#!/usr/bin/env python3
"""Verify the published causal-compression audit contract."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_IDENTITY = (
    "MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>"
)
EXPECTED_RECOVERY_SHA = (
    "2d292e9e85a63014996690a8976ce28e8944c28fc2ec01e4c5c12f7aa2a5e73b"
)
EXPECTED_SOURCE_TIP = "0af4f3f155e081723b18dd55c775626590695bd2"
EXPECTED_STATUS = (
    "INCONCLUSIVE_C1_TAUTOLOGICAL_PROXY_C2_C3_C4_C5_PROXY_ONLY_"
    "C6_NOT_REPRODUCED_NO_PAPER_CLAIMS_VERIFIED_NO_CURRENT_SCORE"
)
EXPECTED_CLAIMS = {
    "C1": "TAUTOLOGICAL_PROXY",
    "C2": "PROXY_PASS",
    "C3": "PROXY_PASS",
    "C4": "PROXY_PASS",
    "C5": "PROXY_PASS",
    "C6": "NOT_REPRODUCED",
}


def fail(reason: str) -> None:
    print("FINAL_AUDIT=FAILED reason=" + reason)
    raise SystemExit(1)


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail("git_" + "_".join(args))
    return result.stdout.strip()


def load(relative_path: str) -> dict:
    try:
        with (ROOT / relative_path).open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        fail(relative_path + "_invalid_" + type(error).__name__)
    raise AssertionError("unreachable")


local_heads = {
    line
    for line in git(
        "for-each-ref",
        "refs/heads",
        "--format=%(refname:short)",
    ).splitlines()
    if line
}
if local_heads != {"main"}:
    fail("branches_" + ",".join(sorted(local_heads)))
if git("branch", "--show-current") != "main":
    fail("head_not_main")

remote_heads = {
    line.removeprefix("origin/")
    for line in git(
        "for-each-ref",
        "refs/remotes/origin",
        "--format=%(refname:short)",
    ).splitlines()
    if line and line != "origin"
}
if remote_heads and remote_heads != {"main"}:
    fail("remote_branches_" + ",".join(sorted(remote_heads)))

all_refs = git("for-each-ref", "--format=%(refname)").splitlines()
if any(
    ref.endswith("/master")
    or "/orx/" in ref
    or ref.endswith("/orx")
    for ref in all_refs
):
    fail("legacy_branch_ref")

commit_count = int(git("rev-list", "--count", "--all"))
if commit_count < 3:
    fail("commit_count_" + str(commit_count))

identity_rows = git(
    "log",
    "--all",
    "--format=%an <%ae>|%cn <%ce>",
).splitlines()
expected_row = EXPECTED_IDENTITY + "|" + EXPECTED_IDENTITY
if not identity_rows or any(row != expected_row for row in identity_rows):
    fail("noncanonical_commit_identity")

claims_doc = load("claims.json")
claims = {claim["id"]: claim for claim in claims_doc["claims"]}
if set(claims) != set(EXPECTED_CLAIMS):
    fail("claim_ids")
if {
    claim_id: claims[claim_id]["status"]
    for claim_id in EXPECTED_CLAIMS
} != EXPECTED_CLAIMS:
    fail("claim_statuses")
if claims_doc.get("overall_status") != EXPECTED_STATUS:
    fail("claims_status")

audit = claims_doc.get("audit", {})
for field, expected in (
    ("proxy_diagnostics_passed", 4),
    ("claims_tautological_proxy", 1),
    ("claims_not_reproduced", 1),
    ("claims_total", 6),
    ("evidence_points", 8),
    ("evidence_points_total", 12),
    ("paper_claims_verified", 0),
):
    if audit.get(field) != expected:
        fail("claims_" + field)
for field in ("current_score_claim", "publication_allowed"):
    if audit.get(field) is not False:
        fail("claims_" + field)

verdict = load("outputs/verdict.json")
if verdict.get("overall_status") != EXPECTED_STATUS:
    fail("verdict_status")
if verdict.get("paper_reproduction") != "inconclusive":
    fail("verdict_paper_reproduction")
for field, expected in (
    ("claims_total", 6),
    ("proxy_diagnostics_passed", 4),
    ("claims_tautological_proxy", 1),
    ("claims_not_reproduced", 1),
    ("evidence_points", 8),
    ("evidence_points_total", 12),
    ("paper_claims_verified", 0),
):
    if verdict.get(field) != expected:
        fail("verdict_" + field)
for field in ("current_score_claim", "publication_allowed"):
    if verdict.get(field) is not False:
        fail("verdict_" + field)
raw_claims = verdict.get("claims", {})
if raw_claims.get("C1_gen_bound", {}).get("VERDICT") != "TAUTOLOGICAL_PROXY":
    fail("verdict_C1")
for key in (
    "C2_deviation",
    "C3_hsic_O1",
    "C4_normality",
    "C5_pairwise_vs_agg",
):
    if raw_claims.get(key, {}).get("VERDICT") != "PROXY_PASS":
        fail("verdict_" + key)
if raw_claims.get("C6_causal_egm", {}).get("paper_status") != "NOT_REPRODUCED":
    fail("verdict_C6")

gate = load("outputs/gate.json")
for field in ("tests_passed", "documentation_gate_passed", "publication_gate_passed"):
    if gate.get(field) is not True:
        fail("gate_" + field)
for field in (
    "paper_reproduction_gate_passed",
    "paper_algorithm_implemented",
    "paper_claims_reproduced",
    "current_score_claim",
    "publication_allowed",
):
    if gate.get(field) is not False:
        fail("gate_" + field)
for field, expected in (
    ("claims_total", 6),
    ("proxy_diagnostics_passed", 4),
    ("claims_tautological_proxy", 1),
    ("claims_not_reproduced", 1),
    ("evidence_points", 8),
    ("paper_claims_verified", 0),
):
    if gate.get(field) != expected:
        fail("gate_" + field)

verdicts = load("reproduction_verdicts.json")
if verdicts.get("claim_statuses") != EXPECTED_CLAIMS:
    fail("reproduction_claim_statuses")
if verdicts.get("evidence", {}).get("paper_claims_verified") != 0:
    fail("reproduction_paper_claims")

state = load("AUTONOMOUS_STATE.json")
if state.get("status") != EXPECTED_STATUS:
    fail("state_status")
if state.get("repository", {}).get("recovery_bundle_sha256") != EXPECTED_RECOVERY_SHA:
    fail("state_recovery_sha")
if state.get("repository", {}).get("canonical_email") != (
    "MachineLearning-Nerd@users.noreply.github.com"
):
    fail("state_identity")
if state.get("source", {}).get("source_tip_before_standardization") != EXPECTED_SOURCE_TIP:
    fail("state_source_tip")

manifest = load("EVIDENCE_MANIFEST.json")
missing = [
    path
    for path in manifest["required_paths"]
    if not (ROOT / path).is_file()
]
if missing:
    fail("missing_paths_" + ",".join(missing))

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for marker in (
    "2603.11907",
    "CLAIM_EVIDENCE.md",
    "Thank you",
    "0/6",
    "MachineLearning-Nerd",
    "not affiliated with or endorsed",
):
    if marker not in readme:
        fail("readme_" + marker.replace(" ", "_"))

branch_audit = (ROOT / "BRANCH_AUDIT.md").read_text(encoding="utf-8")
for marker in (EXPECTED_IDENTITY, EXPECTED_SOURCE_TIP, EXPECTED_RECOVERY_SHA):
    if marker not in branch_audit:
        fail("branch_audit_" + marker[:12])

print(
    "FINAL_AUDIT=VERIFIED "
    "branches=1 commits="
    + str(commit_count)
    + " claims=C1:tautological_proxy,C2:C3:C4:C5:proxy_only,C6:not_reproduced "
    "evidence_points=8 paper_claims_verified=0 current_score_claim=false "
    "publication_allowed=false"
)
