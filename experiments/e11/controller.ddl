-- namespace_list maintains a list of tracked dqlite namespaces for the
-- controller.
CREATE TABLE namespace_list (
    namespace TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE life (
    id INT PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT INTO life VALUES
(0, 'alive'),
(1, 'dying'),
(2, 'dead');

CREATE TABLE lease_type (
    id INT PRIMARY KEY,
    type TEXT
);

CREATE UNIQUE INDEX idx_lease_type_type
ON lease_type (type);

INSERT INTO lease_type VALUES
(0, 'singular-controller'),    -- The controller running singular controller/model workers.
(1, 'application-leadership'), -- The unit that holds leadership for an application.
(2, 'backup-creation');        -- The lease serialising backup archive creation.

CREATE TABLE lease (
    uuid TEXT NOT NULL PRIMARY KEY,
    lease_type_id INT NOT NULL,
    model_uuid TEXT,
    name TEXT,
    holder TEXT,
    start TIMESTAMP,
    expiry TIMESTAMP,
    CONSTRAINT fk_lease_lease_type
    FOREIGN KEY (lease_type_id)
    REFERENCES lease_type (id)
);

CREATE UNIQUE INDEX idx_lease_model_type_name
ON lease (model_uuid, lease_type_id, name);

CREATE INDEX idx_lease_expiry
ON lease (expiry);

CREATE TABLE lease_pin (
    -- The presence of entries in this table for a particular lease_uuid
    -- implies that the lease in question is pinned and cannot expire.
    uuid TEXT NOT NULL PRIMARY KEY,
    lease_uuid TEXT,
    entity_id TEXT,
    CONSTRAINT fk_lease_pin_lease
    FOREIGN KEY (lease_uuid)
    REFERENCES lease (uuid)
);

CREATE UNIQUE INDEX idx_lease_pin_lease_entity
ON lease_pin (lease_uuid, entity_id);

CREATE INDEX idx_lease_pin_lease
ON lease_pin (lease_uuid);

CREATE TABLE change_log_edit_type (
    id INT PRIMARY KEY,
    edit_type TEXT
);

CREATE UNIQUE INDEX idx_change_log_edit_type_edit_type
ON change_log_edit_type (edit_type);

-- The change log type values are bitmasks, so that multiple types can be
-- expressed when looking for changes.
INSERT INTO change_log_edit_type VALUES
(1, 'create'),
(2, 'update'),
(4, 'delete');

CREATE TABLE change_log_namespace (
    id INT PRIMARY KEY,
    namespace TEXT,
    description TEXT
);

CREATE UNIQUE INDEX idx_change_log_namespace_namespace
ON change_log_namespace (namespace);

CREATE TABLE change_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    edit_type_id INT NOT NULL,
    namespace_id INT NOT NULL,
    changed TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW', 'utc')),
    CONSTRAINT fk_change_log_edit_type
    FOREIGN KEY (edit_type_id)
    REFERENCES change_log_edit_type (id),
    CONSTRAINT fk_change_log_namespace
    FOREIGN KEY (namespace_id)
    REFERENCES change_log_namespace (id)
);

-- The change log witness table is used to track which nodes have seen
-- which change log entries. This is used to determine when a change log entry
-- can be deleted.
-- We'll delete all change log entries that are older than the lower_bound
-- change log entry that has been seen by all controllers.
CREATE TABLE change_log_witness (
    controller_id TEXT NOT NULL PRIMARY KEY,
    lower_bound INT NOT NULL DEFAULT (-1),
    upper_bound INT NOT NULL DEFAULT (-1),
    updated_at DATETIME NOT NULL DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW', 'utc'))
);

CREATE INDEX idx_change_log_witness_watermark
ON change_log_witness (lower_bound, updated_at);

CREATE TABLE controller (
    uuid TEXT NOT NULL PRIMARY KEY,
    model_uuid TEXT NOT NULL,
    target_version TEXT NOT NULL,
    api_port TEXT,
    cert TEXT,
    ca_cert TEXT,
    private_key TEXT,
    ca_private_key TEXT,
    system_identity TEXT
);

-- A unique constraint over a constant index ensures only 1 entry matching the
-- condition can exist.
CREATE UNIQUE INDEX idx_singleton_controller ON controller ((1));

-- The cloud and accompanying tables drive the provider tracker. It is not safe
-- to modify the cloud or other tables in a patch/build release. Only make 
-- changes to this table during a major/minor release. Changes to the cloud
-- table will cause undefined behaviour in the provider tracker.
CREATE TABLE cloud_type (
    id INT PRIMARY KEY,
    type TEXT NOT NULL
);

CREATE UNIQUE INDEX idx_cloud_type_type
ON cloud_type (type);

-- The list of all the cloud types that are supported for this release. This
-- doesn't indicate whether the cloud type is supported for the current
-- controller, but rather the cloud type is supported in general.
INSERT INTO cloud_type VALUES
(0, 'kubernetes'),
(1, 'lxd'),
(2, 'maas'),
(3, 'unmanaged'),
(4, 'azure'),
(5, 'ec2'),
(6, 'gce'),
(7, 'oci'),
(8, 'openstack'),
(9, 'vsphere');

CREATE TABLE auth_type (
    id INT PRIMARY KEY,
    type TEXT
);

CREATE UNIQUE INDEX idx_auth_type_type
ON auth_type (type);

INSERT INTO auth_type VALUES
(0, 'access-key'),
(1, 'instance-role'),
(2, 'userpass'),
(3, 'oauth1'),
(4, 'oauth2'),
(5, 'jsonfile'),
(6, 'clientcertificate'),
(7, 'httpsig'),
(8, 'interactive'),
(9, 'empty'),
(10, 'certificate'),
(11, 'oauth2withcert'),
(12, 'service-principal-secret'),
(13, 'managed-identity'),
(14, 'service-account');

CREATE TABLE cloud (
    uuid TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    cloud_type_id INT NOT NULL,
    endpoint TEXT NOT NULL,
    identity_endpoint TEXT,
    storage_endpoint TEXT,
    skip_tls_verify BOOLEAN NOT NULL,
    CONSTRAINT chk_name_empty CHECK (name != ''),
    CONSTRAINT fk_cloud_type
    FOREIGN KEY (cloud_type_id)
    REFERENCES cloud_type (id)
);

CREATE TABLE cloud_defaults (
    cloud_uuid TEXT NOT NULL,
    "key" TEXT NOT NULL,
    value TEXT,
    PRIMARY KEY (cloud_uuid, "key"),
    CONSTRAINT chk_key_empty CHECK ("key" != ''),
    CONSTRAINT fk_cloud_uuid
    FOREIGN KEY (cloud_uuid)
    REFERENCES cloud (uuid)
);

CREATE TABLE cloud_auth_type (
    cloud_uuid TEXT NOT NULL,
    auth_type_id INT NOT NULL,
    CONSTRAINT fk_cloud_auth_type_cloud
    FOREIGN KEY (cloud_uuid)
    REFERENCES cloud (uuid),
    CONSTRAINT fk_cloud_auth_type_auth_type
    FOREIGN KEY (auth_type_id)
    REFERENCES auth_type (id),
    PRIMARY KEY (cloud_uuid, auth_type_id)
);

CREATE UNIQUE INDEX idx_cloud_auth_type_cloud_uuid_auth_type_id
ON cloud_auth_type (cloud_uuid, auth_type_id);

CREATE TABLE cloud_region (
    uuid TEXT NOT NULL PRIMARY KEY,
    cloud_uuid TEXT NOT NULL,
    name TEXT NOT NULL,
    endpoint TEXT,
    identity_endpoint TEXT,
    storage_endpoint TEXT,
    CONSTRAINT fk_cloud_region_cloud
    FOREIGN KEY (cloud_uuid)
    REFERENCES cloud (uuid)
);

CREATE UNIQUE INDEX idx_cloud_region_cloud_uuid_name
ON cloud_region (cloud_uuid, name);

CREATE INDEX idx_cloud_region_cloud_uuid
ON cloud_region (cloud_uuid);

CREATE TABLE cloud_region_defaults (
    region_uuid TEXT NOT NULL,
    "key" TEXT NOT NULL,
    value TEXT,
    PRIMARY KEY (region_uuid, "key"),
    CONSTRAINT chk_key_empty CHECK ("key" != ''),
    CONSTRAINT fk_region_uuid
    FOREIGN KEY (region_uuid)
    REFERENCES cloud_region (uuid)
);

CREATE TABLE cloud_ca_cert (
    cloud_uuid TEXT NOT NULL,
    ca_cert TEXT NOT NULL,
    CONSTRAINT fk_cloud_ca_cert_cloud
    FOREIGN KEY (cloud_uuid)
    REFERENCES cloud (uuid),
    PRIMARY KEY (cloud_uuid, ca_cert)
);

CREATE UNIQUE INDEX idx_cloud_ca_cert_cloud_uuid_ca_cert
ON cloud_ca_cert (cloud_uuid, ca_cert);

CREATE TABLE cloud_credential (
    uuid TEXT NOT NULL PRIMARY KEY,
    cloud_uuid TEXT NOT NULL,
    auth_type_id TEXT NOT NULL,
    owner_uuid TEXT NOT NULL,
    name TEXT NOT NULL,
    revoked BOOLEAN,
    invalid BOOLEAN,
    invalid_reason TEXT,
    CONSTRAINT chk_name_empty CHECK (name != ''),
    CONSTRAINT fk_cloud_credential_cloud
    FOREIGN KEY (cloud_uuid)
    REFERENCES cloud (uuid),
    CONSTRAINT fk_cloud_credential_auth_type
    FOREIGN KEY (auth_type_id)
    REFERENCES auth_type (id),
    CONSTRAINT fk_cloud_credential_user
    FOREIGN KEY (owner_uuid)
    REFERENCES user (uuid)
);

CREATE UNIQUE INDEX idx_cloud_credential_cloud_uuid_owner_uuid
ON cloud_credential (cloud_uuid, owner_uuid, name);

CREATE INDEX idx_cloud_credential_owner_uuid
ON cloud_credential (owner_uuid);

-- view_cloud_credential is a convenience view for accessing a
-- credential UUID based on the natural key used to display the
-- credential to users.
CREATE VIEW v_cloud_credential
AS
SELECT
    cc.uuid,
    cc.cloud_uuid,
    c.name AS cloud_name,
    cc.auth_type_id,
    at.type AS auth_type,
    cc.owner_uuid,
    cc.name,
    cc.revoked,
    cc.invalid,
    cc.invalid_reason,
    u.name AS owner_name
FROM cloud_credential AS cc
JOIN cloud AS c ON cc.cloud_uuid = c.uuid
JOIN user AS u ON cc.owner_uuid = u.uuid
JOIN auth_type AS at ON cc.auth_type_id = at.id;

CREATE TABLE cloud_credential_attribute (
    cloud_credential_uuid TEXT NOT NULL,
    "key" TEXT NOT NULL,
    value TEXT,
    PRIMARY KEY (cloud_credential_uuid, "key"),
    CONSTRAINT chk_key_empty CHECK ("key" != ''),
    CONSTRAINT fk_cloud_credential_uuid
    FOREIGN KEY (cloud_credential_uuid)
    REFERENCES cloud_credential (uuid)
);

-- v_cloud_credential_attribute returns a view of all cloud credentials
-- and their attributes repeated for every attribute.
CREATE VIEW v_cloud_credential_attribute
AS
SELECT
    cc.uuid,
    cc.cloud_uuid,
    cc.auth_type_id,
    cc.auth_type,
    cc.owner_uuid,
    cc.name,
    cc.revoked,
    cc.invalid,
    cc.invalid_reason,
    cc.cloud_name,
    cc.owner_name,
    cca."key" AS attribute_key,
    cca.value AS attribute_value
FROM v_cloud_credential AS cc
JOIN cloud_credential_attribute AS cca ON cc.uuid = cca.cloud_credential_uuid;

CREATE TABLE external_controller (
    uuid TEXT NOT NULL PRIMARY KEY,
    alias TEXT,
    ca_cert TEXT NOT NULL
);

CREATE TABLE external_controller_address (
    uuid TEXT NOT NULL PRIMARY KEY,
    controller_uuid TEXT NOT NULL,
    address TEXT NOT NULL,
    CONSTRAINT fk_external_controller_address_external_controller_uuid
    FOREIGN KEY (controller_uuid)
    REFERENCES external_controller (uuid)
);

CREATE UNIQUE INDEX idx_external_controller_address
ON external_controller_address (controller_uuid, address);

CREATE TABLE external_model (
    uuid TEXT NOT NULL PRIMARY KEY,
    controller_uuid TEXT NOT NULL,
    CONSTRAINT fk_external_model_external_controller_uuid
    FOREIGN KEY (controller_uuid)
    REFERENCES external_controller (uuid)
);

CREATE INDEX idx_external_model_controller_uuid
ON external_model (controller_uuid);

-- model_namespace is a mapping table from models to the corresponding dqlite
-- namespace database.
CREATE TABLE model_namespace (
    namespace TEXT NOT NULL,
    model_uuid TEXT UNIQUE NOT NULL,
    CONSTRAINT fk_model_uuid
    FOREIGN KEY (model_uuid)
    REFERENCES model (uuid)
);

CREATE UNIQUE INDEX idx_namespace_model_uuid ON model_namespace (namespace, model_uuid);

CREATE TABLE model_type (
    id INT PRIMARY KEY,
    type TEXT NOT NULL
);

CREATE UNIQUE INDEX idx_model_type_type
ON model_type (type);

INSERT INTO model_type VALUES
(0, 'iaas'),
(1, 'caas');

CREATE TABLE model (
    uuid TEXT NOT NULL PRIMARY KEY,
    -- activated tells us if the model creation process has been completed and
    -- we can use this model. The reason for this is model creation still happens
    -- over several transactions with any one of them possibly failing. We write true
    -- to this field when we are happy that the model can safely be used after all
    -- operations have been completed.
    activated BOOLEAN DEFAULT FALSE NOT NULL,
    cloud_uuid TEXT NOT NULL,
    cloud_region_uuid TEXT,
    cloud_credential_uuid TEXT,
    model_type_id INT NOT NULL,
    life_id INT NOT NULL,
    name TEXT NOT NULL,
    qualifier TEXT NOT NULL,
    CONSTRAINT fk_model_cloud
    FOREIGN KEY (cloud_uuid)
    REFERENCES cloud (uuid),
    CONSTRAINT fk_model_cloud_region
    FOREIGN KEY (cloud_region_uuid)
    REFERENCES cloud_region (uuid),
    CONSTRAINT fk_model_cloud_credential
    FOREIGN KEY (cloud_credential_uuid)
    REFERENCES cloud_credential (uuid),
    CONSTRAINT fk_model_model_type_id
    FOREIGN KEY (model_type_id)
    REFERENCES model_type (id),
    CONSTRAINT fk_model_life_id
    FOREIGN KEY (life_id)
    REFERENCES life (id)
);

-- idx_model_qualified_name established an index that stops models being created
-- with the same qualified name.
CREATE UNIQUE INDEX idx_model_qualified_name ON model (name, qualifier);
CREATE INDEX idx_model_activated ON model (activated);
CREATE INDEX idx_model_life ON model (life_id);

-- v_model_all is a view that provides a simple way to access models
-- that have not been activated. This is useful for the model creation process
-- where we need to access the model to update it but we do not want to show it
-- to the user until it is ready.
CREATE VIEW v_model_all AS
SELECT
    m.uuid,
    m.life_id,
    m.cloud_uuid,
    c.name AS cloud_name,
    ct.type AS cloud_type,
    c.endpoint AS cloud_endpoint,
    c.skip_tls_verify AS cloud_skip_tls_verify,
    cr.uuid AS cloud_region_uuid,
    cr.name AS cloud_region_name,
    cc.uuid AS cloud_credential_uuid,
    cc.name AS cloud_credential_name,
    cc.invalid AS cloud_credential_invalid,
    ccc.name AS cloud_credential_cloud_name,
    cco.uuid AS cloud_credential_owner_uuid,
    cco.name AS cloud_credential_owner_name,
    m.model_type_id,
    mt.type AS model_type,
    m.qualifier,
    m.name,
    l.value AS life,
    m.activated,
    -- Don't rely on controller_uuid always being set to a value.
    ctrli.uuid AS controller_uuid,
    IIF(ctrlm.model_uuid IS NOT NULL, TRUE, FALSE) AS is_controller_model
FROM model AS m
JOIN cloud AS c ON m.cloud_uuid = c.uuid
JOIN cloud_type AS ct ON c.cloud_type_id = ct.id
JOIN model_type AS mt ON m.model_type_id = mt.id
JOIN life AS l ON m.life_id = l.id
LEFT JOIN controller AS ctrli
LEFT JOIN controller AS ctrlm ON m.uuid = ctrlm.model_uuid
LEFT JOIN cloud_region AS cr ON m.cloud_region_uuid = cr.uuid
LEFT JOIN cloud_credential AS cc ON m.cloud_credential_uuid = cc.uuid
LEFT JOIN cloud AS ccc ON cc.cloud_uuid = ccc.uuid
LEFT JOIN user AS cco ON cc.owner_uuid = cco.uuid;

--- v_model purpose is to provide an easy access mechanism for models in the
--- system. It will only show models that have been activated so the caller does
--- not have to worry about retrieving half complete models.
CREATE VIEW v_model AS
SELECT
    uuid,
    cloud_uuid,
    cloud_name,
    cloud_type,
    cloud_endpoint,
    cloud_skip_tls_verify,
    cloud_region_uuid,
    cloud_region_name,
    cloud_credential_uuid,
    cloud_credential_name,
    cloud_credential_invalid,
    cloud_credential_cloud_name,
    cloud_credential_owner_uuid,
    cloud_credential_owner_name,
    model_type_id,
    model_type,
    name,
    qualifier,
    life_id,
    life,
    activated,
    controller_uuid,
    is_controller_model
FROM v_model_all
WHERE activated = TRUE;

-- v_model_state exists to provide a simple view over the states that are
-- needed to calculate a model's status.
CREATE VIEW v_model_state AS
SELECT
    m.uuid,
    l.value AS life,
    cc.invalid AS cloud_credential_invalid,
    cc.invalid_reason AS cloud_credential_invalid_reason,
    IIF(mmi.model_uuid IS NOT NULL, TRUE, FALSE) AS migrating
FROM model AS m
JOIN life AS l ON m.life_id = l.id
LEFT JOIN cloud_credential AS cc ON m.cloud_credential_uuid = cc.uuid
LEFT JOIN model_migration_import AS mmi ON m.uuid = mmi.model_uuid
WHERE m.activated = TRUE;

-- v_cloud is used to fetch well-constructed information about a cloud.
-- This view also includes information on whether the cloud is the
-- controller model's cloud.
CREATE VIEW v_cloud
AS
-- This selects the controller model's cloud uuid. We use this when loading
-- clouds to know if the cloud is the controller's cloud.
WITH controllers AS (
    SELECT m.cloud_uuid
    FROM model AS m
    WHERE
        m.name = 'controller'
        AND m.qualifier = 'admin'
        AND m.activated = TRUE
)

SELECT
    c.uuid,
    c.name,
    c.cloud_type_id,
    ct.type AS cloud_type,
    c.endpoint,
    c.identity_endpoint,
    c.storage_endpoint,
    c.skip_tls_verify,
    IIF(controllers.cloud_uuid IS NULL, FALSE, TRUE) AS is_controller_cloud
FROM cloud AS c
JOIN cloud_type AS ct ON c.cloud_type_id = ct.id
LEFT JOIN controllers ON c.uuid = controllers.cloud_uuid;

-- v_cloud_auth is a view similar to v_cloud but includes a row for
-- each cloud and auth type pair.
CREATE VIEW v_cloud_auth
AS
SELECT
    c.uuid,
    c.name,
    c.cloud_type_id,
    c.cloud_type,
    c.endpoint,
    c.identity_endpoint,
    c.storage_endpoint,
    c.skip_tls_verify,
    c.is_controller_cloud,
    at.id AS auth_type_id,
    at.type AS auth_type
FROM v_cloud AS c
LEFT JOIN cloud_auth_type AS cat ON c.uuid = cat.cloud_uuid
JOIN auth_type AS at ON cat.auth_type_id = at.id;

CREATE TABLE controller_config (
    "key" TEXT NOT NULL PRIMARY KEY,
    value TEXT
);

CREATE VIEW v_controller_config AS
SELECT
    "key",
    value
FROM controller_config
UNION ALL
SELECT
    'controller-uuid' AS "key",
    controller.uuid AS value
FROM controller
UNION ALL
SELECT
    'ca-cert' AS "key",
    controller.ca_cert AS value
FROM controller
UNION ALL
SELECT
    'api-port' AS "key",
    controller.api_port AS value
FROM controller
WHERE controller.api_port IS NOT NULL AND controller.api_port != '';

CREATE TABLE password_hash_algorithm (
    id INT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE UNIQUE INDEX idx_password_hash_algorithm
ON password_hash_algorithm (name);

INSERT INTO password_hash_algorithm VALUES
(0, 'sha512');

CREATE TABLE controller_node (
    controller_id TEXT NOT NULL PRIMARY KEY,
    life_id INT NOT NULL DEFAULT 0,
    dqlite_node_id TEXT,              -- This is the uint64 from Dqlite NodeInfo, stored as text.
    dqlite_bind_address TEXT,         -- Hostname or IP address (no port) that Dqlite is bound to.
    CONSTRAINT fk_controller_node_life
    FOREIGN KEY (life_id)
    REFERENCES life (id)
);

CREATE UNIQUE INDEX idx_controller_node_dqlite_node
ON controller_node (dqlite_node_id);

CREATE UNIQUE INDEX idx_controller_node_dqlite_bind_address
ON controller_node (dqlite_bind_address);

-- controller_node_agent_version tracks the reported agent version running for
-- each controller in the cluster.
CREATE TABLE controller_node_agent_version (
    controller_id TEXT NOT NULL PRIMARY KEY,
    version TEXT NOT NULL,
    architecture_id INT NOT NULL,
    CONSTRAINT fk_controller_node_agent_version_controller
    FOREIGN KEY (controller_id)
    REFERENCES controller_node (controller_id),
    CONSTRAINT fk_controller_node_agent_version_architecture
    FOREIGN KEY (architecture_id)
    REFERENCES architecture (id)
);

CREATE INDEX idx_controller_node_agent_version_architecture
ON controller_node_agent_version (architecture_id);

CREATE TABLE controller_api_address (
    controller_id TEXT NOT NULL,
    -- The value of the configured IP address with the port appended.
    -- e.g. 192.168.1.2:17070 or [2001:db8:0000:0000:0000:0000:0000:00001]:17070.
    address TEXT NOT NULL,
    -- Represents whether the API address is available for agents usage.
    is_agent BOOLEAN DEFAULT FALSE,
    -- Represents the context an address may apply to. E.g. public, private.
    scope TEXT NOT NULL,
    CONSTRAINT fk_controller_api_address_controller
    FOREIGN KEY (controller_id)
    REFERENCES controller_node (controller_id),
    PRIMARY KEY (controller_id, address)
);

-- Published API endpoints for agents. A NULL controller_id represents a shared
-- endpoint, such as a Kubernetes Service, rather than a specific controller.
CREATE TABLE controller_agent_address (
    uuid TEXT NOT NULL PRIMARY KEY,
    controller_id TEXT,
    -- IP address or hostname with the API port appended.
    address TEXT NOT NULL,
    scope TEXT NOT NULL,
    -- Lower values are preferred within the controller or shared endpoint group.
    priority INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_controller_agent_address_controller
    FOREIGN KEY (controller_id)
    REFERENCES controller_node (controller_id)
);

CREATE UNIQUE INDEX idx_controller_agent_address
ON controller_agent_address (controller_id, address);

-- NULL controller IDs do not compare equal in the index above.
CREATE UNIQUE INDEX idx_controller_agent_address_shared
ON controller_agent_address (address) WHERE controller_id IS NULL;

-- Published API endpoints for clients. Controller identity is retained only
-- when the endpoint reaches a specific controller; shared endpoints use NULL.
CREATE TABLE controller_client_address (
    uuid TEXT NOT NULL PRIMARY KEY,
    controller_id TEXT,
    -- IP address or hostname with the API port appended.
    address TEXT NOT NULL,
    scope TEXT NOT NULL,
    -- Lower values are preferred within the controller or shared endpoint group.
    priority INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_controller_client_address_controller
    FOREIGN KEY (controller_id)
    REFERENCES controller_node (controller_id)
);

CREATE UNIQUE INDEX idx_controller_client_address
ON controller_client_address (controller_id, address);

CREATE UNIQUE INDEX idx_controller_client_address_shared
ON controller_client_address (address) WHERE controller_id IS NULL;

-- Published API endpoints for communication between controllers. Each endpoint
-- must reach the identified controller, so shared Service endpoints do not apply.
CREATE TABLE controller_peer_address (
    uuid TEXT NOT NULL PRIMARY KEY,
    controller_id TEXT NOT NULL,
    -- IP address or hostname with the API port appended.
    address TEXT NOT NULL,
    scope TEXT NOT NULL,
    -- Lower values are preferred for this controller.
    priority INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_controller_peer_address_controller
    FOREIGN KEY (controller_id)
    REFERENCES controller_node (controller_id)
);

CREATE UNIQUE INDEX idx_controller_peer_address
ON controller_peer_address (controller_id, address);

CREATE TABLE controller_node_password (
    controller_id TEXT NOT NULL PRIMARY KEY,
    password_hash_algorithm_id TEXT,
    password_hash TEXT,
    CONSTRAINT fk_controller_node_password_controller
    FOREIGN KEY (controller_id)
    REFERENCES controller_node (controller_id),
    CONSTRAINT fk_controller_node_password_hash_algorithm
    FOREIGN KEY (password_hash_algorithm_id)
    REFERENCES password_hash_algorithm (id)
);

-- controller_node_nonce stores a per-ordinal nonce used to authenticate a
-- controller pod during UnitIntroduction. Nonces are generated before the
-- StatefulSet is created and bound to a specific ordinal in the ConfigMap.
-- The correct nonce must be presented by the pod's init container to prove
-- it is the legitimate pod for that ordinal. The row is verified (not
-- consumed) on each introduction attempt. Idempotency is provided by the
-- password insert-if-absent guard, not by nonce consumption.
--
-- There is deliberately no foreign key to controller_node: this nonce must
-- exist before the controller pod can introduce itself and create that row.
CREATE TABLE controller_node_nonce (
    controller_id TEXT NOT NULL PRIMARY KEY,
    nonce TEXT NOT NULL
);

-- Lookup of export-side migration phases. Mirrors core/migration/phase.go,
-- minus UNKNOWN/NONE (code-only sentinels never written to the DB) and
-- PROCESSRELATIONS (vestigial phase with no actions attached).
CREATE TABLE model_migration_phase (
    id INT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE UNIQUE INDEX idx_model_migration_phase_name
ON model_migration_phase (name);

INSERT INTO model_migration_phase VALUES
(1, 'quiesce'),
(2, 'import'),
(3, 'validation'),
(4, 'success'),
(5, 'log-transfer'),
(6, 'reap'),
(7, 'reap-failed'),
(8, 'done'),
(9, 'abort'),
(10, 'abort-done');


-- Lookup of import-claim phases. A FK to this table replaces an inline CHECK
-- so that adding a future phase is a single INSERT rather than a SQLite
-- table rebuild.
CREATE TABLE model_migration_import_phase_type (
    id INT NOT NULL PRIMARY KEY,
    type TEXT NOT NULL
);

CREATE UNIQUE INDEX idx_model_migration_import_phase_type
ON model_migration_import_phase_type (type);

INSERT INTO model_migration_import_phase_type VALUES
(0, 'importing'),
(1, 'activating'),
(2, 'aborting');

CREATE TABLE model_migration_import (
    uuid TEXT NOT NULL PRIMARY KEY,
    model_uuid TEXT NOT NULL,
    source_migration_uuid TEXT NOT NULL,
    phase_type_id INT NOT NULL DEFAULT 0,
    updated_at DATETIME NOT NULL,
    CONSTRAINT fk_model_migration_import_phase_type
    FOREIGN KEY (phase_type_id)
    REFERENCES model_migration_import_phase_type (id)
);

CREATE UNIQUE INDEX idx_model_migration_import ON model_migration_import (model_uuid);

CREATE INDEX idx_model_migration_import_phase_updated
ON model_migration_import (phase_type_id, updated_at);

-- Durable handoff from Import to Activate for cross-model relation offers.
CREATE TABLE model_migration_import_offer (
    migration_uuid TEXT NOT NULL,
    offer_uuid TEXT NOT NULL,
    PRIMARY KEY (migration_uuid, offer_uuid),
    CONSTRAINT fk_model_migration_import_offer_migration
    FOREIGN KEY (migration_uuid)
    REFERENCES model_migration_import (uuid)
);

-- Durable handoff from Import to Activate for third-party external controller
-- model mappings. Activate reads these rows to set the offerer controller
-- for each offerer model without depending on the original import envelope
-- still being in memory after a controller restart.
CREATE TABLE model_migration_import_external_controller_model (
    migration_uuid TEXT NOT NULL,
    offerer_model_uuid TEXT NOT NULL,
    controller_uuid TEXT NOT NULL,
    PRIMARY KEY (migration_uuid, offerer_model_uuid),
    CONSTRAINT fk_model_migration_import_ecm_migration
    FOREIGN KEY (migration_uuid)
    REFERENCES model_migration_import (uuid),
    CONSTRAINT fk_model_migration_import_ecm_external_controller
    FOREIGN KEY (controller_uuid)
    REFERENCES external_controller (uuid)
);

CREATE INDEX idx_model_migration_import_ecm_controller
ON model_migration_import_external_controller_model (controller_uuid);

-- One row per export migration attempt for a model. There is no attempt
-- counter: a retry is just a new migration with a new uuid.
-- model_uuid deliberately has no FK to model because source REAP deletes
-- the model row while export history remains available for diagnostics.
--
-- current_phase_id and updated_at are denormalised from
-- model_migration_export_phase so that watchers and "is this migration
-- active?" queries do not have to aggregate the history table on every read.
-- The history table remains the source of truth.
CREATE TABLE model_migration_export (
    uuid TEXT NOT NULL PRIMARY KEY,
    model_uuid TEXT NOT NULL,
    target_controller_uuid TEXT NOT NULL,
    current_phase_id INT NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    start_time TIMESTAMP NOT NULL,
    CONSTRAINT fk_model_migration_export_target_controller
    FOREIGN KEY (target_controller_uuid)
    REFERENCES external_controller (uuid),
    CONSTRAINT fk_model_migration_export_current_phase
    FOREIGN KEY (current_phase_id)
    REFERENCES model_migration_phase (id)
);

-- At most one active export migration per model. Persisted terminal phase ids
-- are reap-failed (7), done (8), and abort-done (10).
CREATE UNIQUE INDEX idx_model_migration_export_active_model
ON model_migration_export (model_uuid)
WHERE current_phase_id NOT IN (7, 8, 10);

CREATE INDEX idx_model_migration_export_model
ON model_migration_export (model_uuid);

CREATE INDEX idx_model_migration_export_target_controller
ON model_migration_export (target_controller_uuid);

-- Hosted offer UUIDs captured before the source model DB is purged. REAP uses
-- these rows to delete source-controller offer permissions after the source
-- model row and model DB namespace have gone.
CREATE TABLE model_migration_export_offer (
    migration_uuid TEXT NOT NULL,
    offer_uuid TEXT NOT NULL,
    PRIMARY KEY (migration_uuid, offer_uuid),
    CONSTRAINT fk_model_migration_export_offer_migration
    FOREIGN KEY (migration_uuid)
    REFERENCES model_migration_export (uuid)
);

-- Standalone redirect snapshot for a model that has completed REAP. This table
-- deliberately has no FK to model, model_migration_export, or
-- external_controller because those rows may be removed while offline agents
-- still need redirect information from this source controller.
CREATE TABLE model_migration_redirect (
    model_uuid TEXT NOT NULL PRIMARY KEY,
    source_migration_uuid TEXT NOT NULL,
    target_controller_uuid TEXT NOT NULL,
    target_controller_alias TEXT,
    target_addresses TEXT NOT NULL,
    target_ca_cert TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP
);

-- Captured model access at migration time. The snapshot is intentionally
-- independent of the live permission rows, which are removed during REAP.
CREATE TABLE model_migration_redirect_user (
    model_uuid TEXT NOT NULL,
    user_uuid TEXT NOT NULL,
    user_name TEXT NOT NULL,
    access TEXT NOT NULL,
    PRIMARY KEY (model_uuid, user_uuid),
    CONSTRAINT fk_model_migration_redirect_user_redirect
    FOREIGN KEY (model_uuid)
    REFERENCES model_migration_redirect (model_uuid)
);

-- Per-migration authentication material for connecting to the target
-- controller. Held separately from external_controller because the material
-- is per-migration (it may be rotated, scoped, or JIMM-issued) and
-- external_controller is shared with the cross-model relations domain.
--
-- The dual FK (migration + external_controller) makes the relationship
-- explicit: a row here means "auth material for this migration to connect
-- to that external controller".
CREATE TABLE model_migration_export_target_auth (
    migration_uuid TEXT NOT NULL PRIMARY KEY,
    external_controller_uuid TEXT NOT NULL,
    target_user TEXT NOT NULL,
    target_macaroons TEXT,
    target_token TEXT,
    target_skip_user_checks BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_model_migration_export_target_auth_migration
    FOREIGN KEY (migration_uuid)
    REFERENCES model_migration_export (uuid),
    CONSTRAINT fk_model_migration_export_target_auth_external_controller
    FOREIGN KEY (external_controller_uuid)
    REFERENCES external_controller (uuid)
);

CREATE INDEX idx_model_migration_export_target_auth_external_controller
ON model_migration_export_target_auth (external_controller_uuid);

-- Time-ordered record of which phases an export migration has entered.
-- Each phase is entered at most once per migration, so (migration_uuid,
-- phase_id) is the natural key.
--
-- model_uuid is denormalised from the parent model_migration_export row so the
-- changestream trigger can emit the model-scoped key watched for phase changes.
CREATE TABLE model_migration_export_phase (
    migration_uuid TEXT NOT NULL,
    model_uuid TEXT NOT NULL,
    phase_id INT NOT NULL,
    changed_at TIMESTAMP NOT NULL,
    PRIMARY KEY (migration_uuid, phase_id),
    CONSTRAINT fk_model_migration_export_phase_migration
    FOREIGN KEY (migration_uuid)
    REFERENCES model_migration_export (uuid),
    CONSTRAINT fk_model_migration_export_phase_phase
    FOREIGN KEY (phase_id)
    REFERENCES model_migration_phase (id)
);

CREATE INDEX idx_model_migration_export_phase_changed_at
ON model_migration_export_phase (migration_uuid, changed_at);

-- Current free-form status message reported by the migration master.
CREATE TABLE model_migration_export_status (
    migration_uuid TEXT NOT NULL PRIMARY KEY,
    message TEXT NOT NULL,
    recorded_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_model_migration_export_status_migration
    FOREIGN KEY (migration_uuid)
    REFERENCES model_migration_export (uuid)
);

CREATE INDEX idx_model_migration_export_status_recorded_at
ON model_migration_export_status (migration_uuid, recorded_at);

-- Status messages are intentionally not changelogged. They can update often
-- during migration and should not amplify model migration watcher traffic.

-- Reports submitted by minion agents (machines/units) confirming or
-- failing the work for a given phase. entity_key is the agent's tag-like
-- identifier (e.g. "machine-0", "unit-foo-0").
CREATE TABLE model_migration_export_minion_sync (
    migration_uuid TEXT NOT NULL,
    phase_id INT NOT NULL,
    entity_key TEXT NOT NULL,
    success BOOLEAN NOT NULL,
    reported_at TIMESTAMP NOT NULL,
    PRIMARY KEY (migration_uuid, phase_id, entity_key),
    CONSTRAINT fk_model_migration_export_minion_sync_migration
    FOREIGN KEY (migration_uuid)
    REFERENCES model_migration_export (uuid),
    CONSTRAINT fk_model_migration_export_minion_sync_phase
    FOREIGN KEY (phase_id)
    REFERENCES model_migration_phase (id)
);

CREATE TABLE upgrade_state_type (
    id INT PRIMARY KEY,
    type TEXT
);

CREATE UNIQUE INDEX idx_upgrade_state_type_type
ON upgrade_state_type (type);

INSERT INTO upgrade_state_type VALUES
(0, 'created'),
(1, 'started'),
(2, 'db-completed'),
(3, 'steps-completed'),
(4, 'error');

CREATE TABLE upgrade_info (
    uuid TEXT NOT NULL PRIMARY KEY,
    previous_version TEXT NOT NULL,
    target_version TEXT NOT NULL,
    state_type_id INT NOT NULL,
    CONSTRAINT fk_upgrade_info_upgrade_state_type
    FOREIGN KEY (state_type_id)
    REFERENCES upgrade_state_type (id)
);

-- A unique constraint over a constant index ensures only 1 entry matching the 
-- condition can exist. This states, that multiple upgrades can exist if they're
-- not active, but only one active upgrade can exist
CREATE UNIQUE INDEX idx_singleton_active_upgrade ON upgrade_info ((1)) WHERE state_type_id < 3;

CREATE TABLE upgrade_info_controller_node (
    uuid TEXT NOT NULL PRIMARY KEY,
    controller_node_id TEXT NOT NULL,
    upgrade_info_uuid TEXT NOT NULL,
    node_upgrade_completed_at TIMESTAMP,
    CONSTRAINT fk_controller_node_id
    FOREIGN KEY (controller_node_id)
    REFERENCES controller_node (controller_id),
    CONSTRAINT fk_upgrade_info
    FOREIGN KEY (upgrade_info_uuid)
    REFERENCES upgrade_info (uuid)
);

CREATE UNIQUE INDEX idx_upgrade_info_controller_node
ON upgrade_info_controller_node (controller_node_id, upgrade_info_uuid);

CREATE INDEX idx_upgrade_info_controller_node_upgrade_completed_controller
ON upgrade_info_controller_node (upgrade_info_uuid, node_upgrade_completed_at);

CREATE TABLE autocert_cache (
    uuid TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    data TEXT NOT NULL,
    encoding TEXT NOT NULL,
    CONSTRAINT fk_autocert_cache_encoding
    FOREIGN KEY (encoding)
    REFERENCES autocert_cache_encoding (id)
);

-- NOTE(nvinuesa): This table only populated with *one* hard-coded value
-- (x509) because golang's autocert cache doesn't provide encoding in it's
-- function signatures, and in juju we are only using x509 certs. The value
-- of this table is to correctly represent the domain and already have a
-- list of possible encodings when we update our code in the future.
CREATE TABLE autocert_cache_encoding (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

INSERT INTO autocert_cache_encoding VALUES
(0, 'x509');    -- Only x509 certs encoding supported today.

CREATE TABLE object_store_metadata (
    uuid TEXT NOT NULL PRIMARY KEY,
    sha_256 TEXT NOT NULL,
    sha_384 TEXT NOT NULL,
    size INT NOT NULL
);

-- Add a unique index for each hash and a composite unique index for both hashes
-- to ensure that the same hash is not stored multiple times.
CREATE UNIQUE INDEX idx_object_store_metadata_sha_256 ON object_store_metadata (sha_256);
CREATE UNIQUE INDEX idx_object_store_metadata_sha_384 ON object_store_metadata (sha_384);

CREATE TABLE object_store_metadata_path (
    path TEXT NOT NULL PRIMARY KEY,
    metadata_uuid TEXT NOT NULL,
    CONSTRAINT fk_object_store_metadata_metadata_uuid
    FOREIGN KEY (metadata_uuid)
    REFERENCES object_store_metadata (uuid)
);

CREATE INDEX idx_object_store_metadata_path_metadata_uuid
ON object_store_metadata_path (metadata_uuid);

CREATE VIEW v_object_store_metadata AS
SELECT
    osm.uuid,
    osm.sha_256,
    osm.sha_384,
    osm.size,
    osmp.path
FROM object_store_metadata AS osm
LEFT JOIN object_store_metadata_path AS osmp
    ON osm.uuid = osmp.metadata_uuid;

CREATE TABLE object_store_placement (
    uuid TEXT NOT NULL,
    node_id TEXT NOT NULL,
    CONSTRAINT fk_object_store_placement_uuid
    FOREIGN KEY (uuid)
    REFERENCES object_store_metadata (uuid),
    PRIMARY KEY (uuid, node_id)
);

CREATE TABLE object_store_backend_type (
    id INT NOT NULL PRIMARY KEY,
    type TEXT NOT NULL UNIQUE
);

INSERT INTO object_store_backend_type (id, type) VALUES
(0, 'file'),
(1, 's3');

CREATE TABLE object_store_backend (
    uuid TEXT NOT NULL PRIMARY KEY,
    life_id INT NOT NULL,
    type_id INT NOT NULL,
    updated_at DATETIME NOT NULL,
    CONSTRAINT fk_object_store_backend_life_id
    FOREIGN KEY (life_id)
    REFERENCES life (id),
    CONSTRAINT fk_object_store_backend_type_id
    FOREIGN KEY (type_id)
    REFERENCES object_store_backend_type (id)
);

INSERT INTO object_store_backend (uuid, life_id, type_id, updated_at) VALUES
('653813f9-2896-5332-8cbe-629a337a56a3', 0, 0, current_timestamp);

-- A unique constraint over a constant index ensures only 1 entry matching the
-- condition can exist. In this case only 1 object store backend of type file
-- can exist, but multiple s3 backends can exist.
CREATE UNIQUE INDEX idx_singleton_object_store_backend_type_id ON object_store_backend ((1)) WHERE type_id = 0;

-- This unique constraint ensures only 1 object store backend can exist with a
-- life_id of 0, which is the life_id used for the file backend. This ensures
-- only 1 file backend can exist at a time.
CREATE UNIQUE INDEX idx_singleton_object_store_backend_life_id_alive ON object_store_backend ((1)) WHERE life_id = 0;
CREATE UNIQUE INDEX idx_singleton_object_store_backend_life_id_dying ON object_store_backend ((1)) WHERE life_id = 1;

CREATE TABLE object_store_backend_s3_config (
    object_store_backend_uuid TEXT NOT NULL PRIMARY KEY,
    bucket TEXT,
    region TEXT,
    endpoint TEXT NOT NULL,
    static_key TEXT NOT NULL,
    static_secret TEXT NOT NULL,
    CONSTRAINT fk_object_store_backend_uuid_s3_config_object_store_uuid
    FOREIGN KEY (object_store_backend_uuid)
    REFERENCES object_store_backend (uuid)
);

CREATE TABLE object_store_drain_phase_type (
    id INT PRIMARY KEY,
    type TEXT
);

CREATE UNIQUE INDEX idx_object_store_drain_phase_type_type
ON object_store_drain_phase_type (type);

INSERT INTO object_store_drain_phase_type VALUES
(0, 'unknown'),
(1, 'draining'),
(2, 'error'),
(3, 'completed');

CREATE TABLE object_store_drain_info (
    uuid TEXT NOT NULL PRIMARY KEY,
    phase_type_id INT NOT NULL,
    from_backend_uuid TEXT,
    to_backend_uuid TEXT NOT NULL,
    CONSTRAINT fk_object_store_drain_info_object_store_drain_phase_type
    FOREIGN KEY (phase_type_id)
    REFERENCES object_store_drain_phase_type (id),
    CONSTRAINT fk_object_store_drain_info_from_object_store_backend_uuid
    FOREIGN KEY (from_backend_uuid)
    REFERENCES object_store_backend (uuid),
    CONSTRAINT fk_object_store_drain_info_to_object_store_backend_uuid
    FOREIGN KEY (to_backend_uuid)
    REFERENCES object_store_backend (uuid)
);

-- A unique constraint over a constant index ensures only 1 entry matching the 
-- condition can exist. This states, that multiple draining can exist if they're
-- not active, but only one active drain can exist.
CREATE UNIQUE INDEX idx_singleton_active_drain ON object_store_drain_info ((1)) WHERE phase_type_id < 2;

CREATE TABLE user (
    uuid TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    display_name TEXT,
    external BOOLEAN NOT NULL,
    removed BOOLEAN NOT NULL DEFAULT FALSE,
    created_by_uuid TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_user_created_by_user
    FOREIGN KEY (created_by_uuid)
    REFERENCES user (uuid)
);

CREATE UNIQUE INDEX idx_singleton_active_user ON user (name) WHERE removed IS FALSE;

CREATE INDEX idx_user_name ON user (name);

CREATE INDEX idx_user_removed
ON user (removed);

CREATE TABLE user_authentication (
    user_uuid TEXT NOT NULL PRIMARY KEY,
    disabled BOOLEAN NOT NULL,
    CONSTRAINT fk_user_authentication_user
    FOREIGN KEY (user_uuid)
    REFERENCES user (uuid)
);

CREATE INDEX idx_user_authentication_disabled_user_uuid
ON user_authentication (disabled, user_uuid);

CREATE TABLE user_password (
    user_uuid TEXT NOT NULL PRIMARY KEY,
    password_hash TEXT NOT NULL,
    password_salt TEXT NOT NULL,
    CONSTRAINT fk_user_password_user
    FOREIGN KEY (user_uuid)
    REFERENCES user_authentication (user_uuid)
);

CREATE TABLE user_activation_key (
    user_uuid TEXT NOT NULL PRIMARY KEY,
    activation_key TEXT NOT NULL,
    CONSTRAINT fk_user_activation_key_user
    FOREIGN KEY (user_uuid)
    REFERENCES user_authentication (user_uuid)
);

CREATE VIEW v_user_auth AS
SELECT
    u.uuid,
    u.name,
    u.display_name,
    u.external,
    u.removed,
    u.created_by_uuid,
    u.created_at,
    a.disabled
FROM user AS u LEFT JOIN user_authentication AS a ON u.uuid = a.user_uuid;

CREATE TABLE flag (
    name TEXT NOT NULL PRIMARY KEY,
    value BOOLEAN DEFAULT 0,
    description TEXT NOT NULL
);

CREATE TABLE permission_access_type (
    id INT PRIMARY KEY,
    type TEXT NOT NULL
);

CREATE UNIQUE INDEX idx_permission_access_type
ON permission_access_type (type);

-- Maps to the Access type in core/permission package.
INSERT INTO permission_access_type VALUES
(0, 'read'),
(1, 'write'),
(2, 'consume'),
(3, 'admin'),
(4, 'login'),
(5, 'add-model'),
(6, 'superuser');

CREATE TABLE permission_object_type (
    id INT PRIMARY KEY,
    type TEXT NOT NULL
);

CREATE UNIQUE INDEX idx_permission_object_type
ON permission_object_type (type);

-- Maps to the ObjectType type in core/permission package.
INSERT INTO permission_object_type VALUES
(0, 'cloud'),
(1, 'controller'),
(2, 'model'),
(3, 'offer');

CREATE TABLE permission_object_access (
    id INT PRIMARY KEY,
    access_type_id INT NOT NULL,
    object_type_id INT NOT NULL,
    CONSTRAINT fk_permission_access_type
    FOREIGN KEY (access_type_id)
    REFERENCES permission_access_type (id),
    CONSTRAINT fk_permission_object_type
    FOREIGN KEY (object_type_id)
    REFERENCES permission_object_type (id)
);

CREATE UNIQUE INDEX idx_permission_object_access
ON permission_object_access (access_type_id, object_type_id);

INSERT INTO permission_object_access VALUES
(0, 3, 0), -- admin, cloud
(1, 5, 0), -- add-model, cloud
(2, 4, 1), -- login, controller
(3, 6, 1), -- superuser, controller
(4, 0, 2), -- read, model
(5, 1, 2), -- write, model
(6, 3, 2), -- admin, model
(7, 0, 3), -- read, offer
(8, 2, 3), -- consume, offer
(9, 3, 3); -- admin, offer

-- Column grant_to may extend to entities beyond users.
-- The name of the column is general, but for now we retain the FK constraint.
-- We will need to remove/replace it in the event of change
CREATE TABLE permission (
    uuid TEXT NOT NULL PRIMARY KEY,
    access_type_id INT NOT NULL,
    object_type_id INT NOT NULL,
    grant_on TEXT NOT NULL, -- name or uuid of the object
    grant_to TEXT NOT NULL,
    CONSTRAINT fk_permission_user_uuid
    FOREIGN KEY (grant_to)
    REFERENCES user (uuid),
    CONSTRAINT fk_permission_object_access
    FOREIGN KEY (access_type_id, object_type_id)
    REFERENCES permission_object_access (access_type_id, object_type_id)
);

-- Allow only 1 combination of grant_on and grant_to
-- Otherwise we will get conflicting permissions.
CREATE UNIQUE INDEX idx_permission_type_to
ON permission (grant_on, grant_to);

CREATE INDEX idx_permission_grant_to
ON permission (grant_to);

CREATE INDEX idx_permission_object_type_grant_on
ON permission (object_type_id, grant_on);

-- All permissions
CREATE VIEW v_permission AS
SELECT
    p.uuid,
    p.grant_on,
    p.grant_to,
    at.type AS access_type,
    ot.type AS object_type
FROM permission AS p
JOIN permission_access_type AS at ON p.access_type_id = at.id
JOIN permission_object_type AS ot ON p.object_type_id = ot.id;

-- All model permissions, verifying the model does exist.
CREATE VIEW v_permission_model AS
SELECT
    p.uuid,
    p.grant_on,
    p.grant_to,
    p.access_type,
    p.object_type
FROM v_permission AS p
JOIN model ON p.grant_on = model.uuid
WHERE p.object_type = 'model';

-- All controller cloud, verifying the cloud does exist.
CREATE VIEW v_permission_cloud AS
SELECT
    p.uuid,
    p.grant_on,
    p.grant_to,
    p.access_type,
    p.object_type
FROM v_permission AS p
JOIN cloud ON p.grant_on = cloud.name
WHERE p.object_type = 'cloud';

-- All controller permissions, verifying the controller does exists.
CREATE VIEW v_permission_controller AS
SELECT
    p.uuid,
    p.grant_on,
    p.grant_to,
    p.access_type,
    p.object_type
FROM v_permission AS p
JOIN controller ON p.grant_on = controller.uuid
WHERE p.object_type = 'controller';

-- All offer permissions, NOT verifying the offer does exist.
CREATE VIEW v_permission_offer AS
SELECT
    p.uuid,
    p.grant_on,
    p.grant_to,
    p.access_type,
    p.object_type
FROM v_permission AS p
WHERE p.object_type = 'offer';

-- The permissions for the special user everyone@external.
CREATE VIEW v_everyone_external AS
SELECT
    p.uuid,
    p.grant_on,
    p.grant_to,
    p.access_type,
    p.object_type
FROM v_permission AS p
JOIN user AS u ON p.grant_to = u.uuid
WHERE u.name = 'everyone@external';

-- Controller database tables for secret backends.

CREATE TABLE secret_backend_type (
    id INT PRIMARY KEY,
    type TEXT NOT NULL,
    description TEXT,
    CONSTRAINT chk_empty_type
    CHECK (type != '')
);

CREATE UNIQUE INDEX idx_secret_backend_type_type
ON secret_backend_type (type);

INSERT INTO secret_backend_type VALUES
(0, 'controller', 'the juju controller secret backend'),
(1, 'kubernetes', 'the kubernetes secret backend'),
(2, 'vault', 'the vault secret backend');

CREATE TABLE secret_backend_origin (
    id INT NOT NULL PRIMARY KEY,
    origin TEXT NOT NULL UNIQUE,
    CONSTRAINT chk_secret_backend_origin_not_empty
    CHECK (origin != '')
);

INSERT INTO secret_backend_origin (id, origin) VALUES
(0, 'built-in'),
(1, 'user');

CREATE TABLE secret_backend (
    uuid TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    backend_type_id INT NOT NULL,
    token_rotate_interval INT,
    origin_id INT NOT NULL DEFAULT 1,
    CONSTRAINT chk_empty_name
    CHECK (name != ''),
    CONSTRAINT fk_secret_backend_type_id
    FOREIGN KEY (backend_type_id)
    REFERENCES secret_backend_type (id)
);

CREATE UNIQUE INDEX idx_secret_backend_name
ON secret_backend (name);

CREATE TABLE secret_backend_config (
    backend_uuid TEXT NOT NULL,
    name TEXT NOT NULL,
    content TEXT NOT NULL,
    CONSTRAINT chk_empty_name
    CHECK (name != ''),
    CONSTRAINT chk_empty_content
    CHECK (content != ''),
    CONSTRAINT pk_secret_backend_config
    PRIMARY KEY (backend_uuid, name),
    CONSTRAINT fk_secret_backend_config_backend_uuid
    FOREIGN KEY (backend_uuid)
    REFERENCES secret_backend (uuid)
);

CREATE TABLE secret_backend_rotation (
    backend_uuid TEXT NOT NULL PRIMARY KEY,
    next_rotation_time DATETIME NOT NULL,
    CONSTRAINT fk_secret_backend_rotation_secret_backend_uuid
    FOREIGN KEY (backend_uuid)
    REFERENCES secret_backend (uuid)
);

CREATE TABLE secret_backend_reference (
    secret_backend_uuid TEXT NOT NULL,
    model_uuid TEXT NOT NULL,
    secret_revision_uuid TEXT NOT NULL,
    secret_id TEXT NOT NULL,
    CONSTRAINT pk_secret_backend_reference
    PRIMARY KEY (secret_backend_uuid, model_uuid, secret_revision_uuid),
    CONSTRAINT fk_secret_backend_reference_model_uuid
    FOREIGN KEY (model_uuid)
    REFERENCES model (uuid),
    CONSTRAINT fk_secret_backend_reference_secret_backend_uuid
    FOREIGN KEY (secret_backend_uuid)
    REFERENCES secret_backend (uuid)
);

CREATE INDEX idx_secret_backend_reference_revision
ON secret_backend_reference (secret_revision_uuid);

CREATE TABLE model_secret_backend (
    model_uuid TEXT NOT NULL PRIMARY KEY,
    secret_backend_uuid TEXT NOT NULL,
    CONSTRAINT fk_model_secret_backend_model_uuid
    FOREIGN KEY (model_uuid)
    REFERENCES model (uuid),
    CONSTRAINT fk_model_secret_backend_secret_backend_uuid
    FOREIGN KEY (secret_backend_uuid)
    REFERENCES secret_backend (uuid)
);

CREATE VIEW v_model_secret_backend AS
SELECT
    m.uuid,
    m.name,
    mt.type AS model_type,
    msb.secret_backend_uuid,
    sb.name AS secret_backend_name,
    (SELECT uuid FROM controller) AS controller_uuid
FROM model_secret_backend AS msb
JOIN secret_backend AS sb ON msb.secret_backend_uuid = sb.uuid
JOIN model AS m ON msb.model_uuid = m.uuid
JOIN model_type AS mt ON m.model_type_id = mt.id;

CREATE TABLE model_last_login (
    model_uuid TEXT NOT NULL,
    user_uuid TEXT NOT NULL,
    time TIMESTAMP NOT NULL,
    PRIMARY KEY (model_uuid, user_uuid),
    CONSTRAINT fk_model_last_login_model
    FOREIGN KEY (model_uuid)
    REFERENCES model (uuid),
    CONSTRAINT fk_model_last_login_user
    FOREIGN KEY (user_uuid)
    REFERENCES user (uuid)
);

CREATE INDEX idx_model_last_login_user_uuid_time
ON model_last_login (user_uuid, time);

CREATE VIEW v_user_last_login AS
-- We cannot select last_login as MAX directly here because it returns a sqlite
-- string value, not a timestamp and this stops us scanning into time.Time.
SELECT
    time AS last_login,
    user_uuid,
    MAX(time) AS t
FROM model_last_login
GROUP BY user_uuid;

CREATE TABLE bakery_config (
    local_users_private_key TEXT NOT NULL,
    local_users_public_key TEXT NOT NULL,
    local_users_third_party_private_key TEXT NOT NULL,
    local_users_third_party_public_key TEXT NOT NULL,
    external_users_third_party_private_key TEXT NOT NULL,
    external_users_third_party_public_key TEXT NOT NULL,
    offers_third_party_private_key TEXT NOT NULL,
    offers_third_party_public_key TEXT NOT NULL
);

-- A unique constraint over a constant index ensures only 1 entry matching the
-- condition can exist.
CREATE UNIQUE INDEX idx_singleton_bakery_config ON bakery_config ((1));

CREATE TABLE macaroon_root_key (
    id TEXT NOT NULL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    root_key TEXT NOT NULL
);

CREATE INDEX idx_macaroon_root_key_expires_at
ON macaroon_root_key (expires_at);

CREATE INDEX idx_macaroon_root_key_created_expires
ON macaroon_root_key (created_at DESC, expires_at);

CREATE TABLE ssh_fingerprint_hash_algorithm (
    id INT PRIMARY KEY,
    algorithm TEXT NOT NULL
);

CREATE UNIQUE INDEX idx_ssh_fingerprint_hash_algorithm_algorithm
ON ssh_fingerprint_hash_algorithm (algorithm);

INSERT INTO ssh_fingerprint_hash_algorithm VALUES
(0, 'md5'),
(1, 'sha256');

CREATE TABLE user_public_ssh_key (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- comment is the comment string set in the public key. We also retain this
    -- value in public_key. This column exists to make an index for deletion.
    comment TEXT NOT NULL,
    fingerprint_hash_algorithm_id INT NOT NULL,
    fingerprint TEXT NOT NULL,
    public_key TEXT NOT NULL,
    user_uuid TEXT NOT NULL,
    FOREIGN KEY (fingerprint_hash_algorithm_id)
    REFERENCES ssh_fingerprint_hash_algorithm (id),
    FOREIGN KEY (user_uuid)
    REFERENCES user (uuid)
);

CREATE UNIQUE INDEX idx_user_public_ssh_key_user_fingerprint
ON user_public_ssh_key (user_uuid, fingerprint);

CREATE UNIQUE INDEX idx_user_public_ssh_key_user_public_key
ON user_public_ssh_key (user_uuid, public_key);

CREATE INDEX idx_user_public_ssh_key_user_comment
ON user_public_ssh_key (user_uuid, comment);

CREATE TABLE model_authorized_keys (
    model_uuid TEXT NOT NULL,
    user_public_ssh_key_id INTEGER NOT NULL,
    PRIMARY KEY (model_uuid, user_public_ssh_key_id),
    FOREIGN KEY (user_public_ssh_key_id)
    REFERENCES user_public_ssh_key (id),
    FOREIGN KEY (model_uuid)
    REFERENCES model (uuid)
);

--CREATE UNIQUE INDEX idx_model_authorized_keys_composite
--ON model_authorized_keys (model_uuid, user_public_ssh_key_id);

CREATE INDEX idx_model_authorized_keys_model_uuid
ON model_authorized_keys (model_uuid);

CREATE INDEX idx_model_authorized_keys_model_uuid_user_public_ssh_key_id
ON model_authorized_keys (user_public_ssh_key_id);

-- v_model_authorized_keys provides a nice view of what public ssh keys are
-- currently allowed on a model making sure that users that are removed and or
-- disabled have thier authorized keys removed from the model.
CREATE VIEW v_model_authorized_keys AS
SELECT
    mak.model_uuid,
    upsk.public_key,
    upsk.user_uuid
FROM model_authorized_keys AS mak
JOIN user_public_ssh_key AS upsk ON mak.user_public_ssh_key_id = upsk.id
JOIN user AS u ON upsk.user_uuid = u.uuid
JOIN user_authentication AS ua ON u.uuid = ua.user_uuid
WHERE
    u.removed = FALSE
    AND ua.disabled = FALSE;

CREATE TABLE architecture (
    id INT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE UNIQUE INDEX idx_architecture_name
ON architecture (name);

INSERT INTO architecture VALUES
(0, 'amd64'),
(1, 'arm64'),
(2, 'ppc64el'),
(3, 's390x'),
(4, 'riscv64');

CREATE TABLE cloud_image_metadata (
    uuid TEXT NOT NULL PRIMARY KEY,
    created_at DATETIME NOT NULL,
    source TEXT NOT NULL,
    stream TEXT NOT NULL,
    region TEXT NOT NULL,
    version TEXT NOT NULL,
    architecture_id INT NOT NULL,
    virt_type TEXT NOT NULL,
    root_storage_type TEXT NOT NULL,
    root_storage_size INT,
    priority INT,
    image_id TEXT NOT NULL,
    CONSTRAINT fk_cloud_image_metadata_arch
    FOREIGN KEY (architecture_id)
    REFERENCES architecture (id)
);

CREATE UNIQUE INDEX idx_cloud_image_metadata_unique_fields
ON cloud_image_metadata (stream, region, version, architecture_id, virt_type, root_storage_type, source);

CREATE INDEX idx_cloud_image_metadata_source
ON cloud_image_metadata (source);

CREATE INDEX idx_cloud_image_metadata_created_at
ON cloud_image_metadata (created_at);

CREATE INDEX idx_cloud_image_metadata_image_id
ON cloud_image_metadata (image_id);

-- The agent_binary_store table in the controller database records information about
-- the agent binaries stored in the controller's object store, including their version, SHA,
-- architecture, and the object store reference.
-- This table tracks agent binaries available across the whole Juju controller
-- for use by any model.
CREATE TABLE agent_binary_store (
    version TEXT NOT NULL,
    architecture_id INT NOT NULL,
    object_store_uuid TEXT NOT NULL,
    PRIMARY KEY (version, architecture_id),
    CONSTRAINT fk_agent_binary_metadata_object_store_metadata
    FOREIGN KEY (object_store_uuid)
    REFERENCES object_store_metadata (uuid),
    CONSTRAINT fk_agent_binary_metadata_architecture
    FOREIGN KEY (architecture_id)
    REFERENCES architecture (id)
);

CREATE VIEW v_agent_binary_store AS
SELECT
    abs.version,
    abs.object_store_uuid,
    abs.architecture_id,
    a.name AS architecture_name,
    osm.size,
    osm.sha_256,
    osm.sha_384,
    osmp.path
FROM agent_binary_store AS abs
JOIN architecture AS a ON abs.architecture_id = a.id
JOIN object_store_metadata AS osm ON abs.object_store_uuid = osm.uuid
JOIN object_store_metadata_path AS osmp ON osm.uuid = osmp.metadata_uuid;

CREATE INDEX idx_agent_binary_store_object_store_uuid
ON agent_binary_store (object_store_uuid);

CREATE TABLE charm_tracing_config (
    "key" TEXT NOT NULL PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE logging_loki_config (
    uuid TEXT NOT NULL PRIMARY KEY,
    endpoint TEXT NOT NULL,
    ca_cert TEXT NOT NULL DEFAULT '',
    insecure_skip_verify BOOLEAN NULL,
    org_id TEXT NOT NULL DEFAULT ''
);

CREATE UNIQUE INDEX idx_singleton_logging_loki_config ON logging_loki_config ((1));

CREATE TABLE workload_tracing_config (
    "key" TEXT NOT NULL PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE ssh_key_algorithm_type (
    id INT PRIMARY KEY,
    type TEXT NOT NULL
);

CREATE UNIQUE INDEX idx_ssh_key_algorithm_type_type
ON ssh_key_algorithm_type (type);

INSERT INTO ssh_key_algorithm_type VALUES
(0, 'ssh-rsa'),
(1, 'ecdsa-sha2-nistp256'),
(2, 'ssh-ed25519');

CREATE TABLE controller_ssh_host_key (
    id TEXT NOT NULL PRIMARY KEY,
    algorithm_type_id INT NOT NULL,
    ssh_key TEXT NOT NULL,
    public_key BLOB NOT NULL DEFAULT '',
    CONSTRAINT fk_controller_ssh_host_key_algorithm_type_id
    FOREIGN KEY (algorithm_type_id)
    REFERENCES ssh_key_algorithm_type (id)
);

CREATE UNIQUE INDEX idx_singleton_controller_ssh_host_key
ON controller_ssh_host_key ((1));

-- controller_ssh_server_port holds the port the controller's embedded SSH
-- jump server listens on. It is a singleton (only one row) and is owned by the
-- controller charm, which pushes changes via the control socket. The SSH
-- server worker watches this table and restarts on the configured port.
CREATE TABLE controller_ssh_server_port (
    port INT NOT NULL
);

CREATE UNIQUE INDEX idx_singleton_controller_ssh_server_port
ON controller_ssh_server_port ((1));

-- model_database_deletion stages deletions of a purged model's dqlite
-- database for the model DB deleter worker to process asynchronously.
--
-- When a model is purged from the controller database while its dqlite
-- database must outlive the purge transaction (source-side model migration
-- REAP), a row is staged here inside that same transaction. The model DB
-- deleter worker on each controller node watches this table, deletes the
-- database, and removes the row on success, retrying on failure.
--
-- The table is deliberately standalone with no FK to model: the model row is
-- gone by the time a row exists here.
CREATE TABLE model_database_deletion (
    namespace TEXT NOT NULL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL
);


-- insert namespace for Cloud
INSERT INTO change_log_namespace VALUES (10007, 'cloud', 'Cloud changes based on uuid');

-- insert trigger for Cloud
CREATE TRIGGER trg_log_cloud_insert
AFTER INSERT ON cloud FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10007, NEW.uuid, DATETIME('now', 'utc'));
END;

-- update trigger for Cloud
CREATE TRIGGER trg_log_cloud_update
AFTER UPDATE ON cloud FOR EACH ROW
WHEN 
	NEW.uuid != OLD.uuid OR
	NEW.name != OLD.name OR
	NEW.cloud_type_id != OLD.cloud_type_id OR
	NEW.endpoint != OLD.endpoint OR
	(NEW.identity_endpoint != OLD.identity_endpoint OR (NEW.identity_endpoint IS NOT NULL AND OLD.identity_endpoint IS NULL) OR (NEW.identity_endpoint IS NULL AND OLD.identity_endpoint IS NOT NULL)) OR
	(NEW.storage_endpoint != OLD.storage_endpoint OR (NEW.storage_endpoint IS NOT NULL AND OLD.storage_endpoint IS NULL) OR (NEW.storage_endpoint IS NULL AND OLD.storage_endpoint IS NOT NULL)) OR
	NEW.skip_tls_verify != OLD.skip_tls_verify
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10007, OLD.uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for Cloud
CREATE TRIGGER trg_log_cloud_delete
AFTER DELETE ON cloud FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10007, OLD.uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for CloudCaCert
INSERT INTO change_log_namespace VALUES (10008, 'cloud_ca_cert', 'CloudCaCert changes based on cloud_uuid');

-- insert trigger for CloudCaCert
CREATE TRIGGER trg_log_cloud_ca_cert_insert
AFTER INSERT ON cloud_ca_cert FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10008, NEW.cloud_uuid, DATETIME('now', 'utc'));
END;

-- update trigger for CloudCaCert
CREATE TRIGGER trg_log_cloud_ca_cert_update
AFTER UPDATE ON cloud_ca_cert FOR EACH ROW
WHEN 
	NEW.cloud_uuid != OLD.cloud_uuid OR
	NEW.ca_cert != OLD.ca_cert
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10008, OLD.cloud_uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for CloudCaCert
CREATE TRIGGER trg_log_cloud_ca_cert_delete
AFTER DELETE ON cloud_ca_cert FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10008, OLD.cloud_uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for CloudCredential
INSERT INTO change_log_namespace VALUES (10009, 'cloud_credential', 'CloudCredential changes based on uuid');

-- insert trigger for CloudCredential
CREATE TRIGGER trg_log_cloud_credential_insert
AFTER INSERT ON cloud_credential FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10009, NEW.uuid, DATETIME('now', 'utc'));
END;

-- update trigger for CloudCredential
CREATE TRIGGER trg_log_cloud_credential_update
AFTER UPDATE ON cloud_credential FOR EACH ROW
WHEN 
	NEW.uuid != OLD.uuid OR
	NEW.cloud_uuid != OLD.cloud_uuid OR
	NEW.auth_type_id != OLD.auth_type_id OR
	NEW.owner_uuid != OLD.owner_uuid OR
	NEW.name != OLD.name OR
	(NEW.revoked != OLD.revoked OR (NEW.revoked IS NOT NULL AND OLD.revoked IS NULL) OR (NEW.revoked IS NULL AND OLD.revoked IS NOT NULL)) OR
	(NEW.invalid != OLD.invalid OR (NEW.invalid IS NOT NULL AND OLD.invalid IS NULL) OR (NEW.invalid IS NULL AND OLD.invalid IS NOT NULL)) OR
	(NEW.invalid_reason != OLD.invalid_reason OR (NEW.invalid_reason IS NOT NULL AND OLD.invalid_reason IS NULL) OR (NEW.invalid_reason IS NULL AND OLD.invalid_reason IS NOT NULL))
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10009, OLD.uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for CloudCredential
CREATE TRIGGER trg_log_cloud_credential_delete
AFTER DELETE ON cloud_credential FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10009, OLD.uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for CloudCredentialAttribute
INSERT INTO change_log_namespace VALUES (10010, 'cloud_credential_attribute', 'CloudCredentialAttribute changes based on cloud_credential_uuid');

-- insert trigger for CloudCredentialAttribute
CREATE TRIGGER trg_log_cloud_credential_attribute_insert
AFTER INSERT ON cloud_credential_attribute FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10010, NEW.cloud_credential_uuid, DATETIME('now', 'utc'));
END;

-- update trigger for CloudCredentialAttribute
CREATE TRIGGER trg_log_cloud_credential_attribute_update
AFTER UPDATE ON cloud_credential_attribute FOR EACH ROW
WHEN 
	NEW.cloud_credential_uuid != OLD.cloud_credential_uuid OR
	NEW.key != OLD.key OR
	(NEW.value != OLD.value OR (NEW.value IS NOT NULL AND OLD.value IS NULL) OR (NEW.value IS NULL AND OLD.value IS NOT NULL))
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10010, OLD.cloud_credential_uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for CloudCredentialAttribute
CREATE TRIGGER trg_log_cloud_credential_attribute_delete
AFTER DELETE ON cloud_credential_attribute FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10010, OLD.cloud_credential_uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for ExternalController
INSERT INTO change_log_namespace VALUES (10000, 'external_controller', 'ExternalController changes based on uuid');

-- insert trigger for ExternalController
CREATE TRIGGER trg_log_external_controller_insert
AFTER INSERT ON external_controller FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10000, NEW.uuid, DATETIME('now', 'utc'));
END;

-- update trigger for ExternalController
CREATE TRIGGER trg_log_external_controller_update
AFTER UPDATE ON external_controller FOR EACH ROW
WHEN 
	NEW.uuid != OLD.uuid OR
	(NEW.alias != OLD.alias OR (NEW.alias IS NOT NULL AND OLD.alias IS NULL) OR (NEW.alias IS NULL AND OLD.alias IS NOT NULL)) OR
	NEW.ca_cert != OLD.ca_cert
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10000, OLD.uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for ExternalController
CREATE TRIGGER trg_log_external_controller_delete
AFTER DELETE ON external_controller FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10000, OLD.uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for ControllerConfig
INSERT INTO change_log_namespace VALUES (10002, 'controller_config', 'ControllerConfig changes based on key');

-- insert trigger for ControllerConfig
CREATE TRIGGER trg_log_controller_config_insert
AFTER INSERT ON controller_config FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10002, NEW.key, DATETIME('now', 'utc'));
END;

-- update trigger for ControllerConfig
CREATE TRIGGER trg_log_controller_config_update
AFTER UPDATE ON controller_config FOR EACH ROW
WHEN 
	NEW.key != OLD.key OR
	(NEW.value != OLD.value OR (NEW.value IS NOT NULL AND OLD.value IS NULL) OR (NEW.value IS NULL AND OLD.value IS NOT NULL))
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10002, OLD.key, DATETIME('now', 'utc'));
END;
-- delete trigger for ControllerConfig
CREATE TRIGGER trg_log_controller_config_delete
AFTER DELETE ON controller_config FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10002, OLD.key, DATETIME('now', 'utc'));
END;

-- insert namespace for ControllerNode
INSERT INTO change_log_namespace VALUES (10001, 'controller_node', 'ControllerNode changes based on controller_id');

-- insert trigger for ControllerNode
CREATE TRIGGER trg_log_controller_node_insert
AFTER INSERT ON controller_node FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10001, NEW.controller_id, DATETIME('now', 'utc'));
END;

-- update trigger for ControllerNode
CREATE TRIGGER trg_log_controller_node_update
AFTER UPDATE ON controller_node FOR EACH ROW
WHEN 
	NEW.controller_id != OLD.controller_id OR
	NEW.life_id != OLD.life_id OR
	(NEW.dqlite_node_id != OLD.dqlite_node_id OR (NEW.dqlite_node_id IS NOT NULL AND OLD.dqlite_node_id IS NULL) OR (NEW.dqlite_node_id IS NULL AND OLD.dqlite_node_id IS NOT NULL)) OR
	(NEW.dqlite_bind_address != OLD.dqlite_bind_address OR (NEW.dqlite_bind_address IS NOT NULL AND OLD.dqlite_bind_address IS NULL) OR (NEW.dqlite_bind_address IS NULL AND OLD.dqlite_bind_address IS NOT NULL))
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10001, OLD.controller_id, DATETIME('now', 'utc'));
END;
-- delete trigger for ControllerNode
CREATE TRIGGER trg_log_controller_node_delete
AFTER DELETE ON controller_node FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10001, OLD.controller_id, DATETIME('now', 'utc'));
END;

-- insert namespace for ControllerApiAddress
INSERT INTO change_log_namespace VALUES (10003, 'controller_api_address', 'ControllerApiAddress changes based on controller_id');

-- insert trigger for ControllerApiAddress
CREATE TRIGGER trg_log_controller_api_address_insert
AFTER INSERT ON controller_api_address FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10003, NEW.controller_id, DATETIME('now', 'utc'));
END;

-- update trigger for ControllerApiAddress
CREATE TRIGGER trg_log_controller_api_address_update
AFTER UPDATE ON controller_api_address FOR EACH ROW
WHEN 
	NEW.controller_id != OLD.controller_id OR
	NEW.address != OLD.address OR
	(NEW.is_agent != OLD.is_agent OR (NEW.is_agent IS NOT NULL AND OLD.is_agent IS NULL) OR (NEW.is_agent IS NULL AND OLD.is_agent IS NOT NULL)) OR
	NEW.scope != OLD.scope
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10003, OLD.controller_id, DATETIME('now', 'utc'));
END;
-- delete trigger for ControllerApiAddress
CREATE TRIGGER trg_log_controller_api_address_delete
AFTER DELETE ON controller_api_address FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10003, OLD.controller_id, DATETIME('now', 'utc'));
END;

-- insert namespace for ControllerAgentAddress
INSERT INTO change_log_namespace VALUES (10025, 'controller_agent_address', 'ControllerAgentAddress changes based on uuid');

-- insert trigger for ControllerAgentAddress
CREATE TRIGGER trg_log_controller_agent_address_insert
AFTER INSERT ON controller_agent_address FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10025, NEW.uuid, DATETIME('now', 'utc'));
END;

-- update trigger for ControllerAgentAddress
CREATE TRIGGER trg_log_controller_agent_address_update
AFTER UPDATE ON controller_agent_address FOR EACH ROW
WHEN 
	NEW.uuid != OLD.uuid OR
	(NEW.controller_id != OLD.controller_id OR (NEW.controller_id IS NOT NULL AND OLD.controller_id IS NULL) OR (NEW.controller_id IS NULL AND OLD.controller_id IS NOT NULL)) OR
	NEW.address != OLD.address OR
	NEW.scope != OLD.scope OR
	NEW.priority != OLD.priority
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10025, OLD.uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for ControllerAgentAddress
CREATE TRIGGER trg_log_controller_agent_address_delete
AFTER DELETE ON controller_agent_address FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10025, OLD.uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for ControllerClientAddress
INSERT INTO change_log_namespace VALUES (10026, 'controller_client_address', 'ControllerClientAddress changes based on uuid');

-- insert trigger for ControllerClientAddress
CREATE TRIGGER trg_log_controller_client_address_insert
AFTER INSERT ON controller_client_address FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10026, NEW.uuid, DATETIME('now', 'utc'));
END;

-- update trigger for ControllerClientAddress
CREATE TRIGGER trg_log_controller_client_address_update
AFTER UPDATE ON controller_client_address FOR EACH ROW
WHEN 
	NEW.uuid != OLD.uuid OR
	(NEW.controller_id != OLD.controller_id OR (NEW.controller_id IS NOT NULL AND OLD.controller_id IS NULL) OR (NEW.controller_id IS NULL AND OLD.controller_id IS NOT NULL)) OR
	NEW.address != OLD.address OR
	NEW.scope != OLD.scope OR
	NEW.priority != OLD.priority
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10026, OLD.uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for ControllerClientAddress
CREATE TRIGGER trg_log_controller_client_address_delete
AFTER DELETE ON controller_client_address FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10026, OLD.uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for ControllerPeerAddress
INSERT INTO change_log_namespace VALUES (10027, 'controller_peer_address', 'ControllerPeerAddress changes based on controller_id');

-- insert trigger for ControllerPeerAddress
CREATE TRIGGER trg_log_controller_peer_address_insert
AFTER INSERT ON controller_peer_address FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10027, NEW.controller_id, DATETIME('now', 'utc'));
END;

-- update trigger for ControllerPeerAddress
CREATE TRIGGER trg_log_controller_peer_address_update
AFTER UPDATE ON controller_peer_address FOR EACH ROW
WHEN 
	NEW.uuid != OLD.uuid OR
	NEW.controller_id != OLD.controller_id OR
	NEW.address != OLD.address OR
	NEW.scope != OLD.scope OR
	NEW.priority != OLD.priority
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10027, OLD.controller_id, DATETIME('now', 'utc'));
END;
-- delete trigger for ControllerPeerAddress
CREATE TRIGGER trg_log_controller_peer_address_delete
AFTER DELETE ON controller_peer_address FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10027, OLD.controller_id, DATETIME('now', 'utc'));
END;

-- insert namespace for ModelMigrationExport
INSERT INTO change_log_namespace VALUES (10004, 'model_migration_export', 'ModelMigrationExport changes based on model_uuid');

-- insert trigger for ModelMigrationExport
CREATE TRIGGER trg_log_model_migration_export_insert
AFTER INSERT ON model_migration_export FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10004, NEW.model_uuid, DATETIME('now', 'utc'));
END;

-- update trigger for ModelMigrationExport
CREATE TRIGGER trg_log_model_migration_export_update
AFTER UPDATE ON model_migration_export FOR EACH ROW
WHEN 
	NEW.uuid != OLD.uuid OR
	NEW.model_uuid != OLD.model_uuid OR
	NEW.target_controller_uuid != OLD.target_controller_uuid OR
	NEW.start_time != OLD.start_time OR
	(
		OLD.current_phase_id NOT IN (7, 8, 10) AND
		NEW.current_phase_id IN (7, 8, 10)
	) OR
	(
		OLD.current_phase_id IN (7, 8, 10) AND
		NEW.current_phase_id NOT IN (7, 8, 10)
	)
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10004, OLD.model_uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for ModelMigrationExport
CREATE TRIGGER trg_log_model_migration_export_delete
AFTER DELETE ON model_migration_export FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10004, OLD.model_uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for ModelMigrationExportPhase
INSERT INTO change_log_namespace VALUES (10005, 'model_migration_export_phase', 'ModelMigrationExportPhase changes based on model_uuid');

-- insert trigger for ModelMigrationExportPhase
CREATE TRIGGER trg_log_model_migration_export_phase_insert
AFTER INSERT ON model_migration_export_phase FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10005, NEW.model_uuid, DATETIME('now', 'utc'));
END;

-- update trigger for ModelMigrationExportPhase
CREATE TRIGGER trg_log_model_migration_export_phase_update
AFTER UPDATE ON model_migration_export_phase FOR EACH ROW
WHEN 
	NEW.migration_uuid != OLD.migration_uuid OR
	NEW.model_uuid != OLD.model_uuid OR
	NEW.phase_id != OLD.phase_id OR
	NEW.changed_at != OLD.changed_at
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10005, OLD.model_uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for ModelMigrationExportPhase
CREATE TRIGGER trg_log_model_migration_export_phase_delete
AFTER DELETE ON model_migration_export_phase FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10005, OLD.model_uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for ModelMigrationExportMinionSync
INSERT INTO change_log_namespace VALUES (10021, 'model_migration_export_minion_sync', 'ModelMigrationExportMinionSync changes based on migration_uuid');

-- insert trigger for ModelMigrationExportMinionSync
CREATE TRIGGER trg_log_model_migration_export_minion_sync_insert
AFTER INSERT ON model_migration_export_minion_sync FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10021, NEW.migration_uuid, DATETIME('now', 'utc'));
END;

-- update trigger for ModelMigrationExportMinionSync
CREATE TRIGGER trg_log_model_migration_export_minion_sync_update
AFTER UPDATE ON model_migration_export_minion_sync FOR EACH ROW
WHEN 
	NEW.migration_uuid != OLD.migration_uuid OR
	NEW.phase_id != OLD.phase_id OR
	NEW.entity_key != OLD.entity_key OR
	NEW.success != OLD.success OR
	NEW.reported_at != OLD.reported_at
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10021, OLD.migration_uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for ModelMigrationExportMinionSync
CREATE TRIGGER trg_log_model_migration_export_minion_sync_delete
AFTER DELETE ON model_migration_export_minion_sync FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10021, OLD.migration_uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for ModelMigrationImport
INSERT INTO change_log_namespace VALUES (10024, 'model_migration_import', 'ModelMigrationImport changes based on model_uuid');

-- insert trigger for ModelMigrationImport
CREATE TRIGGER trg_log_model_migration_import_insert
AFTER INSERT ON model_migration_import FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10024, NEW.model_uuid, DATETIME('now', 'utc'));
END;

-- update trigger for ModelMigrationImport
CREATE TRIGGER trg_log_model_migration_import_update
AFTER UPDATE ON model_migration_import FOR EACH ROW
WHEN 
	NEW.uuid != OLD.uuid OR
	NEW.model_uuid != OLD.model_uuid OR
	NEW.source_migration_uuid != OLD.source_migration_uuid OR
	NEW.phase_type_id != OLD.phase_type_id OR
	NEW.updated_at != OLD.updated_at
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10024, OLD.model_uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for ModelMigrationImport
CREATE TRIGGER trg_log_model_migration_import_delete
AFTER DELETE ON model_migration_import FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10024, OLD.model_uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for UpgradeInfo
INSERT INTO change_log_namespace VALUES (10006, 'upgrade_info', 'UpgradeInfo changes based on uuid');

-- insert trigger for UpgradeInfo
CREATE TRIGGER trg_log_upgrade_info_insert
AFTER INSERT ON upgrade_info FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10006, NEW.uuid, DATETIME('now', 'utc'));
END;

-- update trigger for UpgradeInfo
CREATE TRIGGER trg_log_upgrade_info_update
AFTER UPDATE ON upgrade_info FOR EACH ROW
WHEN 
	NEW.uuid != OLD.uuid OR
	NEW.previous_version != OLD.previous_version OR
	NEW.target_version != OLD.target_version OR
	NEW.state_type_id != OLD.state_type_id
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10006, OLD.uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for UpgradeInfo
CREATE TRIGGER trg_log_upgrade_info_delete
AFTER DELETE ON upgrade_info FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10006, OLD.uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for UpgradeInfoControllerNode
INSERT INTO change_log_namespace VALUES (10011, 'upgrade_info_controller_node', 'UpgradeInfoControllerNode changes based on upgrade_info_uuid');

-- insert trigger for UpgradeInfoControllerNode
CREATE TRIGGER trg_log_upgrade_info_controller_node_insert
AFTER INSERT ON upgrade_info_controller_node FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10011, NEW.upgrade_info_uuid, DATETIME('now', 'utc'));
END;

-- update trigger for UpgradeInfoControllerNode
CREATE TRIGGER trg_log_upgrade_info_controller_node_update
AFTER UPDATE ON upgrade_info_controller_node FOR EACH ROW
WHEN 
	NEW.uuid != OLD.uuid OR
	NEW.controller_node_id != OLD.controller_node_id OR
	NEW.upgrade_info_uuid != OLD.upgrade_info_uuid OR
	(NEW.node_upgrade_completed_at != OLD.node_upgrade_completed_at OR (NEW.node_upgrade_completed_at IS NOT NULL AND OLD.node_upgrade_completed_at IS NULL) OR (NEW.node_upgrade_completed_at IS NULL AND OLD.node_upgrade_completed_at IS NOT NULL))
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10011, OLD.upgrade_info_uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for UpgradeInfoControllerNode
CREATE TRIGGER trg_log_upgrade_info_controller_node_delete
AFTER DELETE ON upgrade_info_controller_node FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10011, OLD.upgrade_info_uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for ObjectStoreMetadataPath
INSERT INTO change_log_namespace VALUES (10012, 'object_store_metadata_path', 'ObjectStoreMetadataPath changes based on path');

-- insert trigger for ObjectStoreMetadataPath
CREATE TRIGGER trg_log_object_store_metadata_path_insert
AFTER INSERT ON object_store_metadata_path FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10012, NEW.path, DATETIME('now', 'utc'));
END;

-- update trigger for ObjectStoreMetadataPath
CREATE TRIGGER trg_log_object_store_metadata_path_update
AFTER UPDATE ON object_store_metadata_path FOR EACH ROW
WHEN 
	NEW.path != OLD.path OR
	NEW.metadata_uuid != OLD.metadata_uuid
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10012, OLD.path, DATETIME('now', 'utc'));
END;
-- delete trigger for ObjectStoreMetadataPath
CREATE TRIGGER trg_log_object_store_metadata_path_delete
AFTER DELETE ON object_store_metadata_path FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10012, OLD.path, DATETIME('now', 'utc'));
END;

-- insert namespace for ObjectStoreDrainInfo
INSERT INTO change_log_namespace VALUES (10013, 'object_store_drain_info', 'ObjectStoreDrainInfo changes based on uuid');

-- insert trigger for ObjectStoreDrainInfo
CREATE TRIGGER trg_log_object_store_drain_info_insert
AFTER INSERT ON object_store_drain_info FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10013, NEW.uuid, DATETIME('now', 'utc'));
END;

-- update trigger for ObjectStoreDrainInfo
CREATE TRIGGER trg_log_object_store_drain_info_update
AFTER UPDATE ON object_store_drain_info FOR EACH ROW
WHEN 
	NEW.uuid != OLD.uuid OR
	NEW.phase_type_id != OLD.phase_type_id OR
	(NEW.from_backend_uuid != OLD.from_backend_uuid OR (NEW.from_backend_uuid IS NOT NULL AND OLD.from_backend_uuid IS NULL) OR (NEW.from_backend_uuid IS NULL AND OLD.from_backend_uuid IS NOT NULL)) OR
	NEW.to_backend_uuid != OLD.to_backend_uuid
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10013, OLD.uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for ObjectStoreDrainInfo
CREATE TRIGGER trg_log_object_store_drain_info_delete
AFTER DELETE ON object_store_drain_info FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10013, OLD.uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for SecretBackendRotation
INSERT INTO change_log_namespace VALUES (10014, 'secret_backend_rotation', 'SecretBackendRotation changes based on backend_uuid');

-- insert trigger for SecretBackendRotation
CREATE TRIGGER trg_log_secret_backend_rotation_insert
AFTER INSERT ON secret_backend_rotation FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10014, NEW.backend_uuid, DATETIME('now', 'utc'));
END;

-- update trigger for SecretBackendRotation
CREATE TRIGGER trg_log_secret_backend_rotation_update
AFTER UPDATE ON secret_backend_rotation FOR EACH ROW
WHEN 
	NEW.backend_uuid != OLD.backend_uuid OR
	NEW.next_rotation_time != OLD.next_rotation_time
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10014, OLD.backend_uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for SecretBackendRotation
CREATE TRIGGER trg_log_secret_backend_rotation_delete
AFTER DELETE ON secret_backend_rotation FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10014, OLD.backend_uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for ModelSecretBackend
INSERT INTO change_log_namespace VALUES (10015, 'model_secret_backend', 'ModelSecretBackend changes based on model_uuid');

-- insert trigger for ModelSecretBackend
CREATE TRIGGER trg_log_model_secret_backend_insert
AFTER INSERT ON model_secret_backend FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10015, NEW.model_uuid, DATETIME('now', 'utc'));
END;

-- update trigger for ModelSecretBackend
CREATE TRIGGER trg_log_model_secret_backend_update
AFTER UPDATE ON model_secret_backend FOR EACH ROW
WHEN 
	NEW.model_uuid != OLD.model_uuid OR
	NEW.secret_backend_uuid != OLD.secret_backend_uuid
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10015, OLD.model_uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for ModelSecretBackend
CREATE TRIGGER trg_log_model_secret_backend_delete
AFTER DELETE ON model_secret_backend FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10015, OLD.model_uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for Model
INSERT INTO change_log_namespace VALUES (10016, 'model', 'Model changes based on uuid');

-- insert trigger for Model
CREATE TRIGGER trg_log_model_insert
AFTER INSERT ON model FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10016, NEW.uuid, DATETIME('now', 'utc'));
END;

-- update trigger for Model
CREATE TRIGGER trg_log_model_update
AFTER UPDATE ON model FOR EACH ROW
WHEN 
	NEW.uuid != OLD.uuid OR
	NEW.activated != OLD.activated OR
	NEW.cloud_uuid != OLD.cloud_uuid OR
	(NEW.cloud_region_uuid != OLD.cloud_region_uuid OR (NEW.cloud_region_uuid IS NOT NULL AND OLD.cloud_region_uuid IS NULL) OR (NEW.cloud_region_uuid IS NULL AND OLD.cloud_region_uuid IS NOT NULL)) OR
	(NEW.cloud_credential_uuid != OLD.cloud_credential_uuid OR (NEW.cloud_credential_uuid IS NOT NULL AND OLD.cloud_credential_uuid IS NULL) OR (NEW.cloud_credential_uuid IS NULL AND OLD.cloud_credential_uuid IS NOT NULL)) OR
	NEW.model_type_id != OLD.model_type_id OR
	NEW.life_id != OLD.life_id OR
	NEW.name != OLD.name OR
	NEW.qualifier != OLD.qualifier
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10016, OLD.uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for Model
CREATE TRIGGER trg_log_model_delete
AFTER DELETE ON model FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10016, OLD.uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for ModelAuthorizedKeys
INSERT INTO change_log_namespace VALUES (10017, 'model_authorized_keys', 'ModelAuthorizedKeys changes based on model_uuid');

-- insert trigger for ModelAuthorizedKeys
CREATE TRIGGER trg_log_model_authorized_keys_insert
AFTER INSERT ON model_authorized_keys FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10017, NEW.model_uuid, DATETIME('now', 'utc'));
END;

-- update trigger for ModelAuthorizedKeys
CREATE TRIGGER trg_log_model_authorized_keys_update
AFTER UPDATE ON model_authorized_keys FOR EACH ROW
WHEN 
	NEW.model_uuid != OLD.model_uuid OR
	NEW.user_public_ssh_key_id != OLD.user_public_ssh_key_id
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10017, OLD.model_uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for ModelAuthorizedKeys
CREATE TRIGGER trg_log_model_authorized_keys_delete
AFTER DELETE ON model_authorized_keys FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10017, OLD.model_uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for UserAuthentication
INSERT INTO change_log_namespace VALUES (10018, 'user_authentication', 'UserAuthentication changes based on user_uuid');

-- insert trigger for UserAuthentication
CREATE TRIGGER trg_log_user_authentication_insert
AFTER INSERT ON user_authentication FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10018, NEW.user_uuid, DATETIME('now', 'utc'));
END;

-- update trigger for UserAuthentication
CREATE TRIGGER trg_log_user_authentication_update
AFTER UPDATE ON user_authentication FOR EACH ROW
WHEN 
	NEW.user_uuid != OLD.user_uuid OR
	NEW.disabled != OLD.disabled
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10018, OLD.user_uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for UserAuthentication
CREATE TRIGGER trg_log_user_authentication_delete
AFTER DELETE ON user_authentication FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10018, OLD.user_uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for ObjectStoreBackend
INSERT INTO change_log_namespace VALUES (10019, 'object_store_backend', 'ObjectStoreBackend changes based on uuid');

-- insert trigger for ObjectStoreBackend
CREATE TRIGGER trg_log_object_store_backend_insert
AFTER INSERT ON object_store_backend FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10019, NEW.uuid, DATETIME('now', 'utc'));
END;

-- update trigger for ObjectStoreBackend
CREATE TRIGGER trg_log_object_store_backend_update
AFTER UPDATE ON object_store_backend FOR EACH ROW
WHEN 
	NEW.uuid != OLD.uuid OR
	NEW.life_id != OLD.life_id OR
	NEW.type_id != OLD.type_id OR
	NEW.updated_at != OLD.updated_at
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10019, OLD.uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for ObjectStoreBackend
CREATE TRIGGER trg_log_object_store_backend_delete
AFTER DELETE ON object_store_backend FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10019, OLD.uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for LoggingLokiConfig
INSERT INTO change_log_namespace VALUES (10020, 'logging_loki_config', 'LoggingLokiConfig changes based on uuid');

-- insert trigger for LoggingLokiConfig
CREATE TRIGGER trg_log_logging_loki_config_insert
AFTER INSERT ON logging_loki_config FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10020, NEW.uuid, DATETIME('now', 'utc'));
END;

-- update trigger for LoggingLokiConfig
CREATE TRIGGER trg_log_logging_loki_config_update
AFTER UPDATE ON logging_loki_config FOR EACH ROW
WHEN 
	NEW.uuid != OLD.uuid OR
	NEW.endpoint != OLD.endpoint OR
	NEW.ca_cert != OLD.ca_cert OR
	(NEW.insecure_skip_verify != OLD.insecure_skip_verify OR (NEW.insecure_skip_verify IS NOT NULL AND OLD.insecure_skip_verify IS NULL) OR (NEW.insecure_skip_verify IS NULL AND OLD.insecure_skip_verify IS NOT NULL)) OR
	NEW.org_id != OLD.org_id
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10020, OLD.uuid, DATETIME('now', 'utc'));
END;
-- delete trigger for LoggingLokiConfig
CREATE TRIGGER trg_log_logging_loki_config_delete
AFTER DELETE ON logging_loki_config FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10020, OLD.uuid, DATETIME('now', 'utc'));
END;

-- insert namespace for WorkloadTracingConfig
INSERT INTO change_log_namespace VALUES (10022, 'workload_tracing_config', 'WorkloadTracingConfig changes based on key');

-- insert trigger for WorkloadTracingConfig
CREATE TRIGGER trg_log_workload_tracing_config_insert
AFTER INSERT ON workload_tracing_config FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10022, NEW.key, DATETIME('now', 'utc'));
END;

-- update trigger for WorkloadTracingConfig
CREATE TRIGGER trg_log_workload_tracing_config_update
AFTER UPDATE ON workload_tracing_config FOR EACH ROW
WHEN 
	NEW.key != OLD.key OR
	NEW.value != OLD.value
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10022, OLD.key, DATETIME('now', 'utc'));
END;
-- delete trigger for WorkloadTracingConfig
CREATE TRIGGER trg_log_workload_tracing_config_delete
AFTER DELETE ON workload_tracing_config FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10022, OLD.key, DATETIME('now', 'utc'));
END;

-- insert namespace for ModelDatabaseDeletion
INSERT INTO change_log_namespace VALUES (10023, 'model_database_deletion', 'ModelDatabaseDeletion changes based on namespace');

-- insert trigger for ModelDatabaseDeletion
CREATE TRIGGER trg_log_model_database_deletion_insert
AFTER INSERT ON model_database_deletion FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10023, NEW.namespace, DATETIME('now', 'utc'));
END;

-- update trigger for ModelDatabaseDeletion
CREATE TRIGGER trg_log_model_database_deletion_update
AFTER UPDATE ON model_database_deletion FOR EACH ROW
WHEN 
	NEW.namespace != OLD.namespace OR
	NEW.created_at != OLD.created_at
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10023, OLD.namespace, DATETIME('now', 'utc'));
END;
-- delete trigger for ModelDatabaseDeletion
CREATE TRIGGER trg_log_model_database_deletion_delete
AFTER DELETE ON model_database_deletion FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10023, OLD.namespace, DATETIME('now', 'utc'));
END;

-- insert namespace for ControllerSshServerPort
INSERT INTO change_log_namespace VALUES (10028, 'controller_ssh_server_port', 'ControllerSshServerPort changes based on port');

-- insert trigger for ControllerSshServerPort
CREATE TRIGGER trg_log_controller_ssh_server_port_insert
AFTER INSERT ON controller_ssh_server_port FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (1, 10028, NEW.port, DATETIME('now', 'utc'));
END;

-- update trigger for ControllerSshServerPort
CREATE TRIGGER trg_log_controller_ssh_server_port_update
AFTER UPDATE ON controller_ssh_server_port FOR EACH ROW
WHEN 
	NEW.port != OLD.port
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (2, 10028, OLD.port, DATETIME('now', 'utc'));
END;
-- delete trigger for ControllerSshServerPort
CREATE TRIGGER trg_log_controller_ssh_server_port_delete
AFTER DELETE ON controller_ssh_server_port FOR EACH ROW
BEGIN
    INSERT INTO change_log (edit_type_id, namespace_id, changed, created_at)
    VALUES (4, 10028, OLD.port, DATETIME('now', 'utc'));
END;
CREATE TRIGGER trg_secret_backend_immutable_update
    BEFORE UPDATE ON secret_backend
    FOR EACH ROW
    WHEN OLD.origin_id = 0
    BEGIN
        SELECT RAISE(FAIL, 'built-in secret backends are immutable');
    END;

CREATE TRIGGER trg_secret_backend_immutable_delete
    BEFORE DELETE ON secret_backend
    FOR EACH ROW
    WHEN OLD.origin_id = 0
    BEGIN
        SELECT RAISE(FAIL, 'built-in secret backends are immutable');
    END;