import numpy as np
import pytest
from quorum_d.research_checks import (exchangeable_moments, covariance_variance,
    constrained_weights, conditional_errors, paired_bootstrap)
from scripts.strengthen import run

@pytest.fixture(scope='module')
def results():
    return run()

def test_counterexample(results):
    a,b,c,d,e,f=results['counterexample']
    for x in (a,b,c):
        assert x['p']==.5 and x['rho']==0 and x['ess']==3
    assert [x['majority'] for x in (a,b,c)]==[.5,.75,.25]
    for x in (d,e,f):
        assert x['p']==.75 and x['rho']==0 and x['ess']==3
    assert [x['majority'] for x in (d,e,f)]==[54/64,52/64,60/64]
    with pytest.raises(ValueError): exchangeable_moments([0,1,0,0])

def test_covariance():
    s=np.diag([.09,.21,.25]);w=constrained_weights(s)
    expected=1/s.diagonal();expected/=expected.sum()
    assert np.allclose(w,expected)
    v,ess=covariance_variance(w,s,.09)
    assert ess==pytest.approx(.09/v)
    assert v<np.ones(3)@s@np.ones(3)/9
    assert covariance_variance(2*w,s,.09)==pytest.approx((v,ess))
    with pytest.raises(ValueError): covariance_variance(w,s,0)

def test_boundary():
    r=np.array([[1,.75,.75],[.75,1,.3],[.75,.3,1]])
    assert np.allclose(constrained_weights(r),[0,.5,.5])
    with pytest.raises(ValueError): constrained_weights(np.ones((2,2)))

def test_routing(results):
    r=results['routing']
    assert 0<r['routed']['n']<r['full']['n']
    assert r['routed']['correlation']!=r['full']['correlation']
    assert conditional_errors([[0,0],[1,0]],np.array([True,True]))['correlation'][0][1] is None
    assert conditional_errors([[0,0],[1,0]],np.array([False,False]))['n']==0

def test_bootstrap(results):
    a=np.array([1,2,3,4]);b=a-1
    for clusters in (None,[0,0,1,1]):
        r=paired_bootstrap(a,b,reps=100,clusters=clusters)
        assert r['lower']==r['upper']==r['mean']==1
    for r in results['bootstrap']:
        assert r['lower']<r['mean']<r['upper'] and r['units']==4000
    assert paired_bootstrap(a,b,reps=100)==paired_bootstrap(a,b,reps=100)


def test_archive_comparison():
    from scripts.verify_archive import compare
    compare({'x':[1.0,True,'a']},{'x':[1.0+1e-13,True,'a']},'test')
    with pytest.raises(AssertionError): compare([1.0],[1.01],'test')
    with pytest.raises(AssertionError): compare([True],[1],'test')
    with pytest.raises(AssertionError): compare([1],[1,2],'test')
    with pytest.raises(AssertionError): compare({'a':1},{'b':1},'test')


def test_heldout_rejection_and_uncertainty():
    from quorum_d.policy import Limits, Outcome, held_out, select
    labels=np.zeros((100,1),int)
    limits=Limits(.1,2,1,(.2,),(.2,))
    def outcome(name,prefix,errors):
        votes=labels.copy();votes[:errors]=1
        return Outcome(name,1,tuple(f'{prefix}-{i}' for i in range(100)),labels,votes,np.full(100,.02),np.ones(100))
    d=outcome('frozen','dev',0)
    chosen,_=select([d],limits,1)
    assert chosen['name']=='frozen'
    assert held_out(chosen,d.ids,[outcome('frozen','test',0)],limits)['decision']=='deploy_candidate'
    assert held_out(chosen,d.ids,[outcome('frozen','test',40)],limits)['decision']=='do_not_deploy'
    assert held_out(chosen,d.ids,[outcome('frozen','test',20)],limits)['decision']=='defer'
    with pytest.raises(ValueError,match='frozen policy missing'):
        held_out(chosen,d.ids,[outcome('other','test',0)],limits)
