from database import Database
from models import Flower, Recipe, Ingredient, RecipeResult


class RecipeEngine:
    """
    Core recipe resolver for Sunflower Land flower database.

    Time calculation follows Step 1 decision:
    only flower growth time is used.
    Ingredient production time is ignored.
    """

    def __init__(self, db_path="flower.db"):
        self.db = Database(db_path)

    def find_flower(self, name):
        row = self.db.fetch_one(
            """
            SELECT id, name, base_time_seconds
            FROM flowers
            WHERE lower(name)=lower(?)
            """,
            (name,)
        )

        if not row:
            return None

        return Flower(
            id=row["id"],
            name=row["name"],
            base_time_seconds=row["base_time_seconds"]
        )

    def get_recipes(self, flower_id):
        rows = self.db.fetch_all(
            """
            SELECT id, flower_id, verified, notes
            FROM recipes
            WHERE flower_id=?
            ORDER BY id
            """,
            (flower_id,)
        )

        return [
            Recipe(
                id=r["id"],
                flower_id=r["flower_id"],
                verified=r["verified"],
                notes=r["notes"]
            )
            for r in rows
        ]

    def get_recipe_ingredients(self, recipe_id):
        rows = self.db.fetch_all(
            """
            SELECT
                i.id,
                i.name,
                ri.quantity,
                ri.quantity_source
            FROM recipe_ingredients ri
            JOIN ingredients i
                ON i.id = ri.ingredient_id
            WHERE ri.recipe_id=?
            ORDER BY i.name
            """,
            (recipe_id,)
        )

        return [
            Ingredient(
                id=r["id"],
                name=r["name"],
                quantity=r["quantity"],
                quantity_source=r["quantity_source"]
            )
            for r in rows
        ]

    def build_dependency_graph(self, recipe_id):
        rows = self.db.fetch_all(
            """
            SELECT
                parent_item_id,
                child_item_id,
                parent_type,
                child_type
            FROM recipe_dependencies
            WHERE recipe_id=?
            """,
            (recipe_id,)
        )

        graph = {}

        for row in rows:
            parent = row["parent_item_id"]
            child = row["child_item_id"]

            graph.setdefault(parent, [])
            graph[parent].append(child)

        return graph

    def calculate_fastest_route(self, flower):
        recipes = self.get_recipes(flower.id)

        if not recipes:
            return None

        # All routes have same flower growth time.
        # Select verified recipe first, then lowest id.
        recipes.sort(
            key=lambda r: (
                0 if r.verified else 1,
                r.id
            )
        )

        return recipes[0]

    def get_recipe(self, flower_name):
        flower = self.find_flower(flower_name)

        if not flower:
            return None

        recipes = self.get_recipes(flower.id)

        fastest = self.calculate_fastest_route(flower)

        return RecipeResult(
            flower=flower,
            recipes=recipes,
            fastest_recipe_id=fastest.id if fastest else None
        )

    def format_recipe(self, flower_name):
        result = self.get_recipe(flower_name)

        if not result:
            return f"Flower '{flower_name}' not found."

        output = []
        output.append(f"🌸 {result.flower.name}")

        if result.flower.base_time_seconds:
            days = result.flower.base_time_seconds // 86400
            output.append(f"⏱ Growth Time: {days} day(s)")

        output.append("")
        output.append(f"Recipes found: {len(result.recipes)}")

        for recipe in result.recipes:
            marker = "⚡" if recipe.id == result.fastest_recipe_id else " "
            output.append(f"{marker} Route {recipe.id}")

            for item in self.get_recipe_ingredients(recipe.id):
                output.append(
                    f"  - {item.name} x{item.quantity}"
                )

        return "\n".join(output)
