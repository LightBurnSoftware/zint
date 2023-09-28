import os
from pathlib import Path
import sys

workspace = sys.argv[1]

CMakeLists = Path(f'{workspace}/CMakeLists.txt').absolute()

ver_start = 'set(ZINT_VERSION_'
fields = ['MAJOR', 'MINOR', 'RELEASE', 'BUILD']
results = {}
with open(CMakeLists, 'r') as f:
    for line in f.readlines():
        if line.startswith(ver_start):
            for sub in fields:
                sub_start = f'{ver_start}{sub}'
                if line.startswith(sub_start):
                    start = line.index(' ')
                    end = line.index(')')
                    results[sub] = line[start+1:end]
                    
MAJOR =     results.get('MAJOR', '0')
MINOR =     results.get('MINOR', '0')
RELEASE =   results.get('RELEASE', '0')
BUILD =     results.get('BUILD', '0')

ver_str = f'{MAJOR}.{MINOR}.{RELEASE}.{BUILD}'

print(f'Build version {ver_str}')

github_env_path = os.environ.get("GITHUB_ENV")
if github_env_path is not None:
    print(f"GITHUB_ENV environment variable is set to {github_env_path}, writing version to it")
    with Path(github_env_path).open('a') as fh:
        fh.write(f"build_version={ver_str}")
                    
