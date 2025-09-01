from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    name: str
    url: str
    image: str | None
    price: float
    price_per_unit: str | None
    supermarket: str
