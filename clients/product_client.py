from __future__ import annotations

from typing import Any, Protocol

from app.domain import ProductV1, Scenario, Strategy, output_model_for
from app.services import HEADER_MEDIA_TYPES


class HttpClient(Protocol):
    def get(self, url: str, **kwargs: Any): ...
    def post(self, url: str, **kwargs: Any): ...


class ProductClient:
    """Cliente configurável, compartilhado entre execução local e testes."""

    def __init__(
        self,
        http: HttpClient,
        *,
        strategy: Strategy,
        scenario: Scenario,
        version: int,
    ) -> None:
        self.http = http
        self.strategy = strategy
        self.scenario = scenario
        self.version = version

    def _target(self) -> tuple[str, dict[str, Any]]:
        if self.strategy is Strategy.URL:
            return (
                f"/api/url/{self.scenario.value}/v{self.version}/produtos",
                {},
            )
        if self.strategy is Strategy.HEADER:
            return (
                f"/api/header/{self.scenario.value}/produtos",
                {"headers": {"Accept": HEADER_MEDIA_TYPES[self.version]}},
            )
        return (
            f"/api/query/{self.scenario.value}/produtos",
            {"params": {"version": self.version}},
        )

    def list_raw(self):
        path, kwargs = self._target()
        return self.http.get(path, **kwargs)

    def create_raw(self, payload: dict[str, Any]):
        path, kwargs = self._target()
        return self.http.post(path, json=payload, **kwargs)


class LegacyProductClient(ProductClient):
    def __init__(self, http: HttpClient, *, strategy: Strategy, scenario: Scenario):
        super().__init__(
            http,
            strategy=strategy,
            scenario=scenario,
            version=1,
        )

    def list_products(self) -> list[ProductV1]:
        response = self.list_raw()
        response.raise_for_status()
        return [ProductV1.model_validate(item) for item in response.json()]

    def create_product(self, *, nome: str, preco: float, estoque: int) -> ProductV1:
        response = self.create_raw({"nome": nome, "preco": preco, "estoque": estoque})
        response.raise_for_status()
        return ProductV1.model_validate(response.json())


class AdaptedProductClient(ProductClient):
    def __init__(self, http: HttpClient, *, strategy: Strategy, scenario: Scenario):
        super().__init__(
            http,
            strategy=strategy,
            scenario=scenario,
            version=2,
        )

    def list_products(self):
        response = self.list_raw()
        response.raise_for_status()
        model = output_model_for(self.scenario, 2)
        return [model.model_validate(item) for item in response.json()]

    def create_product(self):
        payloads = {
            Scenario.C1: {
                "descricao": "Monitor ultrawide",
                "preco": 1899.90,
                "estoque": 7,
            },
            Scenario.C2: {
                "nome": "Monitor ultrawide",
                "preco": 1899.90,
            },
            Scenario.C3: {
                "nome": "Monitor ultrawide",
                "preco": 1899.90,
                "estoque": 7,
                "categoria": "Monitores",
            },
        }
        response = self.create_raw(payloads[self.scenario])
        response.raise_for_status()
        model = output_model_for(self.scenario, 2)
        return model.model_validate(response.json())
