#!/bin/bash
source ${1:-venv}/bin/activate
python contentcompiler/contentcompiler.py
deactivate
