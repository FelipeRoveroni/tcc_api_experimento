"""Comprova que o ponto inicial atende ao contrato v1 nas nove combinações."""

import pytest

from app.domain import ProductV1, Scenario, Strategy
from clients.trial_client import TrialProductClient
from tests.helpers import request_target


@pytest.mark.parametrize("strategy", list(Strategy))
@pytest.mark.parametrize("scenario", list(Scenario))
def test_trial_lists_v1(client, strategy, scenario):
    trial = TrialProductClient(client, strategy=strategy, scenario=scenario)

    assert trial._target() == request_target(strategy, scenario, 1)
    assert trial.list_products() == [
        ProductV1(id=1, nome="Teclado mecânico", preco=349.90, estoque=12),
        ProductV1(id=2, nome="Mouse sem fio", preco=159.90, estoque=25),
    ]


@pytest.mark.parametrize("strategy", list(Strategy))
@pytest.mark.parametrize("scenario", list(Scenario))
def test_trial_gets_v1_by_id(client, strategy, scenario):
    trial = TrialProductClient(client, strategy=strategy, scenario=scenario)

    assert trial.get_product(1) == ProductV1(
        id=1, nome="Teclado mecânico", preco=349.90, estoque=12
    )


@pytest.mark.parametrize("strategy", list(Strategy))
@pytest.mark.parametrize("scenario", list(Scenario))
def test_trial_creates_v1(client, strategy, scenario):
    trial = TrialProductClient(client, strategy=strategy, scenario=scenario)

    product = trial.create_product(nome="Monitor", preco=1899.90, estoque=7)

    assert product == ProductV1(id=3, nome="Monitor", preco=1899.90, estoque=7)
    assert trial.get_product(3) == product
