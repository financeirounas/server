import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from fastapi import HTTPException
from dotenv import load_dotenv
from jose import jwt, JWTError

load_dotenv()


class JWTService:
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-default-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  * 7

    @staticmethod
    async def generate_jwt_token(
        user_id: str
    ) -> str:
        """
        Gera um JWT assinado contendo o user_id em "sub" + claims extras.
        """
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=JWTService.ACCESS_TOKEN_EXPIRE_MINUTES)

        payload: Dict[str, Any] = {
            "sub": user_id,   
            "iat": int(now.timestamp()), 
            "exp": int(expire.timestamp()) 
        }
        
        token = jwt.encode(payload, JWTService.SECRET_KEY, algorithm=JWTService.ALGORITHM)
        
        return token

    @staticmethod
    async def validate_token(token: str) -> Dict[str, Any]:
        """
        Valida o token:
        - assinatura
        - expiração

        Retorna o payload se for válido.
        Levanta JWTError se for inválido/expirado.
        """
        try:
            payload = jwt.decode(
                token,
                JWTService.SECRET_KEY,
                algorithms=[JWTService.ALGORITHM],
                options={"verify_aud": False}, 
            )
            return payload
        except JWTError as e:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado") from e

    @staticmethod
    async def get_user_id_from_token(token: str) -> Optional[str]:
        """
        Extrai o user_id (sub) do token já validando assinatura/expiração.
        Retorna None se inválido.
        """
        try:
            payload = await JWTService.validate_token(token)
            user_id = payload.get("sub")
            if not isinstance(user_id, str):
                return None
            return user_id
        except JWTError:
            return None

    @staticmethod
    async def get_claim_from_token(token: str, claim: str) -> Any:
        """
        Retorna um claim específico do token (ex.: 'role', 'email'),
        ou None se não existir ou token for inválido.
        """
        try:
            payload = await JWTService.validate_token(token)
            return payload.get(claim)
        except JWTError:
            return None
