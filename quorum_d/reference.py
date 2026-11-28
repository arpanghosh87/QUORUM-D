"""Reference finite-search pipeline using a synthetic execution tape.

No real model calls; the tape stands for independently executed configurations.
Shared calls have their own outcomes. A frozen policy is used on disjoint IID
calibration, development and test items. The search enumerates a fixed menu,
not every admissible policy. No claim of global optimality or risk control.
"""
from dataclasses import dataclass
from itertools import product
import numpy as np
from .statistics import correlated_errors, error_statistics
from .policy import Outcome, Limits, select, held_out


@dataclass(frozen=True)
class Tape:
    ids: tuple
    labels: np.ndarray
    light: np.ndarray  # items x dimensions x 3
    strong: np.ndarray
    shared: np.ndarray
    verifier: np.ndarray


@dataclass(frozen=True)
class Candidate:
    rules: tuple
    weights: tuple

    @property
    def name(self):
        return '+'.join(self.rules)


def synthetic_tape(n, seed, prefix):
    rng = np.random.default_rng(seed)
    labels = rng.integers(0, 2, (n, 2))
    errors = np.stack([correlated_errors(n, p, [.7]*3, seed+10+i)
                       for i,p in enumerate((.22,.25))], axis=1)
    return Tape(tuple(f'{prefix}-{i}' for i in range(n)), labels,
                labels[:,:,None]^errors,
                labels^(rng.random((n,2))<np.array([.10,.18])),
                labels^(rng.random((n,2))<np.array([.12,.14])),
                labels^(rng.random((n,2))<np.array([.06,.09])))


def fit(tape):
    """Competence weights fitted only on calibration data; no elimination."""
    weights, diagnostics = [], []
    for d in range(tape.labels.shape[1]):
        s = error_statistics(tape.light[:,d], tape.labels[:,d])
        w = np.maximum(0, 1-2*s['error_rate'])
        w = w/w.sum() if w.sum() else np.ones(3)/3
        weights.append(tuple(map(float,w)))
        diagnostics.append(dict(error_rate=s['error_rate'].tolist(),
                                correlation=s['correlation'].tolist(), n_items=s['n_items']))
    return tuple(weights), diagnostics


def candidates(weights):
    """Fixed finite menu: 6x6 separate rules plus shared-call alternative."""
    rules = ('single','panel','weighted','verifier','selective','defer')
    return [Candidate(r,weights) for r in product(rules,repeat=2)]+[Candidate(('shared','shared'),weights)]


def execute(policy, tape, calibration_cost_per_item=0.):
    """Run frozen rules using observable ballots; labels only enter scoring.

    Calls are accounted for once per item; for a shared call both dimensions
    use its measured outcomes and the cost is charged once. Parallel latency
    in the tape is the maximum of dimension times (an explicit assumption).
    """
    n,d=tape.labels.shape
    if d!=2 or len(policy.rules)!=d or len(policy.weights)!=d:
        raise ValueError('reference demo supports exactly two dimensions')
    if policy.rules==('shared','shared'):
        return Outcome(policy.name,1,tape.ids,tape.labels,tape.shared.copy(),
                       np.full(n,.025),np.full(n,1.1),calibration_cost_per_item)
    verdict=np.empty((n,d),int); cost=np.zeros(n); lat=np.zeros((n,d)); complexity=0
    for i,rule in enumerate(policy.rules):
        ballots=tape.light[:,i]; panel=(ballots.sum(1)>=2).astype(int)
        if rule=='single': y,c,l,k=tape.strong[:,i],.02,1.,1
        elif rule=='verifier': y,c,l,k=tape.verifier[:,i],.025,1.5,1
        elif rule=='panel': y,c,l,k=panel,.015,1.2,3
        elif rule=='weighted': y,c,l,k=(ballots@np.asarray(policy.weights[i])>=.5).astype(int),.015,1.2,3
        elif rule in ('selective','defer'):
            route=np.abs(2*ballots.sum(1)-3)==1
            if rule=='selective': y,c,l,k=np.where(route,tape.verifier[:,i],panel),.015+.025*route,1.2+.8*route,4
            else: y,c,l,k=np.where(route,-1,panel),.015+.04*route,1.2,3  # assumed human review cost
        else: raise ValueError('unknown rule')
        verdict[:,i]=y; cost+=c; lat[:,i]=l; complexity+=k
    return Outcome(policy.name,complexity,tape.ids,tape.labels,verdict,cost,lat.max(1),calibration_cost_per_item)


def run_reference(cal,dev,test,limits,search_budget,calibration_cost_per_item=0.):
    if set(cal.ids)&set(dev.ids) or set(cal.ids)&set(test.ids) or set(dev.ids)&set(test.ids):
        raise ValueError('calibration/development/test item leakage')
    weights,diagnostics=fit(cal)
    menu=candidates(weights)
    dev_outcomes=[execute(p,dev,calibration_cost_per_item) for p in menu[:search_budget]]
    selected,reports=select(dev_outcomes,limits,search_budget)
    if selected is None:
        return {'decision':'no_automation','calibration':diagnostics,'development':reports}
    frozen=next(p for p in menu if p.name==selected['name'])
    baseline_names={'single+single','panel+panel','weighted+weighted','verifier+verifier','selective+selective','shared+shared',frozen.name}
    test_outcomes=[execute(p,test,calibration_cost_per_item) for p in menu if p.name in baseline_names]
    result=held_out(selected,dev.ids,test_outcomes,limits)
    result.update(calibration=diagnostics,weights=weights,development=reports,
                  frozen={'rules':frozen.rules,'weights':frozen.weights},
                  scope='Synthetic IID finite menu; costs and competence assumed; no live deployment.')
    return result
