
# -*- coding: utf-8 -*-
import os, sys
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
backend_dir = os.path.join(base_dir, 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from scheduler import run_daily_job

if __name__ == '__main__':
    print('Starting daily morning sync and notifications...')
    results = run_daily_job()
    print('Finished! Results:', results)
