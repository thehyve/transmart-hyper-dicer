from typing import List, Optional, Dict

from dicer.data_exception import DataException
from transmart_loader.transmart import Concept as TLConcept, Patient as TLPatient, Visit as TLVisit, \
    TrialVisit as TLTrialVisit, Modifier as TLModifier, Observation as TLObservation, \
    ObservationMetadata as TLObservationMetadata, CategoricalValue as TLCategoricalValue, \
    NumericalValue as TLNumericalValue, Value as TLValue

from dicer.mappers.mapper_helper import value_by_value_type
from dicer.transmart import ConceptDimensionElement, Hypercube, DimensionDeclaration, PatientDimensionElement, \
    VisitDimensionElement, TrialVisitDimensionElement, Cell, StudyDimensionElement


class ObservationMapper:
    """
    Map observations from hypercube query results to transmart-loader objects
    """

    def __init__(self,
                 patient_id_to_patient: Dict[int, TLPatient],
                 concept_code_to_concept: Dict[str, TLConcept],
                 visits: List[TLVisit],
                 trial_visits: List[TLTrialVisit],
                 modifiers: List[TLModifier]):
        self.patient_id_to_patient = patient_id_to_patient
        self.concept_code_to_concept = concept_code_to_concept
        self.visits = visits
        self.trial_visits = trial_visits
        self.modifiers = modifiers

    @staticmethod
    def get_index_by_dimension_name(dimensions: List[DimensionDeclaration], name: str, mandatory: bool = False):
        index = next((i for i, dim in enumerate(dimensions) if dim.name == name), None)
        if index is None and mandatory:
            raise DataException(f'Missing mandatory dimension {name}')
        return index

    @staticmethod
    def get_observation_value(cell: Cell) -> TLValue:
        value = TLCategoricalValue(cell.stringValue) if cell.stringValue else TLNumericalValue(
            cell.numericValue)  # TODO DateValue?
        return value

    def get_observation_metadata(self, cell: Cell, hypercube: Hypercube,
                                 indexed_dimensions: List[DimensionDeclaration],
                                 modifier_dimensions: List[DimensionDeclaration]) -> Optional[TLObservationMetadata]:
        metadata_values = dict()
        for modifier_dim in modifier_dimensions:
            modifier_dimension_index = self.get_index_by_dimension_name(indexed_dimensions, modifier_dim.name)
            modifier_dimension_element_id = cell.dimensionIndexes[modifier_dimension_index]
            if modifier_dimension_element_id is not None:
                modifier = next(filter(lambda x: x.modifier_code == modifier_dim.modifierCode, self.modifiers))
                modifier_value = hypercube.dimensionElements[modifier_dim.name][modifier_dimension_element_id]
                metadata_values[modifier] = value_by_value_type(modifier_value, modifier.value_type)
        if metadata_values:
            return TLObservationMetadata(metadata_values)
        return None

    def get_observation_trial_visit(self, trial_visit_dim_element: TrialVisitDimensionElement) -> Optional[TLTrialVisit]:
        trial_visit = None
        if trial_visit_dim_element:
            trial_visit = next(filter(lambda x:
                                      (x.study.study_id, x.rel_time_label) == (trial_visit_dim_element.studyId,
                                                                               trial_visit_dim_element.relTimeLabel),
                                      self.trial_visits))
        return trial_visit

    def get_observation_trial_visit_for_study(self, study_dim_element: StudyDimensionElement) -> Optional[TLTrialVisit]:
        trial_visit = next(filter(lambda x: (x.study.study_id == study_dim_element.name), self.trial_visits), None)
        if trial_visit is None:
            raise DataException(f'No trial visit found for study {study_dim_element.name}')
        return trial_visit

    def get_observation_visit(self, visit_dim_element: VisitDimensionElement) -> Optional[TLVisit]:
        if visit_dim_element:
            return next(filter(lambda x: x.identifier == visit_dim_element.encounterIds['VISIT_ID'], self.visits))
        return None

    def get_observation_concept(self, concept_dim_element: ConceptDimensionElement) -> TLConcept:
        return self.concept_code_to_concept.get(concept_dim_element.conceptCode)

    def get_observation_patient(self, patient_dim_element: PatientDimensionElement) -> TLPatient:
        return self.patient_id_to_patient.get(patient_dim_element.id)

    def map_observations(self, hypercube: Hypercube) -> List[TLObservation]:
        observations = []
        inline_dimensions = list(filter(lambda d: d.inline, hypercube.dimensionDeclarations))
        indexed_dimensions = list(filter(lambda d: d not in inline_dimensions, list(hypercube.dimensionDeclarations)))
        modifier_dimensions = list(filter(lambda d: d.modifierCode is not None, list(hypercube.dimensionDeclarations)))

        start_time_dimension_idx = self.get_index_by_dimension_name(inline_dimensions, 'start time')
        end_time_dimension_idx = self.get_index_by_dimension_name(inline_dimensions, 'end time')
        patient_dimension_idx = self.get_index_by_dimension_name(indexed_dimensions, 'patient', True)
        concept_dimension_idx = self.get_index_by_dimension_name(indexed_dimensions, 'concept', True)
        visit_dimension_idx = self.get_index_by_dimension_name(indexed_dimensions, 'visit')
        trial_visit_dimension_idx = self.get_index_by_dimension_name(indexed_dimensions, 'trial visit')
        study_dimension_idx = self.get_index_by_dimension_name(indexed_dimensions, 'study', True)

        for cell in hypercube.cells:
            patient_dim_elem_idx = cell.dimensionIndexes[patient_dimension_idx]
            patient_dim_elem = PatientDimensionElement(**hypercube.dimensionElements['patient'][patient_dim_elem_idx])
            observation_patient = self.get_observation_patient(patient_dim_elem)

            concept_dim_elem_idx = cell.dimensionIndexes[concept_dimension_idx]
            concept_dim_elem = ConceptDimensionElement(**hypercube.dimensionElements['concept'][concept_dim_elem_idx])
            observation_concept = self.get_observation_concept(concept_dim_elem)

            observation_visit = None  # Optional
            visit_dim_elem_idx = cell.dimensionIndexes[visit_dimension_idx]
            if visit_dim_elem_idx is not None:
                visit_dim_element = VisitDimensionElement(**hypercube.dimensionElements['visit'][visit_dim_elem_idx])
                observation_visit = self.get_observation_visit(visit_dim_element)

            if trial_visit_dimension_idx is None:
                # get trial visit from study
                study_dim_elem_idx = cell.dimensionIndexes[study_dimension_idx]
                study_dim_elem = StudyDimensionElement(
                    **hypercube.dimensionElements['study'][study_dim_elem_idx])
                observation_trial_visit = self.get_observation_trial_visit_for_study(study_dim_elem)
            else:
                trial_visit_dim_elem_idx = cell.dimensionIndexes[trial_visit_dimension_idx]
                trial_visit_dim_elem = TrialVisitDimensionElement(
                    **hypercube.dimensionElements['trial visit'][trial_visit_dim_elem_idx])
                observation_trial_visit = self.get_observation_trial_visit(trial_visit_dim_elem)

            observation_start_time = cell.inlineDimensions[start_time_dimension_idx]
            observation_end_time = cell.inlineDimensions[end_time_dimension_idx]
            observation_value = self.get_observation_value(cell)
            observation_metadata =\
                self.get_observation_metadata(cell, hypercube, indexed_dimensions, modifier_dimensions)

            observations.append(TLObservation(
                observation_patient,
                observation_concept,
                observation_visit,
                observation_trial_visit,
                observation_start_time,
                observation_end_time,
                observation_value,
                observation_metadata
            ))

        return observations

