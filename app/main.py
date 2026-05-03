from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="Retail Benchmark Secure API")

DB_CONFIG = {
    "dbname": "retail_benchmark",
    "user": "app_user",
    "password": "app_password",
    "host": "localhost",
    "port": 5432,
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


@app.get("/products/{product_id}")
def get_product(product_id: int):
    query = """
        SELECT product_id, product_name, aisle_id, department_id
        FROM products
        WHERE product_id = %s
    """

    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (product_id,))
                result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="Product not found")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/inventory/{product_id}")
def get_inventory(product_id: int):
    query = """
        SELECT product_id, warehouse_id, stock_quantity, inventory_timestamp
        FROM inventory_snapshots
        WHERE product_id = %s
        ORDER BY inventory_timestamp DESC
        LIMIT 20
    """

    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (product_id,))
                result = cursor.fetchall()

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
