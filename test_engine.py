from recipe_engine import RecipeEngine


def run_tests():
    engine = RecipeEngine("flower.db")

    print("TEST 1: Existing flower")
    result = engine.get_recipe("Blue Lavender")

    if result:
        print("PASS")
        print(engine.format_recipe("Blue Lavender"))
    else:
        print("FAIL")

    print("\nTEST 2: Unknown flower")
    result = engine.get_recipe("UNKNOWN FLOWER")

    if result is None:
        print("PASS")
    else:
        print("FAIL")


if __name__ == "__main__":
    run_tests()
def get_recipes(self, flower_id):

    print("SEARCH FLOWER ID:", flower_id)

    rows = self.db.fetch_all(
        """
        SELECT *
        FROM recipes
        WHERE flower_id=?
        """,
        (flower_id,)
    )

    print("FOUND:", len(rows))

    return rows
