import re
import os
import datetime
import pdb

is_nightly = 1
def get_version():
    path = os.path.dirname(__file__)
    version_re = re.compile(r'''__version__ = ['"](.+)['"]''')
    with open(os.path.join(path, 'fastestimator', '__init__.py')) as f:
        init = f.read()
    
    now = datetime.datetime.now()
    version = version_re.search(init).group(1)

    if is_nightly:
        return "{}.dev{}{:02}{:02}{:02}{:02}".format(version, now.year, 1, 1, 1, 0)
    else:
        return version

