import sqlite3


conn = sqlite3.connect("flower.db")

tables = [
    "flowers",
    "seeds",
    "ingredients",
    "recipes",
    "recipe_ingredients",
    "recipe_dependencies"
]


for table in tables:
    result = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()

    print(
        table,
        "=",
        result[0]
    )


conn.close()

import sqlite3

conn = sqlite3.connect("flower.db")

cursor = conn.cursor()


cursor.execute("""
SELECT
    f.name,
    r.id
FROM flowers f
JOIN recipes r
ON f.id=r.flower_id
WHERE f.name='Blue Lavender'
""")


for row in cursor.fetchall():
    print(row)