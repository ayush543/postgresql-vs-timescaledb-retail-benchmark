CREATE TABLE suppliers (
    supplier_id INT PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    region TEXT NOT NULL,
    lead_time_days INT NOT NULL
);

CREATE TABLE product_supplier (
    product_id INT NOT NULL,
    supplier_id INT NOT NULL,
    PRIMARY KEY (product_id, supplier_id)
);

CREATE TABLE reorder_rules (
    product_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    reorder_threshold INT NOT NULL,
    target_stock_level INT NOT NULL,
    PRIMARY KEY (product_id, warehouse_id)
);

CREATE TABLE inventory_snapshots (
    snapshot_id BIGSERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    stock_quantity INT NOT NULL,
    reorder_threshold INT NOT NULL,
    inventory_timestamp TIMESTAMP NOT NULL,
    supplier_id INT NOT NULL
);
