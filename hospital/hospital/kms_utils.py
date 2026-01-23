import base64
import os
from pathlib import Path
from google.cloud import kms

# Configuración de credenciales
# Usamos Path para obtener la ruta absoluta del archivo JSON, independiente de dónde se ejecute el script.
BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_PATH = BASE_DIR / "credenciales_gcp.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(CREDENTIALS_PATH)

# Configuración de KMS
# VERIFICAR: Confirma si 'my-first-project' es el ID correcto de tu proyecto en la consola de GCP.
PROJECT_ID = "dependable-data-449218-p9" 
LOCATION_ID = "global"
KEY_RING_ID = "keys-hospital"
CRYPTO_KEY_ID = "key-comunication-apps"

def _get_kms_client_and_key_name():
    """
    Helper interno para obtener el cliente y la ruta de la clave.
    """
    client = kms.KeyManagementServiceClient()
    # Construye el resource name: projects/{id}/locations/{loc}/keyRings/{ring}/cryptoKeys/{key}
    key_name = client.crypto_key_path(PROJECT_ID, LOCATION_ID, KEY_RING_ID, CRYPTO_KEY_ID)
    return client, key_name

def encriptar(texto: str) -> str:
    """
    Toma un texto plano, lo encripta con Google Cloud KMS y retorna el resultado en Base64.
    
    Args:
        texto (str): El texto a encriptar.
        
    Returns:
        str: El texto encriptado codificado en Base64.
    """
    # Validación básica
    if not texto:
        return ""

    try:
        client, key_name = _get_kms_client_and_key_name()

        # 1. Convertir string a bytes (UTF-8)
        plaintext_bytes = texto.encode("utf-8")

        # 2. Encriptar con KMS
        # Nota: encrypt retorna un objeto con el campo 'ciphertext'
        response = client.encrypt(
            request={
                "name": key_name,
                "plaintext": plaintext_bytes
            }
        )
        ciphertext = response.ciphertext

        # 3. Convertir bytes encriptados a Base64 (string) para transporte/JSON
        encrypted_b64 = base64.b64encode(ciphertext).decode("utf-8")
        
        return encrypted_b64

    except Exception as e:
        # En un entorno real, logging.error(e) sería recomendable
        print(f"Error en encriptar: {e}")
        raise e

def desencriptar(texto_base64: str) -> str:
    """
    Toma un string en Base64 (previamente encriptado), lo desencripta con Google Cloud KMS 
    y retorna el texto plano original.
    
    Args:
        texto_base64 (str): El ciphertext en formato Base64.
        
    Returns:
        str: El texto plano desencriptado.
    """
    if not texto_base64:
        return ""

    try:
        client, key_name = _get_kms_client_and_key_name()

        # 1. Decodificar Base64 a bytes
        ciphertext_bytes = base64.b64decode(texto_base64)

        # 2. Desencriptar con KMS
        response = client.decrypt(
            request={
                "name": key_name,
                "ciphertext": ciphertext_bytes
            }
        )
        plaintext_bytes = response.plaintext

        # 3. Convertir bytes a string (UTF-8)
        plaintext = plaintext_bytes.decode("utf-8")
        
        return plaintext

    except Exception as e:
        print(f"Error en desencriptar: {e}")
        raise e

# --- BLOQUE DE PRUEBA (Borrar después) ---
if __name__ == "__main__":
    try:
        texto = "Prueba de conexión GCP"
        print(f"Encriptando: {texto}")
        cifrado = encriptar(texto)
        print(f"Cifrado: {cifrado}")
        descifrado = desencriptar(cifrado)
        print(f"Descifrado: {descifrado}")
        print("✅ ¡ÉXITO TOTAL!")
    except Exception as e:
        print("❌ Algo falló. Revisa el ID del proyecto o la ruta del JSON.")