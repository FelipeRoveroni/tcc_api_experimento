import pytest
from fastapi.testclient import TestClient

from app.main import app, repository


def pytest_addoption(parser):
    parser.addoption(
        "--strategy",
        choices=("url", "header", "query"),
        help="Estratégia da rodada de migração (somente migration_acceptance.py).",
    )
    parser.addoption(
        "--scenario",
        choices=("c1", "c2", "c3"),
        help="Cenário da rodada de migração (somente migration_acceptance.py).",
    )


@pytest.fixture()
def client():
    repository.reset()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def migration_target(request):
    from app.domain import Scenario, Strategy

    strategy = request.config.getoption("--strategy")
    scenario = request.config.getoption("--scenario")
    if strategy is None or scenario is None:
        raise pytest.UsageError(
            "Informe --strategy=url|header|query e --scenario=c1|c2|c3 "
            "ao executar tests/migration_acceptance.py."
        )
    return Strategy(strategy), Scenario(scenario)
