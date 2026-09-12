#!/usr/bin/env python3
"""Compatibility entry; the shared curator owns the runtime."""
import importlib.util
import sys
from pathlib import Path
runtime = Path(__file__).resolve().parents[2] / 'zane-workbench-curator/scripts/workbench.py'
spec = importlib.util.spec_from_file_location('zane_shared_runtime', runtime)
module = importlib.util.module_from_spec(spec)
prior_bytecode = sys.dont_write_bytecode
sys.dont_write_bytecode = True
try:
    spec.loader.exec_module(module)
finally:
    sys.dont_write_bytecode = prior_bytecode
globals().update({key: value for key, value in vars(module).items() if not key.startswith('_')})
if __name__ == '__main__':
    main()
