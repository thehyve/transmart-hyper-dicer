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


Value = Union[
    str,
    float,
    Dict[str, Optional[Any]]
]


class Field(BaseModel):
    """
    Dimension properties
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
