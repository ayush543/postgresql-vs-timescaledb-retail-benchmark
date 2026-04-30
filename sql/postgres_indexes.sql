CREATE INDEX idx_order_products_product_id
ON order_products(product_id);

CREATE INDEX idx_order_products_order_id
ON order_products(order_id);

CREATE INDEX idx_orders_order_dow_hour
ON orders(order_dow, order_hour_of_day);

CREATE INDEX idx_orders_user_id
ON orders(user_id);

CREATE INDEX idx_inventory_product_time
ON inventory_snapshots(product_id, inventory_timestamp);

CREATE INDEX idx_inventory_warehouse_time
ON inventory_snapshots(warehouse_id, inventory_timestamp);

CREATE INDEX idx_inventory_supplier_id
ON inventory_snapshots(supplier_id);

CREATE INDEX idx_inventory_stock_quantity
ON inventory_snapshots(stock_quantity);
