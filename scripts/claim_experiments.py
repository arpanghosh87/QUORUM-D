"""Reproducible synthetic experiments; not real LLM evidence."""
import csv
from pathlib import Path
import numpy as np
from quorum_d import majority_accuracy, effective_size, correlated_errors
from quorum_d.statistics import minimum_variance_weights, weighted_effective_size


def run(out='results'):
    out=Path(out); out.mkdir(exist_ok=True)
    rng=np.random.default_rng(2026)
    rows=[]
    n_items=200000
    for p in (.4,.75):
        for rho in (0.,.4,.8):
            for n in (1,3,5,9):
                shared=rng.random(n_items)<rho
                common=rng.random(n_items)<p
                independent=(rng.random((n_items,n))<p).sum(1)>n//2
                observed=np.where(shared,common,independent).mean()
                expected=rho*p+(1-rho)*majority_accuracy(n,p)
                rows.append([p,rho,n,expected,observed,abs(expected-observed),effective_size(n,rho)])
    with (out/'majority_simulation.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['competence','rho','n','theoretical_accuracy','simulated_accuracy','absolute_difference','ess']);w.writerows(rows)
    # Fixed known equal-variance synthetic model, disjoint calibration and test items.
    q=[np.sqrt(.7)]*4+[.2/np.sqrt(.7)]
    test=correlated_errors(100000,.25,q,seed=7000)
    r=np.corrcoef(test,rowvar=False); rows2=[]
    for size in (25,100,500,2000):
        scores=[]; failed=0
        for rep in range(50):
            cal=correlated_errors(size,.25,q,seed=10000+size*100+rep)
            if (cal.std(0)==0).any(): failed+=1;continue
            est=np.corrcoef(cal,rowvar=False)
            # Fixed shrinkage toward identity, chosen before generating data.
            est=.9*est+.1*np.eye(5)
            try: weights=minimum_variance_weights(est)
            except ValueError: failed+=1;continue
            scores.append(weighted_effective_size(weights,r))
        rows2.append([size,len(scores),failed,float(np.mean(scores)) if scores else '',float(np.std(scores,ddof=1)) if len(scores)>1 else ''])
    with (out/'calibration_sensitivity.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['calibration_items','successful_fits','failed_fits','mean_test_ess','sd_test_ess']);w.writerows(rows2)
    print('Max absolute simulation difference:',max(r[5] for r in rows))
    print('Calibration sensitivity:',rows2)


if __name__=='__main__':run()
