"""Export archived publication SVGs to PDF and 600 dpi PNG (optional CairoSVG)."""
from pathlib import Path
import argparse
import cairosvg

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=Path('results/figures'))
    p.add_argument('--output',type=Path,default=Path('results/figure_exports'))
    a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True)
    for svg in sorted(a.source.glob('*.svg')):
        cairosvg.svg2pdf(url=str(svg),write_to=str(a.output/(svg.stem+'.pdf')))
        cairosvg.svg2png(url=str(svg),write_to=str(a.output/(svg.stem+'.png')),dpi=600)

if __name__=='__main__':main()
