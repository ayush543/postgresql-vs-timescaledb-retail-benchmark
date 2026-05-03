ALTER TABLE inventory_snapshots ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS warehouse_policy ON inventory_snapshots;

CREATE POLICY warehouse_policy
ON inventory_snapshots
FOR SELECT
TO app_user
USING (warehouse_id = 1);
