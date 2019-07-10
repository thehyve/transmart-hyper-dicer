from datetime import date
from enum import Enum

from pydantic import BaseModel, Schema
from typing import Sequence, Optional, Dict, Union, Any


class DimensionType(str, Enum):
    Subject = 'subject'
    Attribute = 'attribute'


class ValueType(str, Enum):
    String = 'String'
    Int = 'Int'
    Double = 'Double'
    Timestamp = 'Timestamp'
    Map = 'Object'


class SortOrder(str, Enum):
    Asc = 'asc'
    Desc = 'desc'
    NONE = 'none'


class Sex(str, Enum):
    Male = 'male'
    Female = 'female'
    Unknown = 'unknown'


Value = Union[
    str,
    float,
    Dict[str, Optional[Any]]
]


class Field(BaseModel):
    """
    Dimension object field properties
    """
    name: str
    type: Optional[ValueType]


class DimensionDeclaration(BaseModel):
    """
    Dimension properties
    """
    name: str
    dimensionType: Optional[str]
    sortIndex: Optional[int]
    valueType: Optional[str]
    objectFields: Optional[Sequence[Field]] = Schema(None, alias='fields')
    inline: Optional[bool]


class SortDeclaration(BaseModel):
    """
    Sort specification
    """
    dimension: str
    sortOrder: SortOrder


class Cell(BaseModel):
    """
    Observation data cell
    """
    inlineDimensions: Sequence[Optional[Value]]
    dimensionIndexes: Sequence[Optional[int]]
    numericValue: Optional[float]
    stringValue: Optional[str]


class Hypercube(BaseModel):
    """
    Hypercube response model
    """
    dimensionDeclarations: Sequence[DimensionDeclaration]
    sort: Sequence[SortDeclaration]
    cells: Sequence[Cell]
    dimensionElements: Dict[str, Sequence[Optional[Value]]]


class PatientDimensionElement(BaseModel):
    """
    Patient properties
    """
    id: str
    sex: Sex
    subjectIds: Dict[str, str]


class ConceptDimensionElement(BaseModel):
    """
    Concept properties
    """
    conceptCode: str
    name: str
    conceptPath: str


class StudyDimensionElement(BaseModel):
    """
    Study properties
    """
    name: str
    # metadata: Optional[dict[str, str]]


class VisitDimensionElement(BaseModel):
    """
    Patient visit properties
    """
    encounterNum: str
    activeStatusCd: Optional[str]
    startDate: Optional[date]
    endDate: Optional[date]
    inoutCd: Optional[str]
    locationCd: Optional[str]
    encounterIds: Dict[str, str]


class TrialVisitDimensionElement(BaseModel):
    """
    Trial visit properties
    """
    relTimeLabel: str
    relTimeUnit: Optional[str]
    relTime: Optional[str]
    studyId: str


class Dimension(BaseModel):
    """
    Dimension metadata
    """
    name: str
    dimensionType: Optional[DimensionType]
    sortIndex: Optional[int]
    valueType: Optional[ValueType]
    modifierCode: Optional[str]


class Dimensions(BaseModel):
    """
    Dimensions response model
    """
    dimensions: Sequence[Dimension]


class TreeNode(BaseModel):
    """
    Ontology node
    """
    parent: Optional[Any] = None
    name: str
    children: Sequence[Any] = []


class TreeNodes(BaseModel):
    """
    Tree nodes response model
    """
    tree_nodes: Sequence[TreeNode]


class Study(BaseModel):
    """
    Study properties
    """
    studyId: str
    metadata: Optional[Dict[str, Any]]


class Studies(BaseModel):
    """
    studies response model
    """
    studies: Sequence[Study]


class RelationType(BaseModel):
    """
    Relation type
    """
    label: str
    description: Optional[str]
    symmetrical: Optional[bool]
    biological: Optional[bool]


class RelationTypes(BaseModel):
    """
    relation types response model
    """
    relationTypes: Sequence[RelationType]


class Relation(BaseModel):
    """
    Binary relation between patients
    """
    leftSubjectId: str
    relationTypeLabel: str
    rightSubjectId: str
    biological: Optional[bool]
    shareHousehold: Optional[bool]


class Relations(BaseModel):
    """
    relations response model
    """
    relations: Sequence[Relation]

