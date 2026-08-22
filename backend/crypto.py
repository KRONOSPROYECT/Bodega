import hashlib
import hmac
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

# ─── SHA-256 ──────────────────────────────────────────────────────
def sha256(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

# ─── Ed25519 (demo, reemplazar por ML-DSA en producción) ──────
def load_private_key(pem: str) -> ed25519.Ed25519PrivateKey:
    return serialization.load_pem_private_key(pem.encode(), password=None)

def load_public_key(pem: str) -> ed25519.Ed25519PublicKey:
    return serialization.load_pem_public_key(pem.encode())

def sign_data(private_key: ed25519.Ed25519PrivateKey, data: bytes) -> str:
    return private_key.sign(data).hex()

def verify_signature(public_key: ed25519.Ed25519PublicKey, data: bytes, signature_hex: str) -> bool:
    try:
        public_key.verify(bytes.fromhex(signature_hex), data)
        return True
    except InvalidSignature:
        return False

# ─── Preparación poscuántica (campo de versión) ──────────────
def get_crypto_version() -> str:
    return "QUANTUM-READY-V1"
