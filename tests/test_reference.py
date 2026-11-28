import numpy as np
import pytest
from quorum_d.policy import Limits
from quorum_d.reference import synthetic_tape, fit, candidates, execute, run_reference
from scripts.reference_demo import run


def test_frozen_reference():
    r=run()
    assert len(r['development'])==37
    assert r['frozen']['weights']==r['weights']
    assert r['selected'] in {x['name'] for x in r['reports']}
    assert all(abs(sum(w)-1)<1e-10 for w in r['weights'])
    assert r['decision'] in ('deploy_candidate','do_not_deploy','defer')


def test_shared_accounting_and_independent_execution():
    tape=synthetic_tape(100,11,'test'); w,_=fit(tape)
    menu=candidates(w)
    shared=execute(menu[-1],tape)
    separate=execute(menu[0],tape)
    assert np.allclose(shared.cost,.025) and np.allclose(separate.cost,.04)
    assert np.array_equal(shared.verdict,tape.shared)
    assert np.array_equal(separate.verdict,tape.strong)


def test_split_and_search_limit():
    cal=synthetic_tape(100,11,'cal'); dev=synthetic_tape(100,12,'dev'); test=synthetic_tape(100,13,'test')
    limits=Limits(.001,2,1,(.5,.5),(1,1))
    with pytest.raises(ValueError,match='leakage'): run_reference(cal,dev,cal,limits,1)
    r=run_reference(cal,dev,test,limits,2)
    assert r['decision']=='no_automation' and len(r['development'])==2
