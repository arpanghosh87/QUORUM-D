"""Synthetic end-to-end example. All model competence and prices are assumed."""
import json
from pathlib import Path
import numpy as np
from quorum_d.policy import Outcome, Limits, select, held_out
from quorum_d.statistics import correlated_errors


def generate(n, seed, prefix):
    rng=np.random.default_rng(seed)
    reference=rng.integers(0,2,(n,2))
    # Separate simulated calls per dimension; shared calls use a distinct error model.
    light=np.stack([correlated_errors(n,.22,[.7]*3,seed+i+10) for i in range(2)],1)
    strong=(rng.random((n,2))<np.array([.10,.18])).astype(int)
    verifier=(rng.random((n,2))<np.array([.06,.09])).astype(int)
    ballots=reference[:,:,None]^light
    majority=(ballots.sum(2)>=2).astype(int)
    direct=reference^verifier
    strong_vote=reference^strong
    # Observable one-vote margin; references never enter routing.
    route=np.abs(2*ballots.sum(2)-3)==1
    selective=np.where(route,direct,majority)
    shared=reference^(rng.random((n,2))<np.array([.12,.14]))
    ids=tuple(f'{prefix}-{i}' for i in range(n))
    def out(name,complexity,y,c,l):
        return Outcome(name,complexity,ids,reference,y,np.broadcast_to(c,(n,)).copy(),np.broadcast_to(l,(n,)).copy())
    return [out('single_separate',2,strong_vote,.04,1.0),out('panel',6,majority,.03,1.2),
            out('verifier_only',2,direct,.05,1.5),
            out('selective',8,selective,.03+.025*route.sum(1),1.2+.8*route.any(1)),
            out('single_shared',1,shared,.025,1.1)]


def run():
    limits=Limits(cost=.045,latency=2,coverage=.95,risk=(.17,.19),loss_prices=(.15,.15))
    dev=generate(4000,35,'dev'); test=generate(4000,36,'test')
    selected,reports=select(dev,limits,5)
    result=held_out(selected,dev[0].ids,test,limits)
    result.update({'development':reports,'assumptions':'Synthetic IID items, two binary dimensions, assumed costs and error rates; no empirical LLM results.', 'limits':limits.__dict__})
    return result


if __name__=='__main__':
    p=Path('results'); p.mkdir(exist_ok=True)
    result=run(); (p/'policy_demo.json').write_text(json.dumps(result,indent=2,allow_nan=False))
    print(json.dumps(result,indent=2,allow_nan=False))
