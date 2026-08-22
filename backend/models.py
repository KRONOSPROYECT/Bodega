from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RecordCreate(BaseModel):
    tipo: str = "REGISTRO_EMPRESARIAL"
    empresa: str = "SWRIA"
    metadata: Optional[dict] = {}

class RecordResponse(BaseModel):
    id: str
    folio: str
    empresa: str
    tipo: str
    estado: str
    timestamp: datetime
    hash_anterior: str
    hash_actual: str
    algoritmo: str
    nivel: str
    firma_digital: Optional[str]
    metadata: dict
    created_at: datetime
    revoked_at: Optional[datetime]

class VerifyResponse(BaseModel):
    folio: str
    estado: str
    integridad_valida: bool
    timestamp: datetime
    hash_actual: str
    mensaje: str
