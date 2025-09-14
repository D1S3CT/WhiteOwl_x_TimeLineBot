-- Migration 003: Create working schedules table
CREATE TABLE IF NOT EXISTS working_schedules (
    id SERIAL PRIMARY KEY,
    master_id INTEGER REFERENCES masters(id) ON DELETE CASCADE,
    day_of_week INTEGER CHECK (day_of_week >= 1 AND day_of_week <= 7),
    is_working BOOLEAN DEFAULT TRUE,
    start_time TIME,
    end_time TIME,
    break_start_time TIME,
    break_end_time TIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_schedules_master_id ON working_schedules(master_id);
CREATE INDEX IF NOT EXISTS idx_schedules_day ON working_schedules(day_of_week);

-- Comments
COMMENT ON TABLE working_schedules IS 'График работы мастеров';
COMMENT ON COLUMN working_schedules.day_of_week IS 'День недели (1=Пн, 7=Вс)';
COMMENT ON COLUMN working_schedules.is_working IS 'Рабочий день или выходной';
COMMENT ON COLUMN working_schedules.start_time IS 'Начало рабочего дня';
COMMENT ON COLUMN working_schedules.end_time IS 'Конец рабочего дня';
COMMENT ON COLUMN working_schedules.break_start_time IS 'Начало перерыва';
COMMENT ON COLUMN working_schedules.break_end_time IS 'Конец перерыва';