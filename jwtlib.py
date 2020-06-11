from functools import wraps
from flask import request, Response
import json
from jwt import (
    JWT,
    jwk_from_dict,
    jwk_from_pem,
)

instance = JWT()
signing_key = jwk_from_dict({
    'k':'abc',
    'kty': 'oct'
    })

def encode_auth_token(utenteloggato):
    try:
        if  utenteloggato.ruolo == 'abcde':
            payload = {
            'username': utenteloggato.username,
            'ruolo': 'abcde'
            }
        elif utenteloggato.ruolo == 'root':
            payload = {
            'username': utenteloggato.username,
            'ruolo': 'root'
            }
        else:
            payload = {
                'username': utenteloggato.username
            }
        return instance.encode(
            payload,
            signing_key,
            alg='HS256'
        )
    except Exception as e:
        return e

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = False
        if not auth_token:
            auth_token = request.headers.get('capstoneAuth')
        if not auth_token:
            auth_token = request.headers.get('Authorization')
        if not auth_token:
            auth_token = request.cookies.get('capstoneAuth')
        if not auth_token:  # Authtoken no present so send 401
            return Response('Token mancante!\n' 'Mancano le autorizzazioni per effettuare la chiamata', 401,
                            {'WWW-Authenticate': 'Basic realm="Login Required"'})
        else:
            return f(*args, **kwargs)
    return decorated

def decode_auth_token(token):
    try:
        token = token.replace("Bearer ",'')
        message_received = instance.decode(token, signing_key)
        return(message_received)
    except Exception as e:
        return e