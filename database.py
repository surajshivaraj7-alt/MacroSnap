import sqlite3
from datetime import date

DB_NAME = "macrosnap.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_date TEXT NOT NULL,
            meal_name TEXT,
            calories REAL,
            protein REAL,
            carbs REAL,
            fat REAL
        )
    """)

    conn.commit()

    try:
        conn.execute("ALTER TABLE meals ADD COLUMN meal_name TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    conn.close()
  


def add_meal(meal_name, calories, protein, carbs, fat):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO meals
        (meal_date, meal_name, calories, protein, carbs, fat)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            str(date.today()),
            meal_name,
            calories,
            protein,
            carbs,
            fat
        )
    )

    conn.commit()
    conn.close()


def get_today_meals():
    conn = get_connection()

    meals = conn.execute(
        """
        SELECT calories, protein, carbs, fat
        FROM meals
        WHERE meal_date = ?
        """,
        (str(date.today()),)
    ).fetchall()

    conn.close()

    return meals

# -----------------------------
# MEAL HISTORY
# -----------------------------

def get_meal_history():
    conn = get_connection()

    meals = conn.execute(
        """
        SELECT meal_date, meal_name, calories, protein, carbs, fat
        FROM meals
        ORDER BY meal_date DESC, id DESC
        """
    ).fetchall()

    conn.close()

    return meals


# -----------------------------
# WEEKLY MEALS
# -----------------------------

def get_weekly_meals():
    conn = get_connection()

    meals = conn.execute(
        """
        SELECT meal_date, calories, protein, carbs, fat
        FROM meals
        WHERE meal_date >= date('now', '-6 days')
        ORDER BY meal_date ASC
        """
    ).fetchall()

    conn.close()

    return meals

