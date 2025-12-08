from fastapi import HTTPException
from passlib.context import CryptContext
from entities.models.user import User
from repositories.user_repository import UserRepository
from lib.supabase_client import supabase


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def register_user(email: str, password: str, username: str, role: str) -> User | None:

        existing_user_record = await UserRepository.get_user("email", email)
        if existing_user_record:
            raise HTTPException(status_code=400, detail="User with this email already exists.")

        hashed_password = UserService.hash_password(password)

        created_user_record = await UserRepository.create_user(
            email=email,
            hashed_password=hashed_password,
            username=username,
            role=role
        )
        return created_user_record

    @staticmethod
    async def authenticate_user(email: str, password: str) -> User | None:
        """Autentica usuário por email e senha; retorna User se válido, senão None."""
        user_record = await UserRepository.get_user("email", email)
        if not user_record:
            return None

        if not UserService.verify_password(password, user_record.password):
            return None

        return user_record

    @staticmethod
    async def get_user_by_id(user_id: str) -> User | None:
        """Retorna usuário pelo ID."""
        return await UserRepository.get_user("id", user_id)

    @staticmethod
    async def list_users(role: str | None = None) -> list[User]:
        """Lista usuários com filtros opcionais `role`.

        Usa diretamente o cliente Supabase para permitir listagem completa.
        """
        query = supabase.table("users").select("*")
        if role is not None:
            query = query.eq("role", role)


        response = query.execute()
        if not response.data:
            return []

        users = []
        for item in response.data:
            try:
                users.append(User(**item))
            except Exception:
                # Ignora registros que não batem com o modelo User
                continue

        return users

    @staticmethod
    async def update_user(user_id: str, username: str | None = None, role: str | None = None) -> User | None:
        """Atualiza campos permitidos do usuário e retorna o registro atualizado."""
        payload: dict = {}
        if username is not None:
            payload["username"] = username
        if role is not None:
            payload["role"] = role

        if not payload:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")

        response = (
            supabase.table(UserRepository.TABLE_NAME)
            .update(payload)
            .eq("id", user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=500, detail="Erro ao atualizar usuário no Supabase")

        try:
            return User(**response.data[0])
        except Exception:
            return None
