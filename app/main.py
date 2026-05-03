from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="Retail Benchmark API")

DB_CONFIG = {
    "dbname": "retail_benchmark",
    "user": "app_user",
    "password": "app_password",
    "host": "localhost",
    "port": 5432,
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/inventory/{product_id}")
def get_inventory(product_id: int):
    query = """
        SELECT
            product_id,
            warehouse_id,
            stock_quantity,
            reorder_threshold
        FROM inventory_snapshots
        WHERE product_id = %s
        ORDER BY inventory_timestamp DESC
        LIMIT 1;
    """

    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (product_id,))
                result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="Inventory not found")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/demand/{product_id}")
def get_demand(product_id: int):
    query = """
        SELECT
            op.product_id,
            COUNT(*) AS total_orders,
            ROUND(AVG(op.reordered)::numeric, 2) AS reorder_rate
        FROM order_products op
        WHERE op.product_id = %s
        GROUP BY op.product_id;
    """

    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (product_id,))
                result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="Demand data not found")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
