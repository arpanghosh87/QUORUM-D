import numpy as np
import pytest
from quorum_d.policy import Outcome, Limits, select, held_out, measure
from scripts.policy_demo import generate, run


def test_demo():
    r=run()
    assert r['selected']=='single_shared'
    assert r['decision']=='deploy_candidate'
    assert len(r['reports'])==5
    assert next(x for x in r['reports'] if x['name']=='single_shared')['paired_loss_difference']==[0,0]


def test_exhausted_and_leakage():
    d=generate(1000,2,'dev')
    l=Limits(.001,2,1,(.5,.5),(1,1))
    selected,reports=select(d,l,2)
    assert selected is None and len(reports)==2
    assert held_out(None,d[0].ids,[],l)['decision']=='no_automation'
    l=Limits(1,10,1,(.5,.5),(1,1))
    selected,_=select(d,l,5)
    with pytest.raises(ValueError,match='leakage'): held_out(selected,d[0].ids,d,l)


def test_conditional_risk_and_deferral():
    t=np.zeros((100,1),int); y=np.full_like(t,-1); y[:10]=1
    o=Outcome('a',1,tuple(range(100)),t,y,np.zeros(100),np.zeros(100))
    m=measure(o,Limits(1,1,.1,(.2,),(1,)))
    assert m['accepted_risk']==[1] and m['all_item_error']==[.1]
    assert not m['feasible']


def test_unpaired():
    a,b=generate(20,1,'a'),generate(20,2,'b')
    with pytest.raises(ValueError,match='identical'): select([a[0],b[1]],Limits(1,2,0,(1,1),(1,1)),2)
