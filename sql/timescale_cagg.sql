DROP MATERIALIZED VIEW IF EXISTS daily_inventory_summary;

CREATE MATERIALIZED VIEW daily_inventory_summary
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 day', inventory_timestamp) AS day,
    product_id,
    warehouse_id,
    AVG(stock_quantity) AS avg_stock,
    MIN(stock_quantity) AS min_stock,
    MAX(stock_quantity) AS max_stock
FROM inventory_snapshots
GROUP BY day, product_id, warehouse_id
WITH NO DATA;

CALL refresh_continuous_aggregate(
    'daily_inventory_summary',
    NULL,
    NULL
);
