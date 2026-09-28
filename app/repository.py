from __future__ import annotations

from threading import RLock

from app.domain import ProductRecord

INITIAL_PRODUCTS = (
    ProductRecord(
        id=1,
        nome="Teclado mecânico",
        preco=349.90,
        estoque=12,
        categoria="Periféricos",
    ),
    ProductRecord(
        id=2,
        nome="Mouse sem fio",
        preco=159.90,
        estoque=25,
        categoria="Periféricos",
    ),
)


class ProductRepository:
    """Repositório em memória para manter o experimento autocontido."""

    def __init__(self) -> None:
        self._lock = RLock()
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self._products = {
                product.id: product.model_copy(deep=True)
                for product in INITIAL_PRODUCTS
            }
            self._next_id = max(self._products) + 1

    def list(self) -> list[ProductRecord]:
        with self._lock:
            return [
                self._products[key].model_copy(deep=True)
                for key in sorted(self._products)
            ]

    def get(self, product_id: int) -> ProductRecord | None:
        with self._lock:
            product = self._products.get(product_id)
            return product.model_copy(deep=True) if product else None

    def create(
        self,
        *,
        nome: str,
        preco: float,
        estoque: int,
        categoria: str,
    ) -> ProductRecord:
        with self._lock:
            product = ProductRecord(
                id=self._next_id,
                nome=nome,
                preco=preco,
                estoque=estoque,
                categoria=categoria,
            )
            self._products[product.id] = product
            self._next_id += 1
            return product.model_copy(deep=True)
