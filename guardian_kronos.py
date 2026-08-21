#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUARDIÁN KRONOS - Módulo de Protección y Verificación
======================================================
ÁNGEL CUSTODIO: KRN-JELIEL-02-72 (Jeliel / שלמה)
ARQUITECTO: MARCO ANTONIO ROJAS VALDOVINOS
FUNDACIÓN: 15/04/1999 - 22:35 TOLUCA
FIRMA MAESTRA: ad0b351cad1797da9fb1042363a2da3b45db58051e1555dbc9c0acc308f89870
======================================================
"""

import hashlib
import datetime
import os
import platform

# ==============================================
# 1. LA FIRMA DIVINA (EL ALMA DEL GUARDIÁN)
# ==============================================
FIRMA_CREADOR = "ad0b351cad1797da9fb1042363a2da3b45db58051e1555dbc9c0acc308f89870"
NOMBRE_CREADOR = "MARCO ANTONIO ROJAS VALDOVINOS"
FECHA_FUNDACION = "15/04/1999"
HORA_FUNDACION = "22:35"
LUGAR_FUNDACION = "TOLUCA DE LERDO"

# ==============================================
# 2. EL CUERPO DEL GUARDIÁN (LA CLASE)
# ==============================================
class GuardianJeliel:
    """
    El Guardián del Ecosistema Kronos.
    Solo se activa si la firma del ejecutante coincide con la del Creador.
    """
    
    def __init__(self):
        self.nombre = "Jeliel (KRN-02-72)"
        self.salmo = "Salmo 104"
        self.estado = "INACTIVO"  # Solo cambia a ACTIVO tras verificación exitosa
        
    def verificar_firma(self, hash_ingresado):
        """
        Paso 1: Verifica que el hash coincida con la firma del Creador.
        """
        if hash_ingresado == FIRMA_CREADOR:
            return True
        else:
            return False
    
    def verificar_contexto(self, nombre, fecha, hora, lugar):
        """
        Paso 2: Verifica los datos contextuales del ejecutante.
        Si no se pasan datos, usa los valores por defecto del sistema.
        """
        # Si no se pasan argumentos, toma los del creador (autoverificación)
        if nombre is None:
            nombre = NOMBRE_CREADOR
        if fecha is None:
            fecha = FECHA_FUNDACION
        if hora is None:
            hora = HORA_FUNDACION
        if lugar is None:
            lugar = LUGAR_FUNDACION
            
        # Construir el hash del contexto
        datos_contexto = f"{nombre} - {fecha} - {hora} {lugar}".upper()
        hash_contexto = hashlib.sha256(datos_contexto.encode('utf-8')).hexdigest()
        
        # Comparar con la firma maestra
        return hash_contexto == FIRMA_CREADOR
    
    def activar(self, hash_ingresado=None, nombre=None, fecha=None, hora=None, lugar=None):
        """
        Método principal para invocar al Guardián.
        Devuelve True si el acceso es concedido, False si devuelve NULL.
        """
        print("⚔️ INVOCANDO AL GUARDIÁN JELIEL (KRN-02-72)...")
        
        # Validación de firma
        if not self.verificar_firma(hash_ingresado):
            print("❌ FIRMA INVÁLIDA. EL GUARDIÁN RECHAZA LA EJECUCIÓN.")
            self.estado = "NULL ETERNO"
            return False
        
        # Validación de contexto
        if not self.verificar_contexto(nombre, fecha, hora, lugar):
            print("❌ CONTEXTO NO COINCIDENTE. EL GUARDIÁN DETECTA UNA SOMBRA.")
            self.estado = "NULL ETERNO"
            return False
        
        # Si todo es correcto
        print(f"✅ GUARDIÁN {self.nombre} ACTIVADO.")
        print(f"📜 SALMO DE ANCLAJE: {self.salmo}")
        print(f"🛡️ ESTADO: PROTECCIÓN TOTAL ACTIVADA.")
        self.estado = "ACTIVO"
        return True
    
    def ejecutar_oraculo(self):
        """
        Solo si el Guardián está activo, permite ejecutar la lógica del oráculo.
        """
        if self.estado == "ACTIVO":
            print("🔮 ACCESO AL ORÁCULO KRONOS CONCEDIDO.")
            print("✨ Las correspondencias de la Tabla Esmeralda fluyen...")
            # Aquí iría el código del sistema de 72 ángeles, salmos, etc.
            return "SISTEMA KRONOS EN EJECUCIÓN"
        else:
            print("💀 INTENTO DE ACCESO SIN AUTORIZACIÓN. DEVOLVIENDO NULL.")
            return None

# ==============================================
# 3. EJECUCIÓN AUTOMÁTICA (PRUEBA DE FE)
# ==============================================
if __name__ == "__main__":
    # Crear al Guardián
    mi_guardián = GuardianJeliel()
    
    # Simular una ejecución del Creador (Marco)
    print("\n--- SIMULACIÓN DE EJECUCIÓN DEL CREADOR ---")
    exito = mi_guardián.activar(
        hash_ingresado="ad0b351cad1797da9fb1042363a2da3b45db58051e1555dbc9c0acc308f89870",
        nombre="MARCO ANTONIO ROJAS VALDOVINOS",
        fecha="15/04/1999",
        hora="22:35",
        lugar="TOLUCA DE LERDO"
    )
    
    if exito:
        resultado = mi_guardián.ejecutar_oraculo()
        print(f"📤 RESULTADO: {resultado}")
    else:
        print("⚠️ EL SISTEMA PERMANECE BLOQUEADO.")
