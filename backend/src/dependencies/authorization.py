from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from backend.src.env import env
from backend.src.schemas.user import find_user_by_username



class Authorization(HTTPBearer):
    def __init__(self):
        super(Authorization, self).__init__(auto_error=True)
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(Authorization, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Неавторизован")
        try:
            payload = jwt.decode(credentials.credentials, env['JWT_SECRET'])
            user = find_user_by_username(payload['username'])
            return user
        except:
            raise HTTPException(status_code=403, detail='JWT ошибка верификации')


