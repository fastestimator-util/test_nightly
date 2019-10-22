import re
import os
import datetime
import pdb

def get_version(is_nightly):
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'fastestimator', '__init__.py')) as f:
        init = f.read()

    if is_nightly:
        version_re = re.compile(r'''__version__ = ['"](.+)[-](.+)['"]''')
        now = datetime.datetime.now()
        return "{}-{}{}{}".format(version_re.search(init).group(1), now.year, now.month, now.day)
    else:
        version_re = re.compile(r'''__version__ = ['"](.+)['"]''')
        return version_re.search(init).group(1)

print(get_version(0))