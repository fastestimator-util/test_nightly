#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" # /home/ubuntu/test_nightly/test
path_tutorial=${DIR}'/../tutorial/' # /home/ubuntu/test_nightly/tutorial
path_temp=$(dirname $(mktemp -u))/ # /tmp

filename_abs=$path_tutorial't10_unpaired_dataset.ipynb'
fname=t11_interpretation

echo ${path_temp}${fname}
jupyter nbconvert --to script ${filename_abs} --output ${path_temp}${fname}
if ipython ${path_temp}${fname}'.py'; then
    exit 0
else
    exit 1
fi

