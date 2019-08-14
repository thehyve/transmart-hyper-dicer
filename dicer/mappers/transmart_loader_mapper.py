from transmart_loader.transmart import DataCollection, TrialVisit

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

    study_id_to_study: Dict[str, TLStudy] = None
    studies: List[Study] = None

    def map_study(self, study: Study) -> TLStudy:
        return TLStudy(
            study.studyId,
            study.studyId,
            study.metadata
        )

    def map_studies(self, study_dim_element_values: List[Value], all_studies: List[Study]) -> Dict[str, TLStudy]:
        study_id_to_study: Dict[str, TLStudy] = {}
        study_dim_elements = set(map(lambda x: StudyDimensionElement(**x).name, study_dim_element_values))
        for study in all_studies:
            if study.studyId in study_dim_elements:
                study_id_to_study[study.studyId] = self.map_study(study)
        return study_id_to_study

    def map_trial_visit(self, trial_visit: TrialVisitDimensionElement) -> TLTrialVisit:
        study = self.study_id_to_study.get(trial_visit.studyId)
        return TLTrialVisit(
            study,
            trial_visit.relTimeLabel,
            trial_visit.relTimeUnit,
            trial_visit.relTime
        )

    def map_trial_visits(self, trial_visit_dim_elements: List[Value]) -> List[TrialVisit]:
        """Map trial visit dimension elements to trial visit objects if the trial visit
        dimension is available. Create dummy trial visits based on the list of studies otherwise."""
        if trial_visit_dim_elements is None:
            return [TLTrialVisit(study, '') for study in self.studies]
        else:
            return [self.map_trial_visit(TrialVisitDimensionElement(**x))
                    for x in trial_visit_dim_elements]

    def map_query_results(self, query_results: QueryResults) -> DataCollection:

        patient_mapper = PatientMapper()
        patients = patient_mapper.map_patients(query_results.observations.dimensionElements.get('patient', []))
        relation_types = list(map(lambda x: map_relation_type(x), query_results.relation_types.relationTypes))
        relations = patient_mapper.map_patient_relations(query_results.relations.relations, relation_types)
        visits = patient_mapper.map_patient_visits(query_results.observations.dimensionElements['visit'])

        dimension_objects = query_results.dimensions.dimensions
        modifier_objects = list(filter(lambda x: x.modifierCode, dimension_objects))
        modifiers = list(map(lambda x: map_modifier(x), modifier_objects))
        dimensions = list(map(lambda x: map_dimension(x, modifiers), dimension_objects))

        self.study_id_to_study = self.map_studies(query_results.observations.dimensionElements['study'],
                                                  query_results.studies.studies)
        self.studies = list(self.study_id_to_study.values())

        ontology_mapper = OntologyMapper(
            self.study_id_to_study, query_results.observations.dimensionElements['concept'])
        ontology = ontology_mapper.map_tree_nodes(query_results.tree_nodes.tree_nodes)
        concepts = list(ontology_mapper.concept_code_to_concept.values())

        trial_visit_dim_elements = query_results.observations.dimensionElements.get('trial visit', None)
        trial_visits = self.map_trial_visits(trial_visit_dim_elements)

        observation_mapper = ObservationMapper(patient_mapper.patient_id_to_patient,
                                               ontology_mapper.concept_code_to_concept,
                                               visits, trial_visits, modifiers)
        observations = observation_mapper.map_observations(query_results.observations)

        return DataCollection(concepts,
                              modifiers,
                              dimensions,
                              self.studies,
                              trial_visits,
                              visits,
                              ontology,
                              patients,
                              observations,
                              relation_types,
                              relations)
