from __future__ import annotations

from typing import Annotated, Any

from fastapi import Body, FastAPI, Header, HTTPException, Query, status
from fastapi.responses import JSONResponse

from app.domain import Scenario, Strategy
from app.repository import ProductRepository
from app.services import (
    HEADER_MEDIA_TYPES,
    ensure_version,
    parse_product_payload,
    serialize_product,
    version_from_accept,
)

app = FastAPI(
    title="API experimental de versionamento REST",
    version="1.0.0",
    description=(
        "Ambiente controlado para comparar versionamento por URL, cabeçalho "
        "HTTP e parâmetro de consulta em três cenários disruptivos."
    ),
)
repository = ProductRepository()


def _response(data: Any, *, strategy: Strategy, version: int, status_code: int = 200):
    media_type = (
        HEADER_MEDIA_TYPES[version]
        if strategy is Strategy.HEADER
        else "application/json"
    )
    return JSONResponse(content=data, status_code=status_code, media_type=media_type)


def _list_products(*, strategy: Strategy, scenario: Scenario, version: int):
    version = ensure_version(version)
    data = [
        serialize_product(product, scenario=scenario, version=version)
        for product in repository.list()
    ]
    return _response(data, strategy=strategy, version=version)


def _get_product(
    product_id: int,
    *,
    strategy: Strategy,
    scenario: Scenario,
    version: int,
):
    version = ensure_version(version)
    product = repository.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    data = serialize_product(product, scenario=scenario, version=version)
    return _response(data, strategy=strategy, version=version)


def _create_product(
    payload: dict[str, Any],
    *,
    strategy: Strategy,
    scenario: Scenario,
    version: int,
):
    version = ensure_version(version)
    normalized = parse_product_payload(payload, scenario=scenario, version=version)
    product = repository.create(**normalized)
    data = serialize_product(product, scenario=scenario, version=version)
    return _response(
        data,
        strategy=strategy,
        version=version,
        status_code=status.HTTP_201_CREATED,
    )


@app.get("/health", tags=["infraestrutura"])
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "strategies": [strategy.value for strategy in Strategy],
        "scenarios": [scenario.value for scenario in Scenario],
        "versions": [1, 2],
    }


# Estratégia 1: versão explícita no caminho da URL.
@app.get("/api/url/{scenario}/v{version}/produtos", tags=["URL"])
def list_by_url(scenario: Scenario, version: int):
    return _list_products(
        strategy=Strategy.URL,
        scenario=scenario,
        version=version,
    )


@app.get("/api/url/{scenario}/v{version}/produtos/{product_id}", tags=["URL"])
def get_by_url(scenario: Scenario, version: int, product_id: int):
    return _get_product(
        product_id,
        strategy=Strategy.URL,
        scenario=scenario,
        version=version,
    )


@app.post(
    "/api/url/{scenario}/v{version}/produtos",
    status_code=status.HTTP_201_CREATED,
    tags=["URL"],
)
def create_by_url(
    scenario: Scenario,
    version: int,
    payload: Annotated[dict[str, Any], Body()],
):
    return _create_product(
        payload,
        strategy=Strategy.URL,
        scenario=scenario,
        version=version,
    )


# Estratégia 2: versão negociada pelo cabeçalho Accept.
@app.get("/api/header/{scenario}/produtos", tags=["Cabeçalho"])
def list_by_header(
    scenario: Scenario,
    accept: Annotated[str | None, Header()] = None,
):
    version = version_from_accept(accept)
    return _list_products(
        strategy=Strategy.HEADER,
        scenario=scenario,
        version=version,
    )


@app.get("/api/header/{scenario}/produtos/{product_id}", tags=["Cabeçalho"])
def get_by_header(
    scenario: Scenario,
    product_id: int,
    accept: Annotated[str | None, Header()] = None,
):
    version = version_from_accept(accept)
    return _get_product(
        product_id,
        strategy=Strategy.HEADER,
        scenario=scenario,
        version=version,
    )


@app.post(
    "/api/header/{scenario}/produtos",
    status_code=status.HTTP_201_CREATED,
    tags=["Cabeçalho"],
)
def create_by_header(
    scenario: Scenario,
    payload: Annotated[dict[str, Any], Body()],
    accept: Annotated[str | None, Header()] = None,
):
    version = version_from_accept(accept)
    return _create_product(
        payload,
        strategy=Strategy.HEADER,
        scenario=scenario,
        version=version,
    )


# Estratégia 3: versão selecionada por parâmetro de consulta.
@app.get("/api/query/{scenario}/produtos", tags=["Parâmetro"])
def list_by_query(scenario: Scenario, version: Annotated[int, Query()]):
    return _list_products(
        strategy=Strategy.QUERY,
        scenario=scenario,
        version=version,
    )


@app.get("/api/query/{scenario}/produtos/{product_id}", tags=["Parâmetro"])
def get_by_query(
    scenario: Scenario,
    product_id: int,
    version: Annotated[int, Query()],
):
    return _get_product(
        product_id,
        strategy=Strategy.QUERY,
        scenario=scenario,
        version=version,
    )


@app.post(
    "/api/query/{scenario}/produtos",
    status_code=status.HTTP_201_CREATED,
    tags=["Parâmetro"],
)
def create_by_query(
    scenario: Scenario,
    version: Annotated[int, Query()],
    payload: Annotated[dict[str, Any], Body()],
):
    return _create_product(
        payload,
        strategy=Strategy.QUERY,
        scenario=scenario,
        version=version,
    )
