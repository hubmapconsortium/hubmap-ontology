#!/usr/bin/env python3
import datetime
from owlready2 import *
from constants import CCF_NAMESPACE, CCF_MODEL


onto = get_ontology(CCF_NAMESPACE)

with onto:
  class ccf_part_of(ObjectProperty):
    pass
  class ccf_part_of_rank(ObjectProperty):
    range = [int]
  class ccf_rui_rank(ObjectProperty):
    range = [int]
  class ccf_annotation(ObjectProperty):
    pass
  class ccf_freetext_annotation(ObjectProperty):
    range = [str]
  class ccf_same_as(ObjectProperty):
    pass
  class has_sex(ObjectProperty):
    range = [str]
  class has_side(ObjectProperty):
    range = [str]

  class ccf_preferred_label(AnnotationProperty, FunctionalProperty):
    range = [str]
  class creator_orcid(AnnotationProperty, FunctionalProperty):
    range = [str]
  class creator_uuid(AnnotationProperty, FunctionalProperty):
    range = [str]
  class creator_first_name(AnnotationProperty, FunctionalProperty):
    range = [str]
  class creator_last_name(AnnotationProperty, FunctionalProperty):
    range = [str]
  class creation_date(AnnotationProperty, FunctionalProperty):
    range = [datetime.date]
  class updated_date(AnnotationProperty, FunctionalProperty):
    range = [datetime.date]

  class SpatialPlacement(Thing):
    label = 'spatial placement'
  class has_placement_date(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [datetime.date]
  # Scaling
  class has_x_scaling(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_y_scaling(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_z_scaling(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  # Rotation
  class has_x_rotation(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_y_rotation(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_z_rotation(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_theta_rotation(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_rotation_order(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [str]
  class has_rotation_units(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [str]
  # Translation
  class has_x_translation(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_y_translation(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]
  class has_z_translation(DataProperty, FunctionalProperty):
    domain = [SpatialPlacement]
    range = [float]

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
  
  class SpatialEntity(Thing):
    label = 'spatial entity'
  class has_x_dimension(DataProperty, FunctionalProperty):
    domain = [SpatialEntity]
    range = [float]
  class has_y_dimension(DataProperty, FunctionalProperty):
    domain = [SpatialEntity]
    range = [float]
  class has_z_dimension(DataProperty, FunctionalProperty):
    domain = [SpatialEntity]
    range = [float]
  class has_dimension_units(DataProperty, FunctionalProperty):
    domain = [SpatialEntity]
    range = [str]
  class has_object_reference(ObjectProperty):
    domain = [SpatialEntity]
    range = [SpatialObjectReference]
  class ccf_representation_of(AnnotationProperty):
    domain = [SpatialEntity]

  class has_placement_source(ObjectProperty):
    domain = [SpatialPlacement]
    range = [SpatialEntity, SpatialObjectReference]
  class has_placement_target(ObjectProperty):
    domain = [SpatialPlacement]
    range = [SpatialEntity]

  class anatomical_structure_of(ObjectProperty):
    domain = [SpatialEntity]
    range = [SpatialEntity]

  class ExtractionSet(Thing):
    label = 'extraction set'

  class extraction_site_for(ObjectProperty):
    domain = [SpatialEntity]
    range = [ExtractionSet]

  """ NOTE: Not Ready for prime time
  class Entity(Thing):
    label = 'CCF-indexed entity'
  ### Search properties ###
  class has_age(DataProperty, FunctionalProperty):
    label = 'Donor age (in years) at time of Procedure'
    domain = [Entity]
    range = [int]
  class has_sex(DataProperty, FunctionalProperty):
    label = 'Donor sex at time of Procedure: Male, Female'
    domain = [Entity]
    range = [str]
  class has_bmi(DataProperty, FunctionalProperty):
    label = 'Donor BMI at time of Procedure'
    domain = [Entity]
    range = [float]
  class has_provider(DataProperty, FunctionalProperty):
    label = 'Provider who processed the Procedure'
    domain = [Entity]
    range = [str]
  # has_ccf_annotation is above
  ### Metadata Properties ###
  class has_entitytype(DataProperty, FunctionalProperty):
    label = 'Type of entity: Donor, Sample, Dataset'
    domain = [Entity]
    range = [str]
  class has_uuid(DataProperty, FunctionalProperty):
    label = 'UUID'
    domain = [Entity]
    range = [str]
  class has_doi(DataProperty, FunctionalProperty):
    label = 'DOI'
    domain = [Entity]
    range = [str]
  class has_display_doi(DataProperty, FunctionalProperty):
    label = 'Display DOI'
    domain = [Entity]
    range = [str]
  class has_hubmap_id(DataProperty, FunctionalProperty):
    label = 'HuBMAP ID'
    domain = [Entity]
    range = [str]
  # Use dc:creator and creator_uuid
  # Use updated_date
  # Use rdfs:label for label
  class has_short_description(DataProperty, FunctionalProperty):
    label = 'short description'
    domain = [Entity]
    range = [str]
  class has_long_description(DataProperty, FunctionalProperty):
    label = 'long description'
    domain = [Entity]
    range = [str]
  class has_thumbnail_url(DataProperty, FunctionalProperty):
    label = 'thumbnail url'
    domain = [Entity]
    range = [str]
  class has_download_url(DataProperty, FunctionalProperty):
    label = 'download url'
    domain = [Entity]
    range = [str]
  class has_download_tooltip(DataProperty, FunctionalProperty):
    label = 'download url tooltip'
    domain = [Entity]
    range = [str]
  class has_result_url(DataProperty, FunctionalProperty):
    label = 'result url'
    domain = [Entity]
    range = [str]
  class has_result_type(DataProperty, FunctionalProperty):
    label = 'result type: external_link, local_link, image_viewer'
    domain = [Entity]
    range = [str]
  """

onto.save(file=CCF_MODEL, format='rdfxml')
