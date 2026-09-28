import pytest
from pydantic import ValidationError

from app.domain import ProductV1, Scenario, Strategy, output_model_for
from clients.product_client import AdaptedProductClient, LegacyProductClient
from tests.helpers import request_target

STRATEGIES = list(Strategy)
SCENARIOS = list(Scenario)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert set(response.json()["strategies"]) == {"url", "header", "query"}


@pytest.mark.parametrize("strategy", STRATEGIES)
@pytest.mark.parametrize("scenario", SCENARIOS)
def test_legacy_v1_remains_compatible(client, strategy, scenario):
    legacy = LegacyProductClient(client, strategy=strategy, scenario=scenario)
    products = legacy.list_products()

    assert len(products) == 2
    assert products[0].nome == "Teclado mecânico"
    assert products[0].estoque == 12


@pytest.mark.parametrize("strategy", STRATEGIES)
@pytest.mark.parametrize("scenario", SCENARIOS)
def test_v2_contract_matches_scenario(client, strategy, scenario):
    path, kwargs = request_target(strategy, scenario, 2)
    response = client.get(path, **kwargs)

    assert response.status_code == 200
    model = output_model_for(scenario, 2)
    products = [model.model_validate(item) for item in response.json()]
    assert len(products) == 2

    fields = set(response.json()[0])
    expected = {
        Scenario.C1: {"id", "descricao", "preco", "estoque"},
        Scenario.C2: {"id", "nome", "preco"},
        Scenario.C3: {"id", "nome", "preco", "estoque", "categoria"},
    }[scenario]
    assert fields == expected


@pytest.mark.parametrize("strategy", STRATEGIES)
@pytest.mark.parametrize("scenario", SCENARIOS)
def test_adapted_client_creates_v2_product(client, strategy, scenario):
    adapted = AdaptedProductClient(client, strategy=strategy, scenario=scenario)
    product = adapted.create_product()
    assert product.id == 3


@pytest.mark.parametrize("strategy", STRATEGIES)
@pytest.mark.parametrize("scenario", [Scenario.C1, Scenario.C2])
def test_legacy_validation_detects_silent_break_on_forced_v2(
    client,
    strategy,
    scenario,
):
    path, kwargs = request_target(strategy, scenario, 2)
    response = client.get(path, **kwargs)

    assert response.status_code == 200
    with pytest.raises(ValidationError):
        ProductV1.model_validate(response.json()[0])


@pytest.mark.parametrize("strategy", STRATEGIES)
def test_c3_legacy_post_to_v2_is_explicit_failure(client, strategy):
    path, kwargs = request_target(strategy, Scenario.C3, 2)
    response = client.post(
        path,
        json={"nome": "Produto legado", "preco": 10.0, "estoque": 1},
        **kwargs,
    )
    assert response.status_code == 422


def test_header_requires_supported_accept(client):
    response = client.get("/api/header/c1/produtos")
    assert response.status_code == 406


def test_query_requires_version(client):
    response = client.get("/api/query/c1/produtos")
    assert response.status_code == 422


def test_url_rejects_unsupported_version(client):
    response = client.get("/api/url/c1/v3/produtos")
    assert response.status_code == 400
