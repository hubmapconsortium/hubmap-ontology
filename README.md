# The Common Coordinate Framework (CCF)

[![License: CC BY 4.0](https://licensebuttons.net/l/by/4.0/80x15.png)](https://creativecommons.org/licenses/by/4.0/)

The CCF consists of seven parts:

1. **The CCF Core Model (CCF-CM)** is an architecture for modeling 2-dimensional (2D) and 3-dimensional (3D) spatial data annotated with ontology terms.
2. **The CCF Spatial Reference System (CCF-SRS)** is a curated and annotated instantiation of the Core Model for the Human Body down to the tissue level.
3. **The CCF Anatomical Partonomy (CCF-AP)** is a curated partonomy using existing ontology terms which mirrors the CCF-SRS, but goes further (though not down to the cellular level).
4. **The CCF Cell Types Ontology (CCF-CT)** is a curated ontology using existing ontology terms which describes cell types and connects to the CCF-AP where appropriate.
5. **The CCF Union Ontology (CCF-UO)** is a curated set of ontologies which represents the universe of ontologies connected via the CCF.
6. **The CCF Registration User Interface (CCF-RUI)** is an online interface for placing tissue samples into Reference Organs defined by the CCF-SRS. See [here](https://hubmapconsortium.github.io/ccf-ui/).
7. **The CCF Exploration User Interface (CCF-EUI)** is an online interface for exploring and querying the CCF-SRS, CCF-P, and entities indexed by them, primarily via the CCF-RUI. See [here](https://hubmapconsortium.github.io/ccf-3d-registration/).

## Links

* Documentation
  * [Technical description](https://docs.google.com/document/d/1aS0Xe5uhajnNY0VsuXtHvAUVH5mnd1otheCvEzIv28s/edit?usp=sharing)

* CCF
  * Latest version: <http://purl.org/ccf/latest/ccf.owl>
  * Visualization: [![Visualize the CCF Ontology](https://img.shields.io/badge/Visualize%20with-WebVowl-brightgreen.svg)](http://visualdataweb.de/webvowl/#iri=http://purl.org/ccf/latest/ccf.owl)
  * Test: [![RDF Triple-Checker](https://img.shields.io/badge/RDF%20Triple-Checker-brightgreen.svg)](http://graphite.ecs.soton.ac.uk/checker/?uri=http://purl.org/ccf/latest/ccf.owl)
* CCF Partonomy (CCF-AP)
  * CSV Version: <http://purl.org/ccf/latest/ccf-partonomy.csv>
  * JSON-LD Version: <http://purl.org/ccf/latest/ccf-partonomy.jsonld>
  * Visualization: <http://purl.org/ccf/latest/ccf-partonomy.html>

## License

The CCF Ontology is CC-BY 4.0 licensed. The code to generate the ontology is MIT licensed.

## Credits

The CCF is developed at the [Cyberinfrastructure for Network Science Center at Indiana University](http://cns.iu.edu/). It is funded by NIH Award [OT2OD026671](https://projectreporter.nih.gov/project_info_description.cfm?aid=9687220").
