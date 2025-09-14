-- Migration 001: Create masters table
CREATE TABLE IF NOT EXISTS masters (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    photo_url TEXT,
    description TEXT,
    experience_years INTEGER CHECK (experience_years >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_masters_specialization ON masters(specialization);
CREATE INDEX IF NOT EXISTS idx_masters_phone ON masters(phone_number);

-- Comments
COMMENT ON TABLE masters IS 'Таблица мастеров';
COMMENT ON COLUMN masters.first_name IS 'Имя мастера';
COMMENT ON COLUMN masters.last_name IS 'Фамилия мастера';
COMMENT ON COLUMN masters.phone_number IS 'Номер телефона';
COMMENT ON COLUMN masters.specialization IS 'Специализация';
COMMENT ON COLUMN masters.photo_url IS 'URL фотографии';
COMMENT ON COLUMN masters.description IS 'Описание мастера';
COMMENT ON COLUMN masters.experience_years IS 'Стаж в годах';