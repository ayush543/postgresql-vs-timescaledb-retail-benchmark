-- Create roles
CREATE ROLE read_only;
CREATE ROLE app_user LOGIN PASSWORD 'app_password';
CREATE ROLE etl LOGIN PASSWORD 'etl_password';
CREATE ROLE admin_user LOGIN PASSWORD 'admin_password';

-- Database access
GRANT CONNECT ON DATABASE retail_benchmark TO app_user;
GRANT CONNECT ON DATABASE retail_benchmark TO etl;
GRANT CONNECT ON DATABASE retail_benchmark TO admin_user;

-- Schema access
GRANT USAGE ON SCHEMA public TO app_user;
GRANT USAGE ON SCHEMA public TO etl;
GRANT USAGE ON SCHEMA public TO admin_user;

-- Read-only role
GRANT SELECT ON products, inventory_snapshots, suppliers TO read_only;

-- App user permissions
GRANT SELECT ON products, inventory_snapshots, suppliers TO app_user;

-- ETL permissions
GRANT SELECT, INSERT, UPDATE ON inventory_snapshots TO etl;
GRANT SELECT, INSERT, UPDATE ON suppliers TO etl;
GRANT SELECT, INSERT, UPDATE ON product_supplier TO etl;
GRANT SELECT, INSERT, UPDATE ON reorder_rules TO etl;

-- Admin permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin_user;
