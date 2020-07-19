from flask import jsonify
import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from app.main.models import User
from app.main import db

AUTH0_DOMAIN = 'balazsszalai.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'https://medical-measurement'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def convert_auth0_id_to_api_id(auth0_user_id):
    user = User.query.filter(User.auth0_id == auth0_user_id).first()
    if user is None:
        new_user = User()
        new_user.auth0_id = auth0_user_id
        db.session.add(new_user)
        db.session.commit()
        user_id = new_user.id
    else:
        user_id = user.id
    return user_id


def get_user_id():
    token = get_token_auth_header()
    payload = verify_decode_jwt(token)
    if 'sub' not in payload:
        raise AuthError({
            'code': 'no userID',
            'description': 'UserID not included in JWT.'
        }, 401)
    return convert_auth0_id_to_api_id(payload['sub'])


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'missing_header',
            'description': 'Authorization not found in headers.'
        }, 401)
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')
    if len(header_parts) != 2:
        raise AuthError({
            'code': 'authorization_header_count_mismatch',
            'description': 'Authorization section of headers should consist of 2 parts separated by a single space.'
        }, 401)
    if header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'bearer_not_found',
            'description': 'Expected first part of Authorization header to be bearer.'
        }, 401)
    return header_parts[1]


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 401)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True


def verify_decode_jwt(token):
    # !!NOTE urlopen has a common certificate error described here:
    # https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)

    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

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
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator


def get_response(data, success=True, error=0):
    return jsonify({
        "success": success,
        "error": error,
        "message": data
    })
