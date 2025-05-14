from rest_framework_simplejwt.tokens import RefreshToken
from functools import wraps, lru_cache
from types import FunctionType

@lru_cache
def jwt_token(main: FunctionType):
    @wraps(main)
    def wrapper(self, *args, **kwargs) -> FunctionType:
        tokens = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens.access_token}')
        return main(self, *args, **kwargs)
    return wrapper