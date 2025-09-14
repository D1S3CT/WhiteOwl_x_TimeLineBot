-- Migration 004: Create time slots table
CREATE TABLE IF NOT EXISTS time_slots (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES masters(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    booking_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_slots_master_id ON time_slots(master_id);
CREATE INDEX IF NOT EXISTS idx_slots_date ON time_slots(date);
CREATE INDEX IF NOT EXISTS idx_slots_available ON time_slots(is_available);

-- Comments
COMMENT ON TABLE time_slots IS 'Временные слоты для записи';
COMMENT ON COLUMN time_slots.date IS 'Дата слота';
COMMENT ON COLUMN time_slots.start_time IS 'Время начала';
COMMENT ON COLUMN time_slots.end_time IS 'Время окончания';
COMMENT ON COLUMN time_slots.is_available IS 'Доступность для записи';
COMMENT ON COLUMN time_slots.booking_id IS 'ID бронирования';