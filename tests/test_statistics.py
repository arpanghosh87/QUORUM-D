from itertools import product
import numpy as np
import pytest
from quorum_d import *
from scripts.reproduce import table_rows, mixed_correlation


def test_majority():
    assert majority_accuracy(9,.4) == pytest.approx(.26656768)
    assert majority_accuracy(9,.7) > majority_accuracy(7,.7) > .7
    assert majority_accuracy(9,.5) == pytest.approx(.5)
    with pytest.raises(ValueError): majority_accuracy(4,.7)


def test_effective_size():
    assert effective_size(9,.391) == pytest.approx(2.18,abs=.005)
    assert effective_size(10,.206) == pytest.approx(3.50385424)
    assert effective_size(5,0) == 5
    assert effective_size(5,1) == 1
    assert np.isinf(effective_size(5,-.25))
    with pytest.raises(ValueError): effective_size(5,-.3)


def test_weighted():
    r=mixed_correlation(.2); w=minimum_variance_weights(r)
    assert w.sum() == pytest.approx(1)
    assert weighted_effective_size(w,r) >= weighted_effective_size(np.ones(5),r)
    assert weighted_effective_size(3*w,r) == pytest.approx(weighted_effective_size(w,r))
    with pytest.raises(ValueError): weighted_effective_size([1,1],[[1,2],[2,1]])
    with pytest.raises(ValueError): minimum_variance_weights(np.ones((2,2)))


def test_table5():
    expected=[(1.290,1.290,.0155,.0155),(1.866,2.290,.0375,.0306),(1.667,1.871,.0420,.0374),(1.506,1.585,.0465,.0442),(1.374,1.386,.0510,.0505)]
    for row, target in zip(table_rows(),expected,strict=True):
        assert np.allclose(row[3:5],target[:2],atol=.00051,rtol=0)
        assert np.allclose(row[5:],target[2:],atol=.000051,rtol=0)


def test_vote_and_objective():
    assert weighted_vote([1,0],[1,1],1) == 1
    assert weighted_vote([1,0],[1,2],1.5) == 0
    assert policy_objective(10,20,5,[2,3],[4,1]) == 46
    with pytest.raises(ValueError): weighted_vote([1,-1],[1,1],1)


def test_binary_construction():
    e=correlated_errors(200000,.25,[np.sqrt(.7)]*4+[.4/np.sqrt(.7)])
    s=error_statistics(e,np.zeros(len(e)))
    assert np.allclose(s['error_rate'],.25,atol=.005)
    assert np.allclose(s['correlation'],mixed_correlation(.4),atol=.015)
    assert s['n_items']==200000
    assert np.isnan(error_statistics([[1,0],[1,1]],[0,0])['correlation'][0,0])


def test_pivotal_exhaustive():
    for n in (1,3,5,7,9):
        for b in product((0,1),repeat=n):
            before=sum(b)>n//2
            can_flip=any((sum(b)+1-2*x>n//2)!=before for x in b)
            assert pivotal(b)==can_flip
