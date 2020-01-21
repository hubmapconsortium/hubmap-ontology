#!/bin/bash

mkdir -p docs

python3 src/ccf_model.py
python3 src/ccf_partonomy.py
python3 src/ccf_full.py
