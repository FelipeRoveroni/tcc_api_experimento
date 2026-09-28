from typing import Any

from app.domain import Scenario, Strategy
from app.services import HEADER_MEDIA_TYPES


def request_target(
    strategy: Strategy,
    scenario: Scenario,
    version: int,
) -> tuple[str, dict[str, Any]]:
    if strategy is Strategy.URL:
        return f"/api/url/{scenario.value}/v{version}/produtos", {}
    if strategy is Strategy.HEADER:
        return (
            f"/api/header/{scenario.value}/produtos",
            {"headers": {"Accept": HEADER_MEDIA_TYPES[version]}},
        )
    return (
        f"/api/query/{scenario.value}/produtos",
        {"params": {"version": version}},
    )
