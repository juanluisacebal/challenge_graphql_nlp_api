from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional
import os
from dotenv import load_dotenv
import ssl
import certifi

load_dotenv()

# Configuración de Keycloak
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")
KEYCLOAK_ALGORITHMS = ["RS256"]

# Configuración de SSL
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Configuración de OAuth2
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Verifica y decodifica el token JWT.
    
    Args:
        token: Token JWT
    
    Returns:
        dict: Información del usuario
    
    Raises:
        HTTPException: Si el token es inválido
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Obtener la clave pública de Keycloak
        from keycloak import KeycloakOpenID
        keycloak_openid = KeycloakOpenID(
            server_url=KEYCLOAK_URL,
            client_id=KEYCLOAK_CLIENT_ID,
            realm_name=KEYCLOAK_REALM,
            client_secret_key=KEYCLOAK_CLIENT_SECRET,
            verify=True,
            custom_headers={"User-Agent": "challenge-api"}
        )
        
        # Verificar el token
        token_info = keycloak_openid.decode_token(
            token,
            keycloak_openid.public_key()
        )

        if token_info.get("aud") != "account" or token_info.get("azp") != KEYCLOAK_CLIENT_ID:
            raise HTTPException(
                status_code=401,
                detail="Audiencia o parte autorizada inválida en el token"
            )

        if token_info is None:
            raise credentials_exception

        return token_info
    except JWTError:
        raise credentials_exception
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 