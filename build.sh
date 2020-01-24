#!/bin/bash

mkdir -p dist

python3 src/generate_ccf_model.py
python3 src/generate_ccf_partonomy.py
python3 src/generate_ccf_reference_entities.py
python3 src/generate_hubmap_spatial_entities.py
python3 src/generate_ccf_full.py
cp source_data/ccf-context.jsonld dist
cp src/partonomy.html src/partonomy.vg.json dist