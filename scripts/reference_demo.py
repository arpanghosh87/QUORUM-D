"""Run the complete fixed-menu synthetic calibration/development/test demonstration."""
import json
from pathlib import Path
from quorum_d.policy import Limits
from quorum_d.reference import synthetic_tape, run_reference


def run():
    return run_reference(synthetic_tape(1000,51,'cal'),synthetic_tape(4000,52,'dev'),
                         synthetic_tape(4000,53,'test'),
                         Limits(.046,2,.95,(.17,.19),(.15,.15)),37,.001)


if __name__=='__main__':
    p=Path('results');p.mkdir(exist_ok=True)
    r=run();(p/'reference_demo.json').write_text(json.dumps(r,indent=2,allow_nan=False))
    print(r['decision'],r.get('selected'),len(r['development']))
