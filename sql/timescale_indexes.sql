CREATE INDEX IF NOT EXISTS idx_ts_inventory_product_time
ON inventory_snapshots(product_id, inventory_timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_ts_inventory_warehouse_time
ON inventory_snapshots(warehouse_id, inventory_timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_ts_inventory_supplier_time
ON inventory_snapshots(supplier_id, inventory_timestamp DESC);
