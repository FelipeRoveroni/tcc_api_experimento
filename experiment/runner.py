from __future__ import annotations

import argparse
import csv
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.domain import ProductV1, Scenario, Strategy, output_model_for
from app.main import app, repository
from clients.product_client import (
    AdaptedProductClient,
    LegacyProductClient,
    ProductClient,
)

FIELDNAMES = (
    "execucao_id",
    "data_hora_utc",
    "estrategia",
    "cenario",
    "legado_v1_status_http",
    "legado_v1_contrato_valido",
    "legado_forcado_v2_status_http",
    "legado_forcado_v2_contrato_valido",
    "falhas_explicitas",
    "erros_silenciosos",
    "adaptado_v2_status_http",
    "adaptado_v2_contrato_valido",
    "compatibilidade_legado_percentual",
)


def _legacy_contract_is_valid(payload: object) -> bool:
    try:
        if isinstance(payload, list):
            for item in payload:
                ProductV1.model_validate(item)
        else:
            ProductV1.model_validate(payload)
    except ValidationError:
        return False
    return True


def execute() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with TestClient(app) as http:
        for strategy in Strategy:
            for scenario in Scenario:
                repository.reset()

                legacy = LegacyProductClient(
                    http,
                    strategy=strategy,
                    scenario=scenario,
                )
                legacy_response = legacy.list_raw()
                legacy_contract_ok = (
                    legacy_response.is_success
                    and _legacy_contract_is_valid(legacy_response.json())
                )

                forced = ProductClient(
                    http,
                    strategy=strategy,
                    scenario=scenario,
                    version=2,
                )
                if scenario is Scenario.C3:
                    forced_response = forced.create_raw(
                        {
                            "nome": "Produto legado",
                            "preco": 99.90,
                            "estoque": 3,
                        }
                    )
                    forced_contract_ok = False
                else:
                    forced_response = forced.list_raw()
                    forced_contract_ok = (
                        forced_response.is_success
                        and _legacy_contract_is_valid(forced_response.json())
                    )

                explicit_failures = int(not forced_response.is_success)
                silent_errors = int(
                    forced_response.is_success and not forced_contract_ok
                )

                adapted = AdaptedProductClient(
                    http,
                    strategy=strategy,
                    scenario=scenario,
                )
                adapted_response = adapted.create_raw(
                    {
                        Scenario.C1: {
                            "descricao": "Produto adaptado",
                            "preco": 109.90,
                            "estoque": 4,
                        },
                        Scenario.C2: {
                            "nome": "Produto adaptado",
                            "preco": 109.90,
                        },
                        Scenario.C3: {
                            "nome": "Produto adaptado",
                            "preco": 109.90,
                            "estoque": 4,
                            "categoria": "Teste",
                        },
                    }[scenario]
                )
                adapted_contract_ok = False
                if adapted_response.is_success:
                    model = output_model_for(scenario, 2)
                    try:
                        model.model_validate(adapted_response.json())
                    except ValidationError:
                        adapted_contract_ok = False
                    else:
                        adapted_contract_ok = True

                rows.append(
                    {
                        "execucao_id": str(uuid4()),
                        "data_hora_utc": datetime.now(UTC).isoformat(),
                        "estrategia": strategy.value,
                        "cenario": scenario.value,
                        "legado_v1_status_http": legacy_response.status_code,
                        "legado_v1_contrato_valido": legacy_contract_ok,
                        "legado_forcado_v2_status_http": forced_response.status_code,
                        "legado_forcado_v2_contrato_valido": forced_contract_ok,
                        "falhas_explicitas": explicit_failures,
                        "erros_silenciosos": silent_errors,
                        "adaptado_v2_status_http": adapted_response.status_code,
                        "adaptado_v2_contrato_valido": adapted_contract_ok,
                        "compatibilidade_legado_percentual": (
                            100.0 if legacy_contract_ok else 0.0
                        ),
                    }
                )
    return rows


def save_csv(rows: list[dict[str, object]], output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa o experimento do TCC.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results")
        / f"experimento_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.csv",
    )
    args = parser.parse_args()
    output = save_csv(execute(), args.output)
    print(output.resolve())


if __name__ == "__main__":
    main()
