import psycopg2
from pathlib import Path

DB_NAME = "retail_benchmark"
DB_USER = "shukla"
DB_HOST = "localhost"
DB_PORT = "5432"

BASE_DIR = Path(__file__).resolve().parents[1]

FILES = [
    ("departments", BASE_DIR / "data/raw/instacart/departments.csv"),
    ("aisles", BASE_DIR / "data/raw/instacart/aisles.csv"),
    ("products", BASE_DIR / "data/raw/instacart/products.csv"),
    ("orders", BASE_DIR / "data/raw/instacart/orders.csv"),
    ("order_products", BASE_DIR / "data/processed/order_products.csv"),
    ("suppliers", BASE_DIR / "data/synthetic/suppliers.csv"),
    ("product_supplier", BASE_DIR / "data/synthetic/product_supplier.csv"),
    ("reorder_rules", BASE_DIR / "data/synthetic/reorder_rules.csv"),
]

INVENTORY_FILE = BASE_DIR / "data/synthetic/inventory_snapshots.csv"


def copy_table(cursor, table_name, file_path):
    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")

    print(f"Loading {table_name} from {file_path}")

    with open(file_path, "r") as file:
        cursor.copy_expert(
            f"""
            COPY {table_name}
            FROM STDIN
            WITH CSV HEADER DELIMITER ','
            """,
            file
        )


def copy_inventory(cursor):
    if not INVENTORY_FILE.exists():
        raise FileNotFoundError(f"Missing file: {INVENTORY_FILE}")

    print(f"Loading inventory_snapshots from {INVENTORY_FILE}")

    with open(INVENTORY_FILE, "r") as file:
        cursor.copy_expert(
            """
            COPY inventory_snapshots
            (product_id, warehouse_id, stock_quantity, reorder_threshold, inventory_timestamp, supplier_id)
            FROM STDIN
            WITH CSV HEADER DELIMITER ','
            """,
            file
        )


def main():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )

    try:
        with conn:
            with conn.cursor() as cursor:
                for table_name, file_path in FILES:
                    copy_table(cursor, table_name, file_path)

                copy_inventory(cursor)

        print("PostgreSQL load complete.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
