"""Cliente de ensaio migrado para v2 no cenário C2 por cabeçalho.

Em cada nova rodada, parta do mesmo commit v1 registrado como BASE.
"""

from __future__ import annotations

from typing import Any

from app.domain import ProductC2V2, Scenario, Strategy
from clients.product_client import HttpClient


class TrialProductClient:
    def __init__(self, http: HttpClient, *, strategy: Strategy, scenario: Scenario):
        self.http = http
        self.strategy = strategy
        self.scenario = scenario

    def _target(self) -> tuple[str, dict[str, Any]]:
        """Seleciona v2 por cabeçalho na rodada Header/C2."""
        if self.strategy is Strategy.URL:
            return f"/api/url/{self.scenario.value}/v1/produtos", {}
        if self.strategy is Strategy.HEADER:
            return (
                f"/api/header/{self.scenario.value}/produtos",
                {"headers": {"Accept": "application/vnd.tcc.produto.v2+json"}},
            )
        return (
            f"/api/query/{self.scenario.value}/produtos",
            {"params": {"version": 1}},
        )

    def list_products(self) -> list[ProductC2V2]:
        path, kwargs = self._target()
        response = self.http.get(path, **kwargs)
        response.raise_for_status()
        return [ProductC2V2.model_validate(item) for item in response.json()]

    def get_product(self, product_id: int) -> ProductC2V2:
        path, kwargs = self._target()
        response = self.http.get(f"{path}/{product_id}", **kwargs)
        response.raise_for_status()
        return ProductC2V2.model_validate(response.json())

    def create_product(self, *, nome: str, preco: float) -> ProductC2V2:
        path, kwargs = self._target()
        response = self.http.post(path, json={"nome": nome, "preco": preco}, **kwargs)
        response.raise_for_status()
        return ProductC2V2.model_validate(response.json())
