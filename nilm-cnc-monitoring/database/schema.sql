-- Run inside the "nilm" database:  psql -U postgres -d nilm -f schema.sql
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS machine_data (
    time       TIMESTAMPTZ NOT NULL,
    device_id  TEXT,
    main1      REAL,
    main2      REAL,
    spindle    REAL,
    coolant    REAL,
    hydraulic  REAL,
    aaxis      REAL
);

SELECT create_hypertable('machine_data', 'time', if_not_exists => TRUE);

-- If you already had the table without main1/main2:
-- ALTER TABLE machine_data ADD COLUMN IF NOT EXISTS main1 REAL;
-- ALTER TABLE machine_data ADD COLUMN IF NOT EXISTS main2 REAL;
