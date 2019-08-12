from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Schema
from typing import Sequence, Optional, Dict, Union, Any


class ObservedValueType(str, Enum):
    Numeric = 'NUMERIC'
    Categorical = 'CATEGORICAL'
    Text = 'TEXT'
    Date = 'DATE'
    Unknown = 'UNKNOWN'
    Study = 'STUDY'
    HighDim = 'HIGH_DIMENSIONAL'
    CategoricalOption = 'CATEGORICAL_OPTION'
    Folder = 'FOLDER'
    Modifier = 'MODIFIER'


class VisualAttributes(str, Enum):
    Folder = 'FOLDER'
    Container = 'CONTAINER'
    Multiple = 'MULTIPLE'
    Leaf = 'LEAF'
    ModifierContainer = 'MODIFIER_CONTAINER'
    ModifierFolder = 'MODIFIER_FOLDER'
    ModifierLeaf = 'MODIFIER_LEAF'
    Active = 'ACTIVE'
    Inactive = 'INACTIVE'
    Hidden = 'HIDDEN'
    Editable = 'EDITABLE'
    HighDim = 'HIGH_DIMENSIONAL'
    Numerical = 'NUMERICAL'
    Text = 'TEXT'
    Date = 'DATE'
    Categorical = 'CATEGORICAL'
    CategoricalOption = 'CATEGORICAL_OPTION'
    Study = 'STUDY'
    Program = 'PROGRAM'


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
    modifierCode: Optional[str]


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
    id: int
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


class VisitDimensionElement(BaseModel):
    """
    Patient visit properties
    """
    patientId: int
    activeStatusCd: Optional[str]
    startDate: Optional[datetime]
    endDate: Optional[datetime]
    inoutCd: Optional[str]
    locationCd: Optional[str]
    encounterIds: Dict[str, str]
    lengthOfStay: Optional[int]


class TrialVisitDimensionElement(BaseModel):
    """
    Trial visit properties
    """
    relTimeLabel: str
    relTimeUnit: Optional[str]
    relTime: Optional[int]
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
    children: Sequence[Any] = []
    name: str
    visualAttributes: Sequence[VisualAttributes]
    conceptCode: Optional[str]
    type: ObservedValueType
    studyId: Optional[str]
    metadata: Optional[Dict[str, Value]]


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
    leftSubjectId: int
    relationTypeLabel: str
    rightSubjectId: int
    biological: Optional[bool]
    shareHousehold: Optional[bool]


class Relations(BaseModel):
    """
    relations response model
    """
    relations: Sequence[Relation]

