"""Reproduce Rev34 Figures 3–5 and Table 5; no model calls or empirical claims."""
import argparse
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from quorum_d import effective_size, weighted_effective_size, minimum_variance_weights, cost_per_effective_unit, correlated_errors, error_statistics


def mixed_correlation(r):
    matrix = np.full((5, 5), .7)
    matrix[4, :4] = matrix[:4, 4] = r
    np.fill_diagonal(matrix, 1)
    return matrix


def table_rows():
    for name, r, cost, matrix in [('4 light only', None, .02, .3*np.eye(4)+.7*np.ones((4,4)))] + [('1 frontier + 4 light', r, .07, mixed_correlation(r)) for r in (0., .2, .4, .6)]:
        a = weighted_effective_size(np.ones(len(matrix)), matrix)
        b = weighted_effective_size(minimum_variance_weights(matrix), matrix)
        yield name, r, cost, a, b, cost_per_effective_unit(cost,a), cost_per_effective_unit(cost,b)


def reproduce(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    n = np.arange(1, 22, 2)
    for filename, curves in [('figure3', [(f'rho = {r}', r) for r in (0,.1,.3,.5,.8)]), ('figure4', [('Correctness',.6),('Faithfulness',.2),('Relevance',.3),('Helpfulness',.45),('Task completion',.1)])]:
        fig, ax = plt.subplots(figsize=(7,4), layout='constrained')
        for label, rho in curves:
            ax.plot(n, [effective_size(int(k),rho) for k in n], marker='o', label=f'{label} ({rho})' if filename == 'figure4' else label)
        ax.set(xlabel='Nominal panel size, N', ylabel='Variance-equivalent size', xticks=n, ylim=(0,None))
        ax.legend(); ax.grid(alpha=.2)
        fig.savefig(out/f'{filename}.svg'); plt.close(fig)
    fig, (a,b) = plt.subplots(1,2,figsize=(10,4),layout='constrained')
    rho = np.linspace(0,.8,81)
    for k in (3,5,9):
        a.plot(rho,[.01*k/effective_size(k,r) for r in rho],label=f'N = {k}')
    r = np.linspace(0,.6,61)
    for label, weights in [('Uniform',lambda m: np.ones(5)), ('Minimum variance',minimum_variance_weights)]:
        b.plot(r,[.07/weighted_effective_size(weights(mixed_correlation(x)),mixed_correlation(x)) for x in r],label=label)
    for ax, title, xlabel in [(a,'Equal-cost panels ($0.01/judge)','Common error correlation'),(b,'Mixed panel ($0.07 total)','Cross-tier error correlation')]:
        ax.set(title=title,xlabel=xlabel,ylabel='USD per variance-equivalent unit'); ax.legend(); ax.grid(alpha=.2)
    fig.savefig(out/'figure5.svg'); plt.close(fig)
    with (out/'table5.csv').open('w',newline='') as f:
        writer=csv.writer(f); writer.writerow(['panel','cross_tier_r','cost','ess_uniform','ess_minvar','ceff_uniform','ceff_minvar']); writer.writerows(table_rows())
    e = correlated_errors(200000,.25,[np.sqrt(.7)]*4+[.4/np.sqrt(.7)])
    stats = error_statistics(e,np.zeros(len(e)))
    np.savetxt(out/'synthetic_correlation.csv',stats['correlation'],delimiter=',')
    print('Generated analytical figures/table and synthetic correlations in',out)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--output',default='results'); reproduce(parser.parse_args().output)
