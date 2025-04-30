#!/bin/bash
source ${1:-venv}/bin/activate

python -c "import frontmatter" &>/dev/null
if [ $(echo $?) = 1 ]; then
    echo "frontmatter was not installed, installing now"
    pip install python-frontmatter
fi
python -c "import feedgen" &>/dev/null
if [ $(echo $?) = 1 ]; then
    echo "feedgen was not installed, installing now"
    pip install feedgen
fi

python contentcompiler/contentcompiler.py
deactivate
