import jwt
from django.conf import settings


def decode_jwt_token(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token:
        jwt_token = request.headers['Authorization'].split()[-1]
        return jwt.decode(jwt_token, settings.SECRET_KEY, 'HS256')['username']
    return None
