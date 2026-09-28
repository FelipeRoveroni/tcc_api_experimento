from __future__ import annotations

from enum import Enum
from typing import TypeAlias

from pydantic import BaseModel, ConfigDict, Field


class Scenario(str, Enum):
    """Alterações disruptivas avaliadas pelo experimento."""

    C1 = "c1"  # nome -> descricao
    C2 = "c2"  # remoção de estoque
    C3 = "c3"  # inclusão de categoria obrigatória


class Strategy(str, Enum):
    URL = "url"
    HEADER = "header"
    QUERY = "query"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ProductRecord(StrictModel):
    """Representação canônica interna, independente do contrato público."""

    id: int
    nome: str
    preco: float
    estoque: int
    categoria: str


class ProductV1Input(StrictModel):
    nome: str = Field(min_length=1, max_length=120)
    preco: float = Field(gt=0)
    estoque: int = Field(ge=0)


class ProductV1(ProductV1Input):
    id: int


class ProductC1V2Input(StrictModel):
    descricao: str = Field(min_length=1, max_length=120)
    preco: float = Field(gt=0)
    estoque: int = Field(ge=0)


class ProductC1V2(ProductC1V2Input):
    id: int


class ProductC2V2Input(StrictModel):
    nome: str = Field(min_length=1, max_length=120)
    preco: float = Field(gt=0)


class ProductC2V2(ProductC2V2Input):
    id: int


class ProductC3V2Input(StrictModel):
    nome: str = Field(min_length=1, max_length=120)
    preco: float = Field(gt=0)
    estoque: int = Field(ge=0)
    categoria: str = Field(min_length=1, max_length=80)


class ProductC3V2(ProductC3V2Input):
    id: int


InputModel: TypeAlias = type[
    ProductV1Input | ProductC1V2Input | ProductC2V2Input | ProductC3V2Input
]
OutputModel: TypeAlias = type[ProductV1 | ProductC1V2 | ProductC2V2 | ProductC3V2]


def input_model_for(scenario: Scenario, version: int) -> InputModel:
    if version == 1:
        return ProductV1Input
    return {
        Scenario.C1: ProductC1V2Input,
        Scenario.C2: ProductC2V2Input,
        Scenario.C3: ProductC3V2Input,
    }[scenario]


def output_model_for(scenario: Scenario, version: int) -> OutputModel:
    if version == 1:
        return ProductV1
    return {
        Scenario.C1: ProductC1V2,
        Scenario.C2: ProductC2V2,
        Scenario.C3: ProductC3V2,
    }[scenario]
