"""Finite joint-policy search on paired, precomputed outcomes (Rev34 Algorithm 1).

The caller executes actual candidate configurations, including shared prompts. This
module does not infer joint outcomes by merging standalone judgments. IID Wilson
intervals are descriptive selection diagnostics, not simultaneous risk guarantees.
"""
from dataclasses import dataclass
from math import sqrt
import numpy as np


@dataclass(frozen=True)
class Limits:
    cost: float
    latency: float
    coverage: float
    risk: tuple
    loss_prices: tuple
    deferral_loss: float = 0.5
    z: float = 1.96


@dataclass(frozen=True)
class Outcome:
    name: str
    complexity: int
    ids: tuple
    reference: np.ndarray
    verdict: np.ndarray  # -1 means defer; 0/1 are automated decisions
    cost: np.ndarray  # per-item total, including shared resources only once
    latency: np.ndarray  # measured end-to-end seconds, not sum of parallel calls
    calibration_cost_per_item: float = 0.0


def wilson(k, n, z=1.96):
    if n == 0:
        return 0., 1.
    p = k/n
    center = (p+z*z/(2*n))/(1+z*z/n)
    radius = z*sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
    return max(0.,center-radius), min(1.,center+radius)


def measure(o, limits):
    y, t = np.asarray(o.verdict), np.asarray(o.reference)
    c, latency = np.asarray(o.cost), np.asarray(o.latency)
    if (y.ndim != 2 or y.shape != t.shape or not len(y) or not y.shape[1]
            or len(o.ids) != len(y) or len(set(o.ids)) != len(y)
            or not np.isin(y, [-1,0,1]).all() or not np.isin(t,[0,1]).all()
            or c.shape != (len(y),) or latency.shape != c.shape
            or not np.isfinite(c).all() or not np.isfinite(latency).all()
            or (c<0).any() or (latency<0).any()
            or not np.isfinite(o.calibration_cost_per_item) or o.calibration_cost_per_item<0):
        raise ValueError('invalid paired outcome')
    d=y.shape[1]
    if (len(limits.risk)!=d or len(limits.loss_prices)!=d
            or not np.isfinite([limits.cost,limits.latency,limits.coverage,limits.deferral_loss,limits.z,*limits.risk,*limits.loss_prices]).all()
            or min(limits.cost,limits.latency,limits.deferral_loss,*limits.loss_prices)<0
            or limits.z<=0 or not 0<=limits.coverage<=1 or any(not 0<=r<=1 for r in limits.risk)):
        raise ValueError('invalid limits')
    accepted=y!=-1; wrong=accepted&(y!=t)
    count=accepted.sum(0); errors=wrong.sum(0)
    intervals=[wilson(int(k),int(n),limits.z) for k,n in zip(errors,count)]
    coverage=count/len(y)
    loss=(wrong+limits.deferral_loss*~accepted).mean(0)
    cost=float(c.mean()+o.calibration_cost_per_item); p95=float(np.quantile(latency,.95))
    upper=np.array([v[1] for v in intervals]); lower=np.array([v[0] for v in intervals])
    risk=np.divide(errors,count,out=np.full(d,np.nan),where=count>0)
    feasible=bool(cost<=limits.cost and p95<=limits.latency and (coverage>=limits.coverage).all() and (upper<=limits.risk).all())
    failed=bool(cost>limits.cost or p95>limits.latency or (coverage<limits.coverage).any() or (lower>limits.risk).any())
    return dict(name=o.name, complexity=o.complexity, cost=cost, p95_latency=p95, coverage=coverage.tolist(),
                accepted_risk=risk.tolist(), risk_intervals=intervals, all_item_error=(errors/len(y)).tolist(),
                loss=loss.tolist(), joint_error=float(wrong.all(1).mean()),
                objective=float(cost+loss@np.asarray(limits.loss_prices)), feasible=feasible, failed=failed)


def paired_check(outcomes):
    first=outcomes[0]
    if len({o.name for o in outcomes})!=len(outcomes):
        raise ValueError('duplicate policy names')
    for o in outcomes[1:]:
        if o.ids!=first.ids or not np.array_equal(o.reference,first.reference):
            raise ValueError('policies must use identical ordered items and references')


def select(development, limits, search_budget):
    """Predeclared finite ordered candidate set; no access to held-out outcomes."""
    if not isinstance(search_budget,int) or search_budget<1:
        raise ValueError('positive integer search budget required')
    candidates=list(development)[:search_budget]
    if not candidates:
        return None, []
    paired_check(candidates)
    reports=[measure(o,limits) for o in candidates]
    feasible=[r for r in reports if r['feasible']]
    selected=min(feasible,key=lambda r:(r['objective'],r['complexity'],r['name'])) if feasible else None
    return selected, reports


def held_out(selected, development_ids, test, limits):
    """Evaluate frozen name and declared baselines once; caller must retain frozen rules.

    Returns paired IID standard errors for per-item loss differences versus selected.
    No retuning, no population-level guarantee, no automatic live deployment.
    """
    if selected is None:
        return {'decision':'no_automation','reports':[]}
    test=list(test)
    if not test:
        raise ValueError('held-out outcomes required')
    paired_check(test)
    if set(development_ids)&set(test[0].ids):
        raise ValueError('held-out item leakage')
    chosen=next((o for o in test if o.name==selected['name']),None)
    if chosen is None:
        raise ValueError('frozen policy missing')
    reports=[measure(o,limits) for o in test]
    result=next(r for r in reports if r['name']==chosen.name)
    def loss(o):
        return ((o.verdict!=-1)&(o.verdict!=o.reference))+limits.deferral_loss*(o.verdict==-1)
    for o,r in zip(test,reports):
        diff=loss(o)-loss(chosen)
        r['paired_loss_difference']=diff.mean(0).tolist()
        r['paired_loss_se']=(diff.std(0,ddof=1)/sqrt(len(diff))).tolist() if len(diff)>1 else None
    return {'decision':'deploy_candidate' if result['feasible'] else 'do_not_deploy' if result['failed'] else 'defer', 'selected':chosen.name,'reports':reports}
