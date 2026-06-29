import jwt
from .models import User, BlacklistedToken
from .auth import decode_token


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.jwt_user = None

        if not request.path.startswith("/admin/"):
            auth_header = request.headers.get("Authorization")

            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

                if not BlacklistedToken.objects.filter(token=token).exists():
                    try:
                        payload = decode_token(token)
                        user = User.objects.get(id=payload["user_id"], is_active=True)
                        request.jwt_user = user
                    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
                        request.jwt_user = None

        response = self.get_response(request)
        return response