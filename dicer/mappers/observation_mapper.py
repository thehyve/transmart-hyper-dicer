from typing import List, Optional

from transmart_loader.transmart import Concept as TLConcept, Patient as TLPatient, Visit as TLVisit, \
    TrialVisit as TLTrialVisit, Modifier as TLModifier, Observation as TLObservation, \
    ObservationMetadata as TLObservationMetadata, CategoricalValue as TLCategoricalValue, \
    NumericalValue as TLNumericalValue, Value as TLValue

from dicer.mappers.mapper_helper import value_by_value_type
from dicer.transmart import ConceptDimensionElement, Hypercube, DimensionDeclaration, PatientDimensionElement, \
    VisitDimensionElement, TrialVisitDimensionElement, Cell


class ObservationMapper:
    """
    Map observations from hypercube query results to transmart-loader objects
    """

    def __init__(self,
                 patients: List[TLPatient],
                 concepts: List[TLConcept],
                 visits: List[TLVisit],
                 trial_visits: List[TLTrialVisit],
                 modifiers: List[TLModifier]):
        self.patients = patients
        self.concepts = concepts
        self.visits = visits
        self.trial_visits = trial_visits
        self.modifiers = modifiers

    @staticmethod
    def get_id_by_dimension_name(dimensions: List[DimensionDeclaration], name: str):
        return next(i for i, dim in enumerate(dimensions) if dim.name == name)

    @staticmethod
    def get_observation_value(cell: Cell) -> TLValue:
        value = TLCategoricalValue(cell.stringValue) if cell.stringValue else TLNumericalValue(
            cell.numericValue)  # TODO DateValue?
        return value

    def get_observation_metadata(self, cell: Cell, hypercube: Hypercube,
                                 indexed_dimensions: List[DimensionDeclaration],
                                 modifier_dimensions: List[DimensionDeclaration]) -> Optional[TLObservationMetadata]:
        metadata = None
        for modifier_dim in modifier_dimensions:
            metadata_values = dict()
            modifier_dimension_id = self.get_id_by_dimension_name(indexed_dimensions, modifier_dim.name)
            modifier_dimension_element_id = cell.dimensionIndexes[modifier_dimension_id]
            if modifier_dimension_element_id is not None:
                modifier = next(filter(lambda x: x.modifier_code == modifier_dim.modifierCode, self.modifiers))
                modifier_value = hypercube.dimensionElements[modifier_dim.name][modifier_dimension_element_id]
                metadata_values[modifier] = value_by_value_type(modifier_value, modifier.value_type)
                metadata = TLObservationMetadata(metadata_values)
        return metadata

    def get_observation_trial_visit(self,
                                    cell: Cell,
                                    hypercube: Hypercube,
                                    trial_visits_dimension_id: int) -> Optional[TLTrialVisit]:
        trial_visit = None
        trial_visit_dim_element_id = cell.dimensionIndexes[trial_visits_dimension_id]
        if trial_visit_dim_element_id is not None:
            trial_visit_dim_element = TrialVisitDimensionElement(
                **hypercube.dimensionElements['trial visit'][trial_visit_dim_element_id])
            trial_visit = next(filter(lambda x:
                                      (x.study.study_id, x.rel_time_label) == (trial_visit_dim_element.studyId,
                                                                               trial_visit_dim_element.relTimeLabel),
                                      self.trial_visits))
        return trial_visit

    def get_observation_visit(self, cell: Cell, hypercube: Hypercube, visit_dimension_id: int) -> Optional[TLVisit]:
        visit = None
        visit_dim_element_id = cell.dimensionIndexes[visit_dimension_id]
        if visit_dim_element_id is not None:
            visit_dim_element = VisitDimensionElement(**hypercube.dimensionElements['visit'][visit_dim_element_id])
            visit = next(filter(lambda x: x.identifier == visit_dim_element.encounterIds['VISIT_ID'], self.visits))
        return visit

    def get_observation_concept(self, cell: Cell, hypercube: Hypercube, concept_dimension_id: int) -> TLConcept:
        concept_dim_element = ConceptDimensionElement(
            **hypercube.dimensionElements['concept'][cell.dimensionIndexes[concept_dimension_id]])
        concept = next(filter(lambda x: x.concept_code == concept_dim_element.conceptCode, self.concepts))
        return concept

    def get_observation_patient(self, cell: Cell, hypercube: Hypercube, patient_dimension_id: int) -> TLPatient:
        patient_dim_element = PatientDimensionElement(
            **hypercube.dimensionElements['patient'][cell.dimensionIndexes[patient_dimension_id]])
        patient = next(filter(lambda x: x.identifier == patient_dim_element.subjectIds['SUBJ_ID'], self.patients))
        return patient

    def map_observations(self, hypercube: Hypercube) -> List[TLObservation]:
        observations = []
        inline_dimensions = list(filter(lambda d: d.inline, hypercube.dimensionDeclarations))
        indexed_dimensions = list(filter(lambda d: d not in inline_dimensions, list(hypercube.dimensionDeclarations)))
        modifier_dimensions = list(filter(lambda d: d.modifierCode is not None, list(hypercube.dimensionDeclarations)))

        start_time_dimension_id = self.get_id_by_dimension_name(inline_dimensions, 'start time')
        end_time_dimension_id = self.get_id_by_dimension_name(inline_dimensions, 'end time')
        patient_dimension_id = self.get_id_by_dimension_name(indexed_dimensions, 'patient')
        concept_dimension_id = self.get_id_by_dimension_name(indexed_dimensions, 'concept')
        visit_dimension_id = self.get_id_by_dimension_name(indexed_dimensions, 'visit')
        trial_visits_dimension_id = self.get_id_by_dimension_name(indexed_dimensions, 'trial visit')

        for cell in hypercube.cells:
            observation_patient = self.get_observation_patient(cell, hypercube, patient_dimension_id)
            observation_concept = self.get_observation_concept(cell, hypercube, concept_dimension_id)
            observation_visit = self.get_observation_visit(cell, hypercube, visit_dimension_id)
            observation_trial_visit = self.get_observation_trial_visit(cell, hypercube, trial_visits_dimension_id)
            observation_start_time = cell.inlineDimensions[start_time_dimension_id]
            observation_end_time = cell.inlineDimensions[end_time_dimension_id]
            observation_value = self.get_observation_value(cell)
            observation_metadata = self.get_observation_metadata(cell, hypercube,
                                                                 indexed_dimensions, modifier_dimensions)

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

