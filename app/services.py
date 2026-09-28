from __future__ import annotations

from typing import Any

from fastapi import HTTPException
from pydantic import ValidationError

from app.domain import (
    ProductC1V2Input,
    ProductC2V2Input,
    ProductC3V2Input,
    ProductRecord,
    ProductV1Input,
    Scenario,
    input_model_for,
    output_model_for,
)

SUPPORTED_VERSIONS = (1, 2)
HEADER_MEDIA_TYPES = {
    1: "application/vnd.tcc.produto.v1+json",
    2: "application/vnd.tcc.produto.v2+json",
}


def ensure_version(version: int) -> int:
    if version not in SUPPORTED_VERSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Versão {version} não suportada. Utilize 1 ou 2.",
        )
    return version


def version_from_accept(accept: str | None) -> int:
    normalized = (accept or "").split(";", maxsplit=1)[0].strip().lower()
    for version, media_type in HEADER_MEDIA_TYPES.items():
        if normalized == media_type:
            return version
    raise HTTPException(
        status_code=406,
        detail=(
            "Cabeçalho Accept ausente ou inválido. Valores aceitos: "
            + ", ".join(HEADER_MEDIA_TYPES.values())
        ),
    )


def serialize_product(
    product: ProductRecord,
    *,
    scenario: Scenario,
    version: int,
) -> dict[str, Any]:
    model = output_model_for(scenario, version)
    if version == 1:
        payload = {
            "id": product.id,
            "nome": product.nome,
            "preco": product.preco,
            "estoque": product.estoque,
        }
    elif scenario is Scenario.C1:
        payload = {
            "id": product.id,
            "descricao": product.nome,
            "preco": product.preco,
            "estoque": product.estoque,
        }
    elif scenario is Scenario.C2:
        payload = {
            "id": product.id,
            "nome": product.nome,
            "preco": product.preco,
        }
    else:
        payload = {
            "id": product.id,
            "nome": product.nome,
            "preco": product.preco,
            "estoque": product.estoque,
            "categoria": product.categoria,
        }
    return model.model_validate(payload).model_dump()


def parse_product_payload(
    payload: dict[str, Any],
    *,
    scenario: Scenario,
    version: int,
) -> dict[str, Any]:
    model = input_model_for(scenario, version)
    try:
        parsed = model.model_validate(payload)
    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail=exc.errors(include_url=False),
        ) from exc

    if isinstance(parsed, ProductV1Input):
        return {
            "nome": parsed.nome,
            "preco": parsed.preco,
            "estoque": parsed.estoque,
            "categoria": "Não informada",
        }
    if isinstance(parsed, ProductC1V2Input):
        return {
            "nome": parsed.descricao,
            "preco": parsed.preco,
            "estoque": parsed.estoque,
            "categoria": "Não informada",
        }
    if isinstance(parsed, ProductC2V2Input):
        return {
            "nome": parsed.nome,
            "preco": parsed.preco,
            "estoque": 0,
            "categoria": "Não informada",
        }
    if isinstance(parsed, ProductC3V2Input):
        return parsed.model_dump()
    raise AssertionError("Modelo de entrada não mapeado")
