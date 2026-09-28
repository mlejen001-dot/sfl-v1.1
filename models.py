from dataclasses import dataclass, field


@dataclass
class Flower:
    id: int
    name: str
    base_time_seconds: int | None


@dataclass
class Recipe:
    id: int
    flower_id: int
    verified: int
    notes: str | None = None


@dataclass
class Ingredient:
    id: int
    name: str
    quantity: int = 1
    quantity_source: str = "default_assumption"


@dataclass
class RecipeResult:
    flower: Flower
    recipes: list = field(default_factory=list)
    fastest_recipe_id: int | None = None
