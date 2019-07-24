from transmart_loader.transmart import DataCollection, Concept, Visit

from dicer.mappers.mapper_helper import *
from dicer.mappers.observation_mapper import ObservationMapper
from dicer.mappers.ontology_mapper import OntologyMapper
from dicer.mappers.patient_mapper import PatientMapper
from dicer.query_results import QueryResults
from dicer.transmart import StudyDimensionElement, TrialVisitDimensionElement


class TransmartLoaderMapper:
    """
    Transmart query results to transmart-loader objects mapping
    """
    def __init__(self):
        self.concepts: List[Concept] = []
        self.modifiers: List[Modifier] = []
        self.dimensions: List[Dimension] = []
        self.studies: List[Study] = []
        self.trial_visits: List[TrialVisit] = []
        self.visits: List[Visit] = []
        self.ontology = []
        self.patients = []
        self.observations = []
        self.relation_types = []
        self.relations = []

    def map_query_results(self, query_results: QueryResults) -> DataCollection:

        patient_mapper = PatientMapper()
        self.patients = patient_mapper.map_patients(query_results.observations.dimensionElements.get('patient', []))
        self.relation_types = list(map(lambda x: map_relation_type(x), query_results.relation_types.relationTypes))
        self.relations = patient_mapper.map_patient_relations(query_results.relations.relations, self.relation_types)
        self.visits = patient_mapper.map_patient_visits(query_results.observations.dimensionElements['visit'])

        dimension_objects = query_results.dimensions.dimensions
        modifier_objects = list(filter(lambda x: x.modifierCode, dimension_objects))
        self.modifiers = list(map(lambda x: map_modifiers(x), modifier_objects))
        self.dimensions = list(map(lambda x: map_dimension(x, self.modifiers), dimension_objects))

        study_objects = query_results.observations.dimensionElements.get('study', [])
        for study in query_results.studies.studies:
            if study.studyId in list(map(lambda x: StudyDimensionElement(**x).name, study_objects)):
                self.studies.append(map_study(study))

        ontology_mapper = OntologyMapper(self.studies)
        self.concepts = ontology_mapper.map_concepts(query_results.observations.dimensionElements.get('concept', []))
        self.ontology = ontology_mapper.map_tree_nodes(query_results.tree_nodes.tree_nodes)

        trial_visit_objects = query_results.observations.dimensionElements.get('trial visit', [])
        self.trial_visits = list(
            map(lambda x: map_trial_visit(TrialVisitDimensionElement(**x), self.studies), trial_visit_objects))

        observation_mapper = ObservationMapper(self.patients, self.concepts, self.visits, self.trial_visits,
                                               self.modifiers)
        self.observations = observation_mapper.map_observations(query_results.observations)
        return DataCollection(self.concepts,
                              self.modifiers,
                              self.dimensions,
                              self.studies,
                              self.trial_visits,
                              self.visits,
                              self.ontology,
                              self.patients,
                              self.observations,
                              self.relation_types,
                              self.relations)
