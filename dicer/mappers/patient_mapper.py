from typing import Dict, List

from transmart_loader.transmart import Patient, IdentifierMapping, Relation, RelationType, Visit

from dicer.mappers.mapper_helper import DataInconsistencyException
from dicer.transmart import PatientDimensionElement, Relation as RelationObject, Value, VisitDimensionElement


class PatientMapper:
    """
    Map patient dimension elements and patient relations from query results to transmart-loader objects
    """

    def __init__(self):
        self.patient_id_to_patient_identifier: Dict[int, str] = {}
        self.patients = []

    def map_patient(self, patient_dimension_element: PatientDimensionElement) -> Patient:
        if not patient_dimension_element.subjectIds or 'SUBJ_ID' not in patient_dimension_element.subjectIds:
            raise DataInconsistencyException('Missing SUBJ_ID mapping for patient with id {}'
                                             .format(patient_dimension_element.id))

        self.patient_id_to_patient_identifier[
            patient_dimension_element.id] = patient_dimension_element.subjectIds['SUBJ_ID']

        return Patient(
            patient_dimension_element.subjectIds['SUBJ_ID'],
            patient_dimension_element.sex,
            list(map(lambda kv: IdentifierMapping(kv[0], kv[1]), patient_dimension_element.subjectIds.items()))
        )

    def map_patient_relation(self, relation: RelationObject, relation_types: List[RelationType],
                             left: Patient, right: Patient) -> Relation:
        relation_type = next((x for x in relation_types if x.label == relation.relationTypeLabel), None)
        if not relation_type:
            raise DataInconsistencyException('Relation {} does not exist.'.format(relation.relationTypeLabel))

        return Relation(
            left,
            relation_type,
            right,
            relation.biological,
            relation.shareHousehold
        )

    def map_patient_visit(self, visit: VisitDimensionElement) -> Visit:
        if not visit.encounterIds or 'VISIT_ID' not in visit.encounterIds:
            raise DataInconsistencyException('Missing visit encounter ID')
        visit_encounter_id = visit.encounterIds['VISIT_ID']

        patient = next(filter(lambda x: x.identifier == self.patient_id_to_patient_identifier[visit.patientId],
                              self.patients), None)
        if not patient:
            raise DataInconsistencyException('Missing patient for visit {}'.format(visit_encounter_id))

        return Visit(
            patient,
            visit_encounter_id,
            visit.activeStatusCd,
            visit.startDate,
            visit.endDate,
            visit.inoutCd,
            visit.locationCd,
            visit.lengthOfStay,
            list(map(lambda kv: IdentifierMapping(kv[0], kv[1]), visit.encounterIds.items()))
        )

    def map_patient_visits(self, visit_dim_elements: List[Value]) -> List[Visit]:
        return list(map(lambda x: self.map_patient_visit(VisitDimensionElement(**x)), visit_dim_elements))

    def map_patient_relations(self, relation_objects: List[RelationObject], relation_types: List[RelationType]):
        relations = []
        for relation_object in relation_objects:
            left = next((x for x in self.patients if x.identifier == self.patient_id_to_patient_identifier.get(
                relation_object.leftSubjectId)), None)
            right = next((x for x in self.patients if x.identifier == self.patient_id_to_patient_identifier.get(
                relation_object.rightSubjectId)), None)

            if not left or not right:
                continue

            relations.append(self.map_patient_relation(relation_object, relation_types, left, right))

        return relations

    def map_patients(self, patient_dim_elements: List[Value]) -> List[Patient]:
        self.patients = list(map(lambda x: self.map_patient(PatientDimensionElement(**x)),
                                 patient_dim_elements))
        return self.patients
