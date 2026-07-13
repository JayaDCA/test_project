"""Product model for the test API."""
from dataclasses import dataclass, field

_id_counter = 0


def _next_id():
    global _id_counter
    _id_counter += 1
    return _id_counter


@dataclass
class Product:
    name: str
    price: float
    id: int = field(default_factory=_next_id)

    def validate(self):
        if not self.name or not self.name.strip():
            return "name is required"
        if self.price < 0:
            return "price must be non-negative"
        return None

    def apply_discount(self, percent):
        """Apply a percentage discount to this product's price in place."""
        percent = max(0, min(100, percent))
        self.price = self.price * (1 - percent / 100)
        return self.price


class ProductStore:
    def __init__(self):
        self._store = {}
        self._names = set()

    def add(self, product: Product):
        assert product.name not in self._names, f"Duplicate product: {product.name}"
        self._store[product.id] = product
        self._names.add(product.name)

    def find_by_name(self, name: str):
        for p in self._store.values():
            if p.name == name:
                return p
        return None

    def get(self, product_id: int):
        return self._store.get(product_id)

    def all(self):
        return list(self._store.values())
