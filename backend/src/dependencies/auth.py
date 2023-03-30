from typing import Any, Awaitable, Union, Optional
from jose import jwt
from strawberry.permission import BasePermission
from strawberry.types import Info
from strawberry.fastapi import GraphQLRouter
from strawberry.fastapi.handlers import GraphQLWSHandler
from strawberry.subscriptions.protocols.graphql_ws.types import OperationMessage

from src.env import env
from src.schemas.user import get_user_by_username


class IsAuthenticated(BasePermission):
    message = "Пользователь не авторизован"

    def has_permission(
        self,
        source,
        info: Info,
    ):
        token: str = info.context.get("Authorization")
        if not token:
            return False

        try:
            payload = jwt.decode(token, env["JWT_SECRET"])
            user = get_user_by_username(payload["username"])
            info.context["user"] = user
            return True
        except:
            return False


class AuthGraphQLWSHandler(GraphQLWSHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token: Optional[str] = None

    async def handle_connection_init(self, message: OperationMessage):
        connection_params = message["payload"]
        self.token = connection_params.get("Authorization")
        await super().handle_connection_init(message)

    async def get_context(self):
        context = await super().get_context()
        context["Authorization"] = self.token
        return context


class AuthGraphQLRouter(GraphQLRouter):
    graphql_ws_handler_class = AuthGraphQLWSHandler
