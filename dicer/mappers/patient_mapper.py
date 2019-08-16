from typing import Dict, List

from transmart_loader.transmart import Patient as TLPatient, IdentifierMapping as TLIdentifierMapping, \
    Relation as TLRelation, RelationType as TLRelationType, Visit as TLVisit

from dicer.data_exception import DataException
from dicer.transmart import PatientDimensionElement, Relation, Value, VisitDimensionElement


class PatientMapper:
    """
    Map patient dimension elements and patient relations from query results to transmart-loader objects
    """

    def __init__(self):
        self.patient_id_to_patient: Dict[int, TLPatient] = {}

    @staticmethod
    def identifier_mappings_from_id_map(id_map: Dict[str, str]):
        return list(map(lambda kv: TLIdentifierMapping(kv[0], kv[1]), id_map.items()))

    def map_patient(self, patient_dimension_element: PatientDimensionElement) -> TLPatient:
        if not patient_dimension_element.subjectIds or 'SUBJ_ID' not in patient_dimension_element.subjectIds:
            raise DataException('Missing SUBJ_ID mapping for patient with id {}'
                                .format(patient_dimension_element.id))

        patient = TLPatient(
            patient_dimension_element.subjectIds['SUBJ_ID'],
            patient_dimension_element.sex,
            self.identifier_mappings_from_id_map(patient_dimension_element.subjectIds)
        )
        self.patient_id_to_patient[patient_dimension_element.id] = patient

        return patient

    def map_patient_relation(self, relation: Relation, relation_types: List[TLRelationType],
                             left: TLPatient, right: TLPatient) -> TLRelation:
        relation_type = next((x for x in relation_types if x.label == relation.relationTypeLabel), None)
        if not relation_type:
            raise DataException('Relation {} does not exist.'.format(relation.relationTypeLabel))

        return TLRelation(
            left,
            relation_type,
            right,
            relation.biological,
            relation.shareHousehold
        )

    def map_patient_visit(self, visit: VisitDimensionElement) -> TLVisit:
        if not visit.encounterIds or 'VISIT_ID' not in visit.encounterIds:
            raise DataException('Missing visit encounter ID')
        visit_encounter_id = visit.encounterIds['VISIT_ID']

        patient = self.patient_id_to_patient.get(visit.patientId)
        if not patient:
            raise DataException('Missing patient for visit {}'.format(visit_encounter_id))

        return TLVisit(
            patient,
            visit_encounter_id,
            visit.activeStatusCd,
            visit.startDate,
            visit.endDate,
            visit.inoutCd,
            visit.locationCd,
            visit.lengthOfStay,
            self.identifier_mappings_from_id_map(visit.encounterIds)
        )

    def map_patient_visits(self, visit_dim_elements: List[Value]) -> List[TLVisit]:
        return list(map(lambda x: self.map_patient_visit(VisitDimensionElement(**x)), visit_dim_elements))

    def map_patient_relations(self, relation_objects: List[Relation], relation_types: List[TLRelationType]):
        relations: List[TLRelation] = []
        for relation_object in relation_objects:
            left = self.patient_id_to_patient.get(relation_object.leftSubjectId)
            right = self.patient_id_to_patient.get(relation_object.rightSubjectId)

            if not left or not right:
                continue

            relations.append(self.map_patient_relation(relation_object, relation_types, left, right))

        return relations

    def map_patients(self, patient_dim_elements: List[Value]) -> List[TLPatient]:
        return list(map(lambda x: self.map_patient(PatientDimensionElement(**x)), patient_dim_elements))
