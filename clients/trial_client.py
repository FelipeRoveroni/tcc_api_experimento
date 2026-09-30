"""Cliente de ensaio migrado para v2 no cenário C3 por URL.

Em cada nova rodada, parta do mesmo commit v1 registrado como BASE.
"""

from __future__ import annotations

from typing import Any

from app.domain import ProductC3V2, Scenario, Strategy
from clients.product_client import HttpClient


class TrialProductClient:
    def __init__(self, http: HttpClient, *, strategy: Strategy, scenario: Scenario):
        self.http = http
        self.strategy = strategy
        self.scenario = scenario

    def _target(self) -> tuple[str, dict[str, Any]]:
        """Seleciona v2 por URL na rodada URL/C3."""
        if self.strategy is Strategy.URL:
            return f"/api/url/{self.scenario.value}/v2/produtos", {}
        if self.strategy is Strategy.HEADER:
            return (
                f"/api/header/{self.scenario.value}/produtos",
                {"headers": {"Accept": "application/vnd.tcc.produto.v1+json"}},
            )
        return (
            f"/api/query/{self.scenario.value}/produtos",
            {"params": {"version": 1}},
        )

    def list_products(self) -> list[ProductC3V2]:
        path, kwargs = self._target()
        response = self.http.get(path, **kwargs)
        response.raise_for_status()
        return [ProductC3V2.model_validate(item) for item in response.json()]

    def get_product(self, product_id: int) -> ProductC3V2:
        path, kwargs = self._target()
        response = self.http.get(f"{path}/{product_id}", **kwargs)
        response.raise_for_status()
        return ProductC3V2.model_validate(response.json())

    def create_product(
        self, *, nome: str, preco: float, estoque: int, categoria: str
    ) -> ProductC3V2:
        path, kwargs = self._target()
        response = self.http.post(
            path,
            json={
                "nome": nome,
                "preco": preco,
                "estoque": estoque,
                "categoria": categoria,
            },
            **kwargs,
        )
        response.raise_for_status()
        return ProductC3V2.model_validate(response.json())
