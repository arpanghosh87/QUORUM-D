"""Generate numerical and Markdown outcomes from focused research checks."""
import json
from pathlib import Path
import numpy as np
from quorum_d.research_checks import (exchangeable_moments, covariance_variance,
    constrained_weights, conditional_errors, paired_bootstrap)
from quorum_d.reference import synthetic_tape, fit, candidates, execute


def run():
    families = [
        ('Independent fair votes', [1/8,3/8,3/8,1/8]),
        ('Even parity', [1/4,0,3/4,0]),
        ('Odd parity', [0,3/4,0,1/4]),
        ('Independent competent votes', [1/64,9/64,27/64,27/64]),
        ('Dependent competent A', [0,12/64,24/64,28/64]),
        ('Dependent competent B', [4/64,0,36/64,24/64]),
    ]
    counterexample=[dict(name=name,q=q,**exchangeable_moments(q)) for name,q in families]
    # Independent Bernoulli errors with probabilities .1, .3, .5.
    s=np.diag([.09,.21,.25]); w=constrained_weights(s)
    v,ess=covariance_variance(w,s,.09)
    # Positive definite matrix whose unconstrained optimum has a negative component.
    r=np.array([[1,.75,.75],[.75,1,.3],[.75,.3,1]])
    u=constrained_weights(r)
    unconstrained=np.linalg.solve(r,np.ones(3));unconstrained/=unconstrained.sum()
    t=synthetic_tape(4000,53,'test')
    errors=t.light[:,0]!=t.labels[:,0,None]
    route=np.abs(2*t.light[:,0].sum(1)-3)==1
    full=conditional_errors(errors,np.ones(len(errors),bool))
    routed=conditional_errors(errors,route)
    weights,_=fit(synthetic_tape(1000,51,'cal'))
    menu=candidates(weights)
    x=execute(next(p for p in menu if p.name=='shared+shared'),t)
    y=execute(next(p for p in menu if p.name=='single+single'),t)
    # Already-declared comparison; descriptive paired IID intervals.
    boot=[paired_bootstrap(x.verdict[:,i]!=t.labels[:,i],y.verdict[:,i]!=t.labels[:,i],seed=2026+i) for i in range(2)]
    return dict(counterexample=counterexample,covariance=dict(weights=w.tolist(),variance=v,reference_variance=.09,ess=ess,uniform_variance=float(np.ones(3)@s@np.ones(3)/9)),constrained=dict(weights=u.tolist(),variance=float(u@r@u),unconstrained_weights=unconstrained.tolist(),uniform_variance=float(np.ones(3)@r@np.ones(3)/9)),routing=dict(full=full,routed=routed),bootstrap=boot)


def report(d):
    lines=['# Final research outcomes — QUORUM-D', '',
    'Companion to the QUORUM-D narrative critical review. Analytical and synthetic evidence only; no real LLM calls, paid API expenditure or independent replication of cited studies. Earlier results are in [validation.md](validation.md); claim mapping is in [claims.md](claims.md). The reference pipeline remains a restricted demonstration, not empirical validation.', '',
    '## 1. Existing reproducibility results', '',
    'The initial package implements Equations 1–5 and reproduces the numerical illustrations of Figures 4–6 and all five Table 6 rows. The original synthetic common-shock, calibration sensitivity and finite-menu demonstrations remain unchanged. Run the verification command below to compare regenerated outputs with archived numerical values.', '',
    '## 2. Identical ESS, different majority accuracy (exact construction)', '',
    '| Distribution | Marginal correctness | Pairwise correlation | ESS | Majority accuracy |', '|---|---:|---:|---:|---:|']
    for a in d['counterexample']:
        lines.append(f"| {a['name']} | {a['p']:.3f} | {a['rho']:.3f} | {a['ess']:.3f} | {a['majority']:.5f} |")
    lines += ['', 'Let K count correct votes among three judges. Given K, choose a uniformly random subset of K judges. Thus p=E[K]/3, joint pairwise correctness=E[K(K−1)]/6, correlation=(joint−p²)/(p(1−p)), and majority accuracy=P(K≥2). The fair distributions over K=0,1,2,3 are (1,3,3,1)/8, (1,0,3,0)/4 and (0,3,0,1)/4. The competent distributions are (1,9,27,27)/64, (0,12,24,28)/64 and (4,0,36,24)/64. Each group shares first and second moments but not its majority tail. Zero pairwise correlation is not mutual independence. This is an exact counterexample, not a simulation or a claim about real judges. The three competent distributions appear in Section 4.2 and Table 5 of the manuscript.', '',
    '## 3. Full covariance and nonnegative weighting (analytical)', '',
    'Independent Bernoulli error probabilities 0.1, 0.3, 0.5 imply variances 0.09, 0.21, 0.25. The reference variance is explicitly 0.09; the resulting reference-normalized size depends on that choice and is not the equal-variance ESS.', '',
    f"Optimal weights: {[round(x,8) for x in d['covariance']['weights']]}; variance {d['covariance']['variance']:.8f}; uniform variance {d['covariance']['uniform_variance']:.8f}; reference ESS {d['covariance']['ess']:.6f}.",
    f"Positive definite correlation example with entries R12=R13=0.75, R23=0.3: unconstrained weights {[round(x,8) for x in d['constrained']['unconstrained_weights']]}; constrained weights {[round(x,8) for x in d['constrained']['weights']]}, variance {d['constrained']['variance']:.6f} versus uniform variance {d['constrained']['uniform_variance']:.6f}. This is a covariance-matrix example, not an asserted jointly feasible Bernoulli model. Small-panel active-face enumeration covers every nonempty face for positive definite matrices of at most 12 judges. It is not a scalable solver. Lower variance does not imply lower decision error.", '',
    '## 4. Selective routing (synthetic)', '',
    '| Subset | Jointly evaluated items | Mean off-diagonal error correlation | Error rates |', '|---|---:|---:|---|']
    for name in ('full','routed'):
        r=d['routing'][name];a=np.asarray(r['correlation']);mean=a[np.triu_indices(3,1)].mean()
        lines.append(f"| {name} | {r['n']} | {mean:.6f} | {', '.join(f'{x:.6f}' for x in r['rates'])} |")
    lines += ['', 'Routing uses only observable one-vote margins of the three lightweight binary judgments, not reference labels. Seed 53, dimension 1 of the existing 4,000-item reference tape. Full and routed pairwise matrices are archived in JSON. Conditional correlations describe the jointly observed routed subset, not the full workload. The negative routed correlations are not evidence that the original judges are independent or that the routing rule improves accuracy. Supports the paper’s conditional-dependence reporting safeguard.', '',
    '## 5. Paired uncertainty (synthetic)', '',
    '| Dimension | Shared minus separate single-judge error | 95% percentile interval |', '|---|---:|---:|']
    for i,b in enumerate(d['bootstrap'],1):
        lines.append(f"| {i} | {b['mean']:.6f} | [{b['lower']:.6f}, {b['upper']:.6f}] |")
    lines += ['', 'Paired IID bootstrap of 4,000 synthetic items, 2,000 draws, seeds 2026 and 2027; same pre-existing synthetic comparison, no new policy selection. Positive differences mean shared is worse. These are descriptive pointwise percentile intervals, no multiple-comparison adjustment or population-level risk guarantee. Cluster resampling helper tested separately; the example is IID.', '',
    '## 6. Reproduction and interpretation', '',
    'Run `python -m scripts.strengthen` and `python -m pytest -q`. Run `python -m scripts.verify_archive` to independently regenerate and verify the archived numerical files. Numerical outputs: `results/strengthening.json`. The results establish neither empirical superiority, actual cost savings, nor complete implementation of Algorithm 1.', '']
    return '\n'.join(lines)


def main():
    d=run();out=Path('results');out.mkdir(exist_ok=True)
    (out/'strengthening.json').write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
    Path('docs/FINAL_RESEARCH_OUTCOMES.md').write_text(report(d))

if __name__=='__main__':main()
