import os
import re
import sys
import argparse
import datetime
from setuptools import find_packages, setup

# Create a environment variable to specify whether it is nightly build
environment_variable_name = 'FASTESTIMATOR_IS_NIGHTLY'
environment_variable_value = os.environ.get(environment_variable_name, None)

if environment_variable_value is not None:
    sys.stderr.write("Using '{}={}' environment variable!\n".format( \
            environment_variable_name, environment_variable_value))

def get_version(is_nightly):
    path = os.path.dirname(__file__)
    version_re = re.compile(r'''__version__ = ['"](.+)['"]''')
    with open(os.path.join(path, 'fastestimator', '__init__.py')) as f:
        init = f.read()
    if is_nightly:
        now = datetime.datetime.now()
        return "{}-{}{}{}".format(version_re.search(init).group(1), now.year, now.month, now.day)
    else:
        return version_re.search(init).group(1)

def get_name(is_nightly):
    if is_nightly:
        return "fastestimator-nightly"
    else:
        return "fastestimator"

setup(
    name=get_name(environment_variable_value) ,
    version=get_version(environment_variable_value),
    description="Deep learning Application framework",
    packages=find_packages(),
    package_dir={'': '.'},
    long_description="FastEstimator is a high-level deep learning API. With the help of FastEstimator, you can easily \
                    build a high-performance deep learning model and run it anywhere.",
    author="FastEstimator Dev",
    url='https://github.com/fastestimator/fastestimator',
    license="Apache License 2.0",
    keywords="fastestimator tensorflow",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3", ],

    # Declare minimal set for installation
    install_requires=[
        'numpy',
        'pyfiglet',
        'pandas',
        'pillow',
        'sklearn',
        'wget',
        'matplotlib',
        'seaborn>= 0.9.0',
        'scipy',
        'pytest',
        'pytest-cov',
        'tensorflow-probability',
        'umap-learn',
        'tqdm',
        'opencv-python',
        'papermill',
        'tf-explain'
    ],
    # Declare extra set for installation
    extras_require={},
    scripts=['bin/fastestimator'])
