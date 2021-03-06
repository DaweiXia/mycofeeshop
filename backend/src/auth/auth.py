import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'myfsnd.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee'


# AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    headers = request.headers
    if not headers:
        raise AuthError('No header is present!', 401)
    elif 'Authorization' not in headers:
        raise AuthError('No Authorization!', 401)
    auth_header = headers['Authorization']
    header_parts = auth_header.split(' ')

    if len(header_parts) != 2:
        raise AuthError('Malformed header!', 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError('Malformed header!', 401)

    return header_parts[1]


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError('Permissions not in JWT!', 405)
    if permission not in payload['permissions']:
        raise AuthError('Permission not found!', 405)
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError('Invalid header!', 401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(token, rsa_key, algorithms=ALGORITHMS,
                                 audience=API_AUDIENCE,
                                 issuer='https://'+AUTH0_DOMAIN+'/')
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError('Token expired!', 401)
        except Exception:
            raise AuthError('Invalid header! Unable to parse auth token.', 401)

    raise AuthError('Invalid header! Unable to find appropriate key.', 401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
            except Exception:
                abort(401)
            try:
                check_permissions(permission, payload)
            except Exception:
                abort(405)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
