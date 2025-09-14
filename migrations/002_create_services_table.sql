-- Migration 002: Create services table
CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES masters(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price TEXT NOT NULL,
    duration INTERVAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_services_master_id ON services(master_id);

-- Comments
COMMENT ON TABLE services IS 'Таблица услуг мастеров';
COMMENT ON COLUMN services.master_id IS 'ID мастера';
COMMENT ON COLUMN services.name IS 'Название услуги';
COMMENT ON COLUMN services.description IS 'Описание услуги';
COMMENT ON COLUMN services.price IS 'Цена услуги';
COMMENT ON COLUMN services.duration IS 'Продолжительность услуги';