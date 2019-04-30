# hubmap-ontology

[![Shipping faster with ZenHub](https://img.shields.io/badge/Shipping_faster_with-ZenHub-5e60ba.svg?style=flat-square)](https://app.zenhub.com/workspaces/ccf-ontology-5cb5dc061be1263b113a17b3/board)

Repository for creating ontologies for HuBMAP

To create these ontologies, we need code as well as original data. Code and data should have an open-source licenses, e.g. MIT for code and CC-BY for data.

Currently, code is licensed under the MIT License and the data is CC-BY 4.0. Eventually, there should be a curated ontology/release version of the ontology that is CC-BY-ND (No derivatives) that will ensure that there are fixed reference forms of the ontology, which should exist side-by-side with an almost identical one so as to permit the ontology to be remixed and reused as need be.

These license policies will be revised in coordination with the appropriate HuBMAP working groups as needed. 

## Release 0.1.0 overview 
The CCF ontology bundles the initial CCF ontology, requested ontology terms, and software necessary to generate the ontology. 

Release 0.1.0 introduces the basic scaffolding (inherited from existing ontologies, particularly UBERON) browsing from the whole-body scale to the single-organ scale, including "insertion points" for organ-specific ontologies. 

It also introduces alpha-level ontologies for kidney and heart, based on terms requested by TMCs and in discussions, to prototype technologies to construct slim ontologies from terms selected from multiple existent ontologies.
As part of this effort, 0.1.0 developed the software framework to add new terms ot the ontology via spreadsheet. 

Lastly, 0.1.0 includes a prototype data ontology and data framework.
The entire ontology is released as an OWL (W3C Web Ontology Language) file, which can be found in the data subdirectory.
We note that we have had some problems with the Turtle format of the ontology, but that the RDF/XML one has given us no problems (as of March 27, 2019).

### Data Framework

For the alpha release, find the correct ontological term in the OWL file and use that term to annotate data. We recommend using [Protege](https://protege.stanford.edu/products.php#desktop-protege) to view and search the ontology.
As this is an alpha-level release, we do not know how the terms will necessarily be incorporated into the data.
Thus, we provide the list of terms. We recommend following the metadata framework (see below) with its spreadsheet as a good way to get started.

### Metadata Framework

We have included a spreadsheet in
```framework/metadata_framework.xslx```
where users can enter in relevant metadata and have the correct ontological term be associated with the metadata.
For v0.1.0, the ontological terms are in hidden rows, 2-5.

## CCF Development roadmap
We maintain a development and release roadmap for the CCF Ontology and supporting software, available [here] (https://docs.google.com/document/d/1Sso27-7YI4993LC5a_HTBBMOK6QN83pcgXEg0ggrsWc/edit) (last updated: March 27, 2019).

## Documentation

[Documentation can be found here](https://docs.google.com/document/d/1X21O5DgGkq9ngPOsBZa-qy1-6Y2MiohJD7Bt-JFyysY/edit#)

## New terms/Bug Reports

If you wish to have new terms be added to the ontology or have other bugs in the software to report, please [fill out a ticket](https://github.com/hubmapconsortium/hubmap-ontology/issues).

## Dependencies

Currently, the code requires the following Python (v3.7.2)  packges:
* Ontospy (1.9.8.2)
* Networkx (2.2)
* RDFLib (4.2.2)
* pandas (0.24.2)
* pydot (1.4.1)
* PyYAML (5.1)
* NumPy (1.16.2)

## Running the code

To run the code:
```
python3 owl_to_nx.py
```
We recommend running the code though in ipython or Jupyter and running these commands first after the import statements:
```
o = ontospy.Ontospy()
o.load_rdf("ext.owl")
o.build_classes()
```
where ext.owl is the ontology file to be loaded. We are using this version of UBERON:  [http://purl.obolibrary.org/obo/uberon/releases/2018-11-25/ext.owl].
This will eventually go into the settings file, owl_settings.yml.
At the moment, the loading and building of the classes takes an extremely long time (~10-30 minutes). Then the rest of the code can be run quickly to generate the ontology.

To change other parameters in the Python code, please adjust owl_settings.yml.
If there's not a setting in the file, please create a ticket for this and we can add it.

## Visualization

Visualization of the partonomy tree can be found [here](https://vega.github.io/editor/#/gist/vega/bherr2/542482aea690cea2a299f5153aa212eb/90ac7717b3500f84b163ff16c8c2bb83f9d90ce1/hubmap-partonomy.vg.json/view)
