"""Render the full policy selection report from generated reference_demo.json."""
import json
from pathlib import Path
import argparse

INTRO = "Analytical/synthetic companion only. All prices, latency and judge performance are assumed. Calibration/development/test seeds 51/52/53; item counts 1,000/4,000/4,000. The fixed menu has 37 candidates. Budget 0.046 USD/item, p95 latency <=2 s, per-dimension coverage >=0.95, accepted-case Wilson upper risk <=0.17/0.19 (z=1.96); loss prices 0.15 per dimension, deferral loss 0.5, amortized calibration 0.001 USD/item. The objective uses all-item loss including deferral, not accepted-case risk alone. Risk and coverage are proportions. Values are rounded for presentation; feasibility and violated criteria use unrounded values. These are descriptive selection diagnostics, not simultaneous guarantees.\n\n"
HEADER = "# Full synthetic policy-selection results\n\n"
TABLE_HEADER = "| Policy | Cost/item | p95 s | Coverage D1 | Coverage D2 | Error D1 | Error D2 | Wilson upper D1 | Wilson upper D2 | Objective | Feasible | Violated criteria |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|"
def violations(r):
    a=[]
    if r['cost']>.046: a.append('budget')
    if r['p95_latency']>2: a.append('latency')
    for i,v in enumerate(r['coverage'],1):
        if v<.95: a.append(f'coverage D{i}')
    for i,(v,lim) in enumerate(zip(r['risk_intervals'],(.17,.19)),1):
        if v[1]>lim: a.append(f'risk D{i}')
    return '; '.join(a) or 'none'

def table(rows):
    lines=[TABLE_HEADER]
    for r in rows:
        cols=[r['name'],f"{r['cost']:.8f}",f"{r['p95_latency']:.1f}",
              *[f'{x:.5f}' for x in r['coverage']],
              *[f'{x:.5f}' for x in r['accepted_risk']],
              *[f'{x[1]:.5f}' for x in r['risk_intervals']],
              f"{r['objective']:.8f}",str(r['feasible']),violations(r)]
        lines.append('| '+' | '.join(cols)+' |')
    return '\n'.join(lines)

def render(d):
    feasible=[r['name'] for r in d['development'] if r['feasible']]
    return (HEADER+INTRO+'## Development — all 37 configurations\n\n'+table(d['development'])
        +f"\n\nDevelopment feasible ({len(feasible)}): {', '.join(feasible)}. Selected: {d['selected']}. Selection minimizes the declared objective among feasible candidates, with complexity and name as tie breakers.\n\n"
        +'## Held-out — frozen selected configuration and declared baselines\n\n'+table(d['reports'])
        +f"\n\nDecision: {d['decision']} (synthetic only). Three held-out configurations are feasible; this is distinct from the four development-feasible policies. Development-feasible alternatives not designated as held-out baselines were not retested. No selection from held-out results. The verifier-only configuration violates budget; uniform and competence-weighted panels violate both critical risk limits. A failed feasibility check is not always a statistically established violation: uncertainty can make a policy inconclusive.\n")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=Path('results/reference_demo.json'))
    p.add_argument('--output',type=Path,default=Path('docs/POLICY_SELECTION_RESULTS.md'))
    a=p.parse_args()
    a.output.write_text(render(json.loads(a.input.read_text())),encoding='utf-8')

if __name__=='__main__':main()
