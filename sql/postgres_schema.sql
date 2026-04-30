DROP TABLE IF EXISTS inventory_snapshots;
DROP TABLE IF EXISTS reorder_rules;
DROP TABLE IF EXISTS product_supplier;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS order_products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS aisles;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department TEXT
);

CREATE TABLE aisles (
    aisle_id INT PRIMARY KEY,
    aisle TEXT
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name TEXT,
    aisle_id INT,
    department_id INT
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    eval_set TEXT,
    order_number INT,
    order_dow INT,
    order_hour_of_day INT,
    days_since_prior_order NUMERIC
);

CREATE TABLE order_products (
    order_id INT,
    product_id INT,
    add_to_cart_order INT,
    reordered INT
);

CREATE TABLE suppliers (
    supplier_id INT PRIMARY KEY,
    supplier_name TEXT,
    region TEXT,
    lead_time_days INT
);

CREATE TABLE product_supplier (
    product_id INT,
    supplier_id INT,
    PRIMARY KEY (product_id, supplier_id)
);

CREATE TABLE reorder_rules (
    product_id INT,
    warehouse_id INT,
    reorder_threshold INT,
    target_stock_level INT,
    PRIMARY KEY (product_id, warehouse_id)
);

CREATE TABLE inventory_snapshots (
    snapshot_id BIGSERIAL PRIMARY KEY,
    product_id INT,
    warehouse_id INT,
    stock_quantity INT,
    reorder_threshold INT,
    inventory_timestamp TIMESTAMP,
    supplier_id INT
);
