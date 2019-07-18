from transmart_loader.transmart import DataCollection

from dicer.mapper_helper import *
from dicer.query_results import QueryResults
from dicer.transmart \
    import ConceptDimensionElement, PatientDimensionElement, \
    StudyDimensionElement, TrialVisitDimensionElement, \
    VisitDimensionElement


class TransmartLoaderMapper:
    '''
    Transmart query results to transmart-loader mapping
    '''
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

    @staticmethod
    def _map_objects(objects, mapping_method, **kwargs):
        return list(map(lambda x: mapping_method(x, kwargs), objects))

    def map_query_results(self, query_results: QueryResults) -> DataCollection:

        patient_objects = query_results.observations.dimensionElements.get('patient', [])
        self.patients = list(map(lambda x: map_patient(PatientDimensionElement(**x)), patient_objects))

        dimension_objects = query_results.dimensions.dimensions
        modifier_objects = list(filter(lambda x: x.modifierCode, dimension_objects))
        self.modifiers = list(map(lambda x: map_modifiers(x), modifier_objects))
        self.dimensions = list(map(lambda x: map_dimension(x, self.modifiers), dimension_objects))

        study_objects = query_results.observations.dimensionElements.get('study', [])
        all_studies = query_results.studies.studies
        for study in all_studies:
            if study.studyId in list(map(lambda x: StudyDimensionElement(**x).name, study_objects)):
                self.studies.append(map_study(study))

        concept_objects = query_results.observations.dimensionElements.get('concept', [])
        self.concepts = list(map(lambda x: map_concept(ConceptDimensionElement(**x)), concept_objects))
        tree_node_objects = query_results.tree_nodes.tree_nodes
        self.ontology = list(map(lambda x: map_tree_node(x, self.studies, self.concepts), tree_node_objects))

        trial_visit_objects = query_results.observations.dimensionElements.get('trial visit', [])
        self.trial_visits = list(
            map(lambda x: map_trial_visit(TrialVisitDimensionElement(**x), self.studies), trial_visit_objects))

        visit_objects = query_results.observations.dimensionElements['visit']
        self.visits = list(map(lambda x: map_visit(VisitDimensionElement(**x), self.patients), visit_objects))

        relation_type_objects = query_results.relation_types.relationTypes
        self.relation_types = list(map(lambda x: map_relation_type(x), relation_type_objects))

        relation_objects = query_results.relations.relations
        self.relations = list(map(lambda x: map_relation(x, self.patients, self.relation_types), relation_objects))

        self.observations = map_observations(query_results.observations,
                                             self.patients, self.concepts, self.visits, self.trial_visits,
                                             self.modifiers)

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
