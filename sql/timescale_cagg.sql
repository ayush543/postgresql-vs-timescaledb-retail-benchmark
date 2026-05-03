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

DROP MATERIALIZED VIEW IF EXISTS daily_warehouse_inventory_summary;

CREATE MATERIALIZED VIEW daily_warehouse_inventory_summary
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', inventory_timestamp) AS day,
    warehouse_id,
    SUM(stock_quantity) AS total_stock,
    AVG(stock_quantity) AS avg_stock,
    COUNT(*) FILTER (WHERE stock_quantity < reorder_threshold) AS low_stock_events,
    COUNT(*) FILTER (WHERE stock_quantity = 0) AS stockout_events
FROM inventory_snapshots
GROUP BY day, warehouse_id
WITH NO DATA;

CALL refresh_continuous_aggregate(
    'daily_warehouse_inventory_summary',
    NULL,
    NULL
);
