from transmart_loader.transmart import DataCollection

from dicer.mappers.mapper_helper import *
from dicer.mappers.observation_mapper import ObservationMapper
from dicer.mappers.ontology_mapper import OntologyMapper
from dicer.mappers.patient_mapper import PatientMapper
from dicer.query_results import QueryResults
from dicer.transmart import TrialVisitDimensionElement


class TransmartLoaderMapper:
    """
    Transmart query results to transmart-loader objects mapping
    """

    @staticmethod
    def map_query_results(query_results: QueryResults) -> DataCollection:

        patient_mapper = PatientMapper()
        patients = patient_mapper.map_patients(query_results.observations.dimensionElements.get('patient', []))
        relation_types = list(map(lambda x: map_relation_type(x), query_results.relation_types.relationTypes))
        relations = patient_mapper.map_patient_relations(query_results.relations.relations, relation_types)
        visits = patient_mapper.map_patient_visits(query_results.observations.dimensionElements['visit'])

        dimension_objects = query_results.dimensions.dimensions
        modifier_objects = list(filter(lambda x: x.modifierCode, dimension_objects))
        modifiers = list(map(lambda x: map_modifier(x), modifier_objects))
        dimensions = list(map(lambda x: map_dimension(x, modifiers), dimension_objects))

        study_id_to_study = get_study_id_to_study_dict(query_results.observations.dimensionElements['study'],
                                                       query_results.studies.studies)
        studies = list(study_id_to_study.values())

        ontology_mapper = OntologyMapper(study_id_to_study, query_results.observations.dimensionElements['concept'])
        ontology = ontology_mapper.map_tree_nodes(query_results.tree_nodes.tree_nodes)
        concepts = list(ontology_mapper.concept_code_to_concept.values())

        trial_visit_dim_elements = query_results.observations.dimensionElements.get('trial visit', [])
        trial_visits = list(
            map(lambda x: map_trial_visit(TrialVisitDimensionElement(**x), study_id_to_study), trial_visit_dim_elements))

        observation_mapper = ObservationMapper(patient_mapper.patient_id_to_patient,
                                               ontology_mapper.concept_code_to_concept,
                                               visits, trial_visits, modifiers)
        observations = observation_mapper.map_observations(query_results.observations)

        return DataCollection(concepts,
                              modifiers,
                              dimensions,
                              studies,
                              trial_visits,
                              visits,
                              ontology,
                              patients,
                              observations,
                              relation_types,
                              relations)
