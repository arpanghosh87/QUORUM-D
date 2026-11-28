"""Analytical diagnostics, not guarantees of judge or policy accuracy."""
from math import comb, isfinite
from numbers import Integral
import numpy as np


def _positive_integer(n):
    if isinstance(n, bool) or not isinstance(n, Integral) or n < 1:
        raise ValueError("n must be a positive integer")


def _prob(p):
    if not isfinite(p) or not 0 <= p <= 1:
        raise ValueError("probability must be in [0, 1]")


def majority_accuracy(n, p):
    """Eq. 2: independent, equally competent binary judges; odd panel."""
    _positive_integer(n)
    _prob(p)
    if n % 2 == 0:
        raise ValueError("odd panel required")
    return sum(comb(n, k) * p**k * (1-p)**(n-k) for k in range(n//2+1, n+1))


def effective_size(n, rho):
    """Eq. 3: equal positive marginal variance and common correlation."""
    _positive_integer(n)
    lower = -1/(n-1) if n > 1 else -1
    if not isfinite(rho) or not lower <= rho <= 1:
        raise ValueError("invalid equicorrelation")
    if n == 1:
        return 1.0
    if rho == lower:
        return np.inf
    return n/(1+(n-1)*rho)


def _weights(weights):
    w = np.asarray(weights, dtype=float)
    if w.ndim != 1 or not w.size or not np.isfinite(w).all() or (w < 0).any() or w.sum() <= 0:
        raise ValueError("weights must be finite, nonnegative, with positive sum")
    return w/w.sum()


def _correlation(matrix):
    r = np.asarray(matrix, dtype=float)
    if r.ndim != 2 or not r.size or r.shape[0] != r.shape[1] or not np.isfinite(r).all():
        raise ValueError("finite square correlation matrix required")
    if not np.allclose(r, r.T, atol=1e-10, rtol=0) or not np.allclose(r.diagonal(), 1, atol=1e-10, rtol=0):
        raise ValueError("matrix must be symmetric with unit diagonal")
    if np.linalg.eigvalsh(r).min() < -1e-10:
        raise ValueError("matrix must be positive semidefinite")
    return r


def weighted_effective_size(weights, correlation):
    """Eq. 4: equal marginal variance; PSD alone does not imply binary feasibility."""
    w, r = _weights(weights), _correlation(correlation)
    if w.size != r.shape[0]:
        raise ValueError("weight and matrix dimensions differ")
    v = float(w @ r @ w)
    if v <= 0:
        raise ValueError("positive weighted variance required")
    return 1/v


def minimum_variance_weights(correlation):
    """Closed form R^-1 1; only for nonsingular matrices with nonnegative optimum."""
    r = _correlation(correlation)
    if np.linalg.eigvalsh(r).min() <= 1e-10:
        raise ValueError("positive definite matrix required")
    w = np.linalg.solve(r, np.ones(r.shape[0]))
    w /= w.sum()
    if (w < -1e-10).any():
        raise ValueError("unconstrained optimum is negative; constrained solver required")
    return _weights(np.maximum(w, 0))


def cost_per_effective_unit(cost, ess):
    if not isfinite(cost) or cost < 0 or not isfinite(ess) or ess <= 0:
        raise ValueError("finite nonnegative cost and finite positive ESS required")
    return cost/ess


def weighted_vote(ballots, weights, threshold):
    """Eq. 1: complete binary ballots; threshold in original weight units; ties positive."""
    w = np.asarray(weights, dtype=float)
    _weights(w)
    y = np.asarray(ballots)
    if y.shape != w.shape or not np.isin(y, [0, 1]).all() or not isfinite(threshold) or not 0 < threshold <= w.sum():
        raise ValueError("invalid ballots or threshold")
    return int(w @ y >= threshold)


def policy_objective(calibration, inference, verification, losses, prices):
    """Eq. 5: one realization or expectation of same-horizon costs and losses."""
    c = np.asarray([calibration, inference, verification], dtype=float)
    l, p = np.asarray(losses, dtype=float), np.asarray(prices, dtype=float)
    if l.ndim != 1 or l.shape != p.shape or not l.size:
        raise ValueError("aligned nonempty dimension vectors required")
    values = np.concatenate((c, l, p))
    if not np.isfinite(values).all() or (values < 0).any():
        raise ValueError("finite nonnegative inputs required")
    return float(c.sum()+l @ p)


def error_statistics(ballots, references):
    """Complete common labeled items; constant columns have undefined correlation (NaN)."""
    y, t = np.asarray(ballots), np.asarray(references)
    if y.ndim != 2 or y.shape[0] < 2 or y.shape[1] < 1 or t.shape != (y.shape[0],) or not np.isin(y, [0, 1]).all() or not np.isin(t, [0, 1]).all():
        raise ValueError("complete binary ballots and aligned references required")
    e = (y != t[:, None]).astype(float)
    cov = np.atleast_2d(np.cov(e, rowvar=False, ddof=1))
    scale = np.sqrt(np.outer(cov.diagonal(), cov.diagonal()))
    corr = np.divide(cov, scale, out=np.full_like(cov, np.nan), where=scale > 0)
    return {"n_items": len(t), "error_rate": e.mean(axis=0), "covariance": cov, "correlation": corr}


def correlated_errors(n_items, error_rate, copy_probabilities, seed=34):
    """Section 5.1: independent copy decisions; pair correlation q_i*q_j."""
    _positive_integer(n_items)
    _prob(error_rate)
    q = np.asarray(copy_probabilities, dtype=float)
    if q.ndim != 1 or not q.size or not np.isfinite(q).all() or (q < 0).any() or (q > 1).any():
        raise ValueError("copy probabilities must be a nonempty vector in [0,1]")
    rng = np.random.default_rng(seed)
    common = rng.random((n_items, 1)) < error_rate
    copy = rng.random((n_items, q.size)) < q
    independent = rng.random((n_items, q.size)) < error_rate
    return np.where(copy, common, independent).astype(np.int8)


def pivotal(ballots):
    """Section 4.5: a single replacement can flip majority iff margin is one."""
    y = np.asarray(ballots)
    if y.ndim != 1 or not y.size or y.size % 2 == 0 or not np.isin(y, [0, 1]).all():
        raise ValueError("odd nonempty binary panel required")
    return abs(2*int(y.sum())-y.size) == 1
