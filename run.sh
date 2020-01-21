#!/bin/bash

mkdir -p docs

if [ ! -e source_ontologies/fma.owl ]; then
  echo "Please download the FMA Owl file from the URL below and save to source_ontologies/fma.owl"
  echo
  echo "https://bioportal.bioontology.org/ontologies/FMA"
  exit -1
fi

python3 src/ccf_model.py
python3 src/ccf_partonomy.py
python3 src/ccf_full.py
