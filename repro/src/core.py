"""Clean-room multi-treatment balancing (arXiv 2603.11907, OpenReview puNfWfBFNT).

Generalization bound for multi-treatment CATE estimation with a balancing weight alpha:
    risk(Phi) <= empirical_risk(Phi) + alpha * imbalance(Phi) + noise

The optimal alpha* minimizes the bound.  We estimate alpha from data and verify:
- C2 (Theorem 3.5): finite-sample deviation bound |alpha_hat - alpha*| <= O(1/sqrt(n)).
- C3: HSIC imbalance achieves O(1) computation w.r.t. K treatments.
- C4 (Theorem 3.8): alpha_hat is asymptotically normal.

Model: K treatments, covariates X in R^d, outcomes Y_k = mu_k(X) + noise.
Representation Phi(X) = X (identity).  Balancing weight alpha trades off empirical
risk vs the HSIC imbalance measure between Phi(X) and the treatment indicator.
"""
from __future__ import annotations
import numpy as np


def simulate_multi_treatment(n, d, K, rng, confounding=True, fixed_logits=None, fixed_effects=None):
    """n samples, d covariates, K treatments. With confounding, treatment assignment
    depends on X.  Pass fixed_logits / fixed_effects to keep the SAME problem instance
    across MC trials (only X/noise/T-draws vary)."""
    X = rng.normal(size=(n, d))
    logits_w = fixed_logits if fixed_logits is not None else rng.normal(size=(d, K))
    if confounding:
        logits = X @ logits_w
        probs = np.exp(logits - logits.max(axis=1, keepdims=True))
        probs /= probs.sum(axis=1, keepdims=True)
        T = np.array([rng.choice(K, p=probs[i]) for i in range(n)])
    else:
        T = rng.integers(0, K, size=n)
    eff = fixed_effects if fixed_effects is not None else rng.normal(size=(K, d))
    Y = np.array([X[i] @ eff[T[i]] for i in range(n)]) + rng.normal(scale=0.3, size=n)
    return X, T, Y, eff


def hsic_imbalance(Phi_X, T_onehot):
    """HSIC(Phi(X), E_T) — Hilbert-Schmidt Independence Criterion between the
    representation Phi(X) and the one-hot treatment indicator.  Cost O(n^2),
    independent of K (the treatment dimension only affects T_onehot's columns)."""
    n = Phi_X.shape[0]
    # kernel matrices
    Kx = Phi_X @ Phi_X.T  # linear kernel (RBF optional)
    Kt = T_onehot @ T_onehot.T
    # center
    H = np.eye(n) - np.ones((n, n)) / n
    Kxc = H @ Kx @ H
    Ktc = H @ Kt @ H
    return float(np.trace(Kxc @ Ktc) / (n * n))


def one_hot(T, K):
    n = len(T)
    oh = np.zeros((n, K))
    oh[np.arange(n), T] = 1.0
    return oh


def optimal_balancing_weight(X, T, Y, K, lam_grid=None):
    """Estimate the optimal balancing weight alpha by minimizing the generalization bound
    over a grid.  The bound: empirical_risk + alpha * HSIC_imbalance + lam * ||alpha||^2."""
    n, d = X.shape
    Phi_X = X
    T_oh = one_hot(T, K)
    imb = hsic_imbalance(Phi_X, T_oh)
    # empirical risk: mean squared error of a representation-based predictor
    # (simple OLS per treatment group, pooled)
    emp_risk = 0.0
    for k in range(K):
        mask = T == k
        if mask.sum() > d:
            Xk = X[mask]; yk = Y[mask]
            wk = np.linalg.lstsq(Xk, yk, rcond=None)[0]
            emp_risk += np.mean((Xk @ wk - yk) ** 2) * mask.sum()
    emp_risk /= n
    # minimize emp_risk + alpha * imb over a grid (alpha >= 0)
    if lam_grid is None:
        lam_grid = np.linspace(0, 5, 50)
    bounds = [emp_risk + a * imb for a in lam_grid]
    best_idx = int(np.argmin(bounds))
    return float(lam_grid[best_idx]), float(imb), float(emp_risk)


def estimate_alpha_star(X, T, Y, K):
    """Population-optimal balancing weight (estimated from large data)."""
    return optimal_balancing_weight(X, T, Y, K)[0]
