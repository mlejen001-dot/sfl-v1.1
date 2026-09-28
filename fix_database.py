import sqlite3
import shutil
from datetime import datetime

DB_FILE = "flower.db"
BACKUP_FILE = "flower_backup_before_migration.db"


def backup_database():
    shutil.copy2(DB_FILE, BACKUP_FILE)
    print(f"Backup created: {BACKUP_FILE}")


def migrate_recipe_flower_relation(conn):
    """
    Memperbaiki recipes.flower_id yang sebelumnya menggunakan
    urutan ekstraksi, bukan primary key flowers.id.
    """

    cursor = conn.cursor()

    flowers = cursor.execute("""
        SELECT id
        FROM flowers
        ORDER BY id
    """).fetchall()

    recipes = cursor.execute("""
        SELECT id, flower_id
        FROM recipes
        ORDER BY id
    """).fetchall()

    if not flowers or not recipes:
        raise Exception("flowers atau recipes kosong")

    groups = {}

    for recipe_id, old_flower_id in recipes:
        groups.setdefault(old_flower_id, [])
        groups[old_flower_id].append(recipe_id)

    fixed = 0

    for old_flower_id, recipe_ids in groups.items():

        if old_flower_id > len(flowers):
            print(
                "Warning: flower index tidak ditemukan:",
                old_flower_id
            )
            continue

        new_flower_id = flowers[old_flower_id - 1][0]

        for recipe_id in recipe_ids:
            cursor.execute("""
                UPDATE recipes
                SET flower_id=?
                WHERE id=?
            """, (new_flower_id, recipe_id))

            fixed += 1

    print("Recipe relation fixed:", fixed)


def update_flower_duration(conn):
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE flowers
        SET base_time_seconds = (
            SELECT MIN(route_time_seconds)
            FROM recipes
            WHERE recipes.flower_id = flowers.id
        )
        WHERE EXISTS (
            SELECT 1
            FROM recipes
            WHERE recipes.flower_id = flowers.id
        )
    """)

    print("Flower duration updated:", cursor.rowcount)


def validate(conn):

    cursor = conn.cursor()

    broken = cursor.execute("""
        SELECT COUNT(*)
        FROM recipes r
        LEFT JOIN flowers f
        ON r.flower_id=f.id
        WHERE f.id IS NULL
    """).fetchone()[0]

    lavender = cursor.execute("""
        SELECT
            f.id,
            f.name,
            COUNT(r.id)
        FROM flowers f
        LEFT JOIN recipes r
        ON f.id=r.flower_id
        WHERE f.name='Blue Lavender'
        GROUP BY f.id,f.name
    """).fetchone()

    print("\nVALIDATION")
    print("----------------")
    print("Broken recipe relation:", broken)
    print("Blue Lavender:", lavender)


def main():

    print("Starting migration...")

    backup_database()

    conn = sqlite3.connect(DB_FILE)

    try:
        migrate_recipe_flower_relation(conn)
        update_flower_duration(conn)

        conn.commit()

        validate(conn)

        print("Migration finished:", datetime.now())

    except Exception as error:
        conn.rollback()
        print("Migration failed:", error)
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
