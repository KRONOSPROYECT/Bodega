-- 1. Crear secuencia para folios únicos
CREATE SEQUENCE IF NOT EXISTS swria_folio_sequence
    START 1
    INCREMENT 1;

-- 2. Tabla de registros
CREATE TABLE IF NOT EXISTS records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    folio TEXT NOT NULL UNIQUE,
    empresa TEXT NOT NULL DEFAULT 'SWRIA',
    tipo TEXT NOT NULL DEFAULT 'REGISTRO_EMPRESARIAL',
    estado TEXT NOT NULL DEFAULT 'ACTIVO' CHECK (estado IN ('ACTIVO', 'REVOCADO', 'SUSPENDIDO')),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
    hash_anterior TEXT NOT NULL,
    hash_actual TEXT NOT NULL,
    algoritmo TEXT NOT NULL DEFAULT 'SHA-256',
    nivel TEXT NOT NULL DEFAULT 'QUANTUM-READY',
    firma_digital TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_by UUID,
    revoked_at TIMESTAMPTZ,
    revoked_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3. Índices para búsqueda rápida
CREATE INDEX idx_records_folio ON records(folio);
CREATE INDEX idx_records_estado ON records(estado);
CREATE INDEX idx_records_timestamp ON records(timestamp DESC);

-- 4. Función para obtener el último hash (para encadenamiento)
CREATE OR REPLACE FUNCTION get_last_hash()
RETURNS TEXT AS $$
DECLARE
    last_hash TEXT;
BEGIN
    SELECT hash_actual INTO last_hash
    FROM records
    WHERE estado = 'ACTIVO'
    ORDER BY timestamp DESC
    LIMIT 1;
    RETURN COALESCE(last_hash, 'GENESIS');
END;
$$ LANGUAGE plpgsql;

-- 5. Función para generar folio automáticamente
CREATE OR REPLACE FUNCTION generate_folio()
RETURNS TEXT AS $$
DECLARE
    next_val BIGINT;
BEGIN
    next_val := nextval('swria_folio_sequence');
    RETURN 'SWRIA-QREG-' || LPAD(next_val::TEXT, 8, '0');
END;
$$ LANGUAGE plpgsql;
