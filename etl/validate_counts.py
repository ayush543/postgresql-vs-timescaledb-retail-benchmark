import psycopg2
import pandas as pd

DATABASES = {
    "postgres": "retail_benchmark",
    "timescale": "retail_timescale"
}

TABLES = [
    "departments",
    "aisles",
    "products",
    "orders",
    "order_products",
    "suppliers",
    "product_supplier",
    "reorder_rules",
    "inventory_snapshots"
]

DB_USER = "shukla"
DB_HOST = "localhost"
DB_PORT = "5432"


def get_count(db_name, table_name):
    conn = psycopg2.connect(
        dbname=db_name,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            return cursor.fetchone()[0]
    finally:
        conn.close()


def main():
    results = []

    for table in TABLES:
        postgres_count = get_count(DATABASES["postgres"], table)
        timescale_count = get_count(DATABASES["timescale"], table)

        results.append({
            "table": table,
            "postgres_count": postgres_count,
            "timescale_count": timescale_count,
            "match": postgres_count == timescale_count
        })

    df = pd.DataFrame(results)
    print(df.to_string(index=False))

    if df["match"].all():
        print("\nValidation passed: row counts match.")
    else:
        print("\nValidation failed: row counts do not match.")


if __name__ == "__main__":
    main()
