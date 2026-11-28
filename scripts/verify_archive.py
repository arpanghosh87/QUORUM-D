"""Regenerate in a temporary directory; never overwrite committed snapshots."""
import csv
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ATOL, RTOL = 1e-12, 1e-9


def compare(expected, actual, where):
    if isinstance(expected, dict) and isinstance(actual, dict):
        if expected.keys() != actual.keys():
            raise AssertionError(f'{where}: different keys')
        for key in expected:
            compare(expected[key], actual[key], f'{where}.{key}')
    elif isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            raise AssertionError(f'{where}: different lengths')
        for i,(a,b) in enumerate(zip(expected,actual)):
            compare(a,b,f'{where}[{i}]')
    elif isinstance(expected,bool) or isinstance(actual,bool):
        if type(expected) is not type(actual) or expected != actual:
            raise AssertionError(f'{where}: {expected!r} != {actual!r}')
    elif isinstance(expected,(int,float)) and isinstance(actual,(int,float)):
        if not math.isfinite(expected) or not math.isfinite(actual) or not math.isclose(expected,actual,abs_tol=ATOL,rel_tol=RTOL):
            raise AssertionError(f'{where}: {expected!r} != {actual!r}')
    else:
        if type(expected) is not type(actual) or expected != actual:
            raise AssertionError(f'{where}: {expected!r} != {actual!r}')


def read_csv(path):
    def cell(x):
        try: return float(x)
        except ValueError: return x
    with path.open(newline='') as f:
        return [[cell(x) for x in row] for row in csv.reader(f)]


def reference_rows(path):
    data=json.loads(path.read_text())
    header=['policy','cost','p95_latency','coverage_1','coverage_2','accepted_risk_1','accepted_risk_2','objective','feasible']
    return [header]+[[r['name'],r['cost'],r['p95_latency'],*r['coverage'],*r['accepted_risk'],r['objective'],str(r['feasible']).lower()] for r in data['reports']]


def verify():
    env=os.environ.copy()
    env['PYTHONPATH']=str(ROOT)+os.pathsep+env.get('PYTHONPATH','')
    with tempfile.TemporaryDirectory(prefix='quorum-reproduce-') as tmp:
        work=Path(tmp); (work/'docs').mkdir()
        for module in ('reproduce','claim_experiments','reference_demo','strengthen','archive_policy_report'):
            subprocess.run([sys.executable,'-m',f'scripts.{module}'],cwd=work,env=env,check=True,stdout=subprocess.DEVNULL)
        for name in ('table5.csv','majority_simulation.csv','calibration_sensitivity.csv','synthetic_correlation.csv'):
            compare(read_csv(ROOT/'results'/name),read_csv(work/'results'/name),name)
            print(f'PASS {name}')
        compare(read_csv(ROOT/'results/reference_heldout.csv'),reference_rows(work/'results/reference_demo.json'),'reference_heldout.csv')
        print('PASS reference_heldout.csv')
        compare(json.loads((ROOT/'results/strengthening.json').read_text()),json.loads((work/'results/strengthening.json').read_text()),'strengthening.json')
        print('PASS strengthening.json')
        compare((ROOT/'docs/FINAL_RESEARCH_OUTCOMES.md').read_text(),(work/'docs/FINAL_RESEARCH_OUTCOMES.md').read_text(),'FINAL_RESEARCH_OUTCOMES.md')
        print('PASS FINAL_RESEARCH_OUTCOMES.md')
        compare((ROOT/'docs/POLICY_SELECTION_RESULTS.md').read_text(),(work/'docs/POLICY_SELECTION_RESULTS.md').read_text(),'POLICY_SELECTION_RESULTS.md')
        print('PASS POLICY_SELECTION_RESULTS.md')
    print('All 8 archived artifacts reproduced (numeric tolerance: atol=1e-12, rtol=1e-9).')

if __name__=='__main__':verify()
