"""Cliente v1 usado como ponto de partida das migrações medidas.

Em cada rodada, parta do mesmo commit e altere apenas este arquivo para v2.
Não copie a implementação de AdaptedProductClient: ela valida a API, mas não
representa o esforço de adaptação deste cliente.
"""

from __future__ import annotations

from typing import Any

from app.domain import ProductV1, Scenario, Strategy
from clients.product_client import HttpClient


class TrialProductClient:
    def __init__(self, http: HttpClient, *, strategy: Strategy, scenario: Scenario):
        self.http = http
        self.strategy = strategy
        self.scenario = scenario

    def _target(self) -> tuple[str, dict[str, Any]]:
        """Seletores v1: adapte somente o ramo da estratégia da rodada."""
        if self.strategy is Strategy.URL:
            return f"/api/url/{self.scenario.value}/v1/produtos", {}
        if self.strategy is Strategy.HEADER:
            return (
                f"/api/header/{self.scenario.value}/produtos",
                {"headers": {"Accept": "application/vnd.tcc.produto.v1+json"}},
            )
        return (
            f"/api/query/{self.scenario.value}/produtos",
            {"params": {"version": 1}},
        )

    def list_products(self) -> list[ProductV1]:
        path, kwargs = self._target()
        response = self.http.get(path, **kwargs)
        response.raise_for_status()
        return [ProductV1.model_validate(item) for item in response.json()]

    def get_product(self, product_id: int) -> ProductV1:
        path, kwargs = self._target()
        response = self.http.get(f"{path}/{product_id}", **kwargs)
        response.raise_for_status()
        return ProductV1.model_validate(response.json())

    def create_product(self, *, nome: str, preco: float, estoque: int) -> ProductV1:
        path, kwargs = self._target()
        response = self.http.post(
            path, json={"nome": nome, "preco": preco, "estoque": estoque}, **kwargs
        )
        response.raise_for_status()
        return ProductV1.model_validate(response.json())
