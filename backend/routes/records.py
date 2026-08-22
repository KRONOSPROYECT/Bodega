from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
import os
from ..database import get_db
from ..crypto import sha256, sign_data, load_private_key, get_crypto_version
from ..models import RecordCreate, RecordResponse, VerifyResponse

router = APIRouter(prefix="/api/records", tags=["records"])

# Cargar clave privada (desde env)
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if not PRIVATE_KEY:
    raise ValueError("PRIVATE_KEY no configurada en .env")

priv_key = load_private_key(PRIVATE_KEY)

@router.post("/", response_model=RecordResponse)
async def create_record(data: RecordCreate, db=Depends(get_db)):
    # 1. Obtener último hash (encadenamiento)
    last_hash_resp = db.rpc("get_last_hash").execute()
    hash_anterior = last_hash_resp.data if last_hash_resp.data else "GENESIS"

    # 2. Generar folio y timestamp
    folio_resp = db.rpc("generate_folio").execute()
    folio = folio_resp.data
    timestamp = datetime.now(timezone.utc)

    # 3. Calcular hash_actual
    raw_content = f"{folio}|{data.empresa}|{data.tipo}|{timestamp.isoformat()}|{hash_anterior}"
    hash_actual = sha256(raw_content)

    # 4. Firmar digitalmente el hash
    firma = sign_data(priv_key, hash_actual.encode())

    # 5. Insertar en la base de datos
    record_data = {
        "folio": folio,
        "empresa": data.empresa,
        "tipo": data.tipo,
        "timestamp": timestamp.isoformat(),
        "hash_anterior": hash_anterior,
        "hash_actual": hash_actual,
        "algoritmo": "SHA-256",
        "nivel": get_crypto_version(),
        "firma_digital": firma,
        "metadata": data.metadata
    }

    result = db.table("records").insert(record_data).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Error al crear el registro")

    return RecordResponse(**result.data[0])

@router.get("/{folio}", response_model=VerifyResponse)
async def verify_record(folio: str, db=Depends(get_db)):
    # 1. Buscar el registro
    result = db.table("records").select("*").eq("folio", folio).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    record = result.data[0]

    # 2. Recalcular hash_actual
    raw_content = f"{record['folio']}|{record['empresa']}|{record['tipo']}|{record['timestamp']}|{record['hash_anterior']}"
    hash_calculado = sha256(raw_content)

    integridad_valida = hash_calculado == record["hash_actual"]

    # 3. Verificar firma (opcional, pero recomendado)
    #   Aquí se cargaría la clave pública y se verificaría la firma

    return VerifyResponse(
        folio=record["folio"],
        estado=record["estado"],
        integridad_valida=integridad_valida,
        timestamp=record["timestamp"],
        hash_actual=record["hash_actual"],
        mensaje="Registro auténtico" if integridad_valida else "Alerta: integridad no confirmada"
    )

@router.post("/{folio}/revoke")
async def revoke_record(folio: str, db=Depends(get_db)):
    # 1. Verificar que existe y no está ya revocado
    result = db.table("records").select("*").eq("folio", folio).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    record = result.data[0]
    if record["estado"] == "REVOCADO":
        raise HTTPException(status_code=400, detail="El registro ya está revocado")

    # 2. Actualizar estado
    update_data = {
        "estado": "REVOCADO",
        "revoked_at": datetime.now(timezone.utc).isoformat()
    }
    result = db.table("records").update(update_data).eq("folio", folio).execute()
    return {"mensaje": f"Registro {folio} revocado correctamente"}

@router.get("/", response_model=list[RecordResponse])
async def list_records(limit: int = 10, db=Depends(get_db)):
    result = db.table("records").select("*").order("timestamp", desc=True).limit(limit).execute()
    return result.data
