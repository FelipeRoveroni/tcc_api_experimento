"""Critérios v2: executar explicitamente para uma estratégia e um cenário.

Este arquivo não começa com test_ para não entrar em ``pytest -q`` antes da
migração. Ele deve falhar sobre o cliente de ensaio v1 e passar após a adaptação.
"""

import pytest

from app.domain import Scenario, output_model_for
from clients.trial_client import TrialProductClient
from tests.helpers import request_target

SEED_V2 = {
    Scenario.C1: {
        "id": 1,
        "descricao": "Teclado mecânico",
        "preco": 349.90,
        "estoque": 12,
    },
    Scenario.C2: {"id": 1, "nome": "Teclado mecânico", "preco": 349.90},
    Scenario.C3: {
        "id": 1,
        "nome": "Teclado mecânico",
        "preco": 349.90,
        "estoque": 12,
        "categoria": "Periféricos",
    },
}

SECOND_V2 = {
    Scenario.C1: {
        "id": 2,
        "descricao": "Mouse sem fio",
        "preco": 159.90,
        "estoque": 25,
    },
    Scenario.C2: {"id": 2, "nome": "Mouse sem fio", "preco": 159.90},
    Scenario.C3: {
        "id": 2,
        "nome": "Mouse sem fio",
        "preco": 159.90,
        "estoque": 25,
        "categoria": "Periféricos",
    },
}

CREATION_V2 = {
    Scenario.C1: {
        "descricao": "Monitor ultrawide",
        "preco": 1899.90,
        "estoque": 7,
    },
    Scenario.C2: {"nome": "Monitor ultrawide", "preco": 1899.90},
    Scenario.C3: {
        "nome": "Monitor ultrawide",
        "preco": 1899.90,
        "estoque": 7,
        "categoria": "Monitores",
    },
}


@pytest.fixture()
def trial(client, migration_target):
    strategy, scenario = migration_target
    return TrialProductClient(client, strategy=strategy, scenario=scenario)


def assert_v2_product(product, scenario, expected):
    assert isinstance(product, output_model_for(scenario, 2))
    assert product.model_dump() == expected


def test_lists_v2(trial, migration_target):
    strategy, scenario = migration_target
    assert trial._target() == request_target(strategy, scenario, 2)
    products = trial.list_products()

    assert len(products) == 2
    assert_v2_product(products[0], scenario, SEED_V2[scenario])
    assert_v2_product(products[1], scenario, SECOND_V2[scenario])


def test_gets_v2_by_id(trial, migration_target):
    strategy, scenario = migration_target
    assert trial._target() == request_target(strategy, scenario, 2)
    product = trial.get_product(1)

    assert_v2_product(product, scenario, SEED_V2[scenario])


def test_creates_v2(trial, migration_target):
    strategy, scenario = migration_target
    assert trial._target() == request_target(strategy, scenario, 2)
    product = trial.create_product(**CREATION_V2[scenario])

    assert_v2_product(product, scenario, {"id": 3, **CREATION_V2[scenario]})
    assert_v2_product(trial.get_product(3), scenario, product.model_dump())
