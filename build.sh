#!/bin/bash

rm -rf dist
mkdir -p dist

cp -r source_objects dist/objects
python3 src/generate_ccf_model.py
python3 src/generate_ccf_partonomy.py
python3 src/generate_ccf_reference_entities.py
python3 src/generate_hubmap_spatial_entities.py
python3 src/generate_ccf_full.py
cp source_data/ccf-*context.jsonld dist
cp src/ccf-partonomy.html src/ccf-partonomy.vg.json dist
python3 src/generate_ccf_partonomy_report.py

if [ "$1" == "report" ]
then
  mkdir -p dist/reports
  python3 src/generate_ccf_partonomy_report.py dist/reports/ccf-partonomy.heart.csv http://purl.obolibrary.org/obo/UBERON_0000948
  python3 src/generate_ccf_partonomy_report.py dist/reports/ccf-partonomy.lung.csv http://purl.obolibrary.org/obo/LMHA_00211
  python3 src/generate_ccf_partonomy_report.py dist/reports/ccf-partonomy.kidney.csv http://purl.obolibrary.org/obo/UBERON_0002113
  python3 src/generate_ccf_partonomy_report.py dist/reports/ccf-partonomy.spleen.csv http://purl.obolibrary.org/obo/UBERON_0002106
  python3 src/generate_ccf_partonomy_report.py dist/reports/ccf-partonomy.colon.csv http://purl.obolibrary.org/obo/UBERON_0001155
  python3 src/generate_ccf_partonomy_report.py dist/reports/ccf-partonomy.small-intestine.csv http://purl.obolibrary.org/obo/UBERON_0002108
  python3 src/generate_ccf_partonomy_report.py dist/reports/ccf-partonomy.rectum.csv http://purl.obolibrary.org/obo/UBERON_0001052
fi