#!/usr/bin/env python3
import datetime
from owlready2 import *
from constants import CCF_NAMESPACE, CCF_MODEL


onto = get_ontology(CCF_NAMESPACE)

with onto:
  class ccf_part_of(ObjectProperty):
    pass
  class ccf_annotation(ObjectProperty):
    pass
  class ccf_freetext_annotation(ObjectProperty):
    range = [str]
  class ccf_same_as(ObjectProperty):
    pass

  class has_x(DataProperty, FunctionalProperty):
    range = [float]
  class has_y(DataProperty, FunctionalProperty):
    range = [float]
  class has_z(DataProperty, FunctionalProperty):
    range = [float]
  class has_units(DataProperty, FunctionalProperty):
    range = [str]
  class has_creator_orcid(AnnotationProperty, FunctionalProperty):
    range = [str]
  class has_creator_first_name(AnnotationProperty, FunctionalProperty):
    range = [str]
  class has_creator_last_name(AnnotationProperty, FunctionalProperty):
    range = [str]

  class SpatialTransformation(Thing):
    label = 'spatial transformation'
  class SpatialRotation(Thing):
    label = 'spatial rotation'
  class SpatialTranslation(Thing):
    label = 'spatial translation'
  class SpatialScaling(Thing):
    label = 'spatial scaling'
  class has_rotation(ObjectProperty, FunctionalProperty):
    domain = [SpatialTransformation]
    range = [SpatialRotation]
  class has_translation(ObjectProperty, FunctionalProperty):
    domain = [SpatialTransformation]
    range = [SpatialTranslation]
  class has_scaling(ObjectProperty, FunctionalProperty):
    domain = [SpatialTransformation]
    range = [SpatialScaling]

  class SpatialPlacement(Thing):
    label = 'spatial placement'
  class has_transformation(ObjectProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [SpatialTransformation]
  class has_placement_date(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [datetime.date]

  class SpatialObjectReference(Thing):
    label = 'spatial object reference'
  class has_object_file(DataProperty, FunctionalProperty):
    domain = [SpatialObjectReference]
    range = [str] # URI
  class has_object_file_format(DataProperty, FunctionalProperty):
    domain = [SpatialObjectReference]
    range = [str] # mimetype
  class has_object_file_subpath(DataProperty, FunctionalProperty):
    domain = [SpatialObjectReference]
    range = [str] # format specific internal path
  class has_object_file_transformation(ObjectProperty, FunctionalProperty):
    domain = [SpatialObjectReference]
    range = [SpatialTransformation]
  
  class SpatialDimension(Thing):
    label = 'spatial dimension'

  class SpatialEntity(Thing):
    label = 'spatial entity'
  class has_object_reference(ObjectProperty):
    domain = [SpatialEntity]
    range = [SpatialObjectReference]
  class has_dimensions(ObjectProperty, FunctionalProperty):
    domain = [SpatialEntity]
    range = [SpatialDimension]
  class has_placement(ObjectProperty):
    domain = [SpatialEntity]
    range = [SpatialPlacement]
  class has_placementee(ObjectProperty):
    domain = [SpatialEntity]
    range = [SpatialPlacement]
  class representation_of(AnnotationProperty):
    domain = [SpatialEntity]

onto.save(file=CCF_MODEL, format='rdfxml')
