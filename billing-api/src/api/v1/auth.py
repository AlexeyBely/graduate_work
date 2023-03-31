from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from core.config import settings
from models.auth import TokenData


http_scheme = HTTPBearer()
router = APIRouter()


async def authenticate(
    credentials: HTTPAuthorizationCredentials = Depends(http_scheme)
) -> TokenData:
    try:
        Jwt_token = credentials.credentials.encode('UTF-8')
        payload = jwt.decode(
            Jwt_token,
            settings.access_token_secret_key,
            algorithms=[settings.token_algoritm],
        )
        token_data = TokenData(**payload)
    except JWTError as e:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={'Authorization': 'Bearer'},
        )
        raise credentials_exception
    return token_data
