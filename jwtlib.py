import json
from datetime import datetime, timedelta, timezone

from jwt import (
    JWT,
    jwk_from_dict,
    jwk_from_pem,
)
from jwt.utils import get_int_from_datetime

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
            'role': 'root'
            }
        elif utenteloggato.ruolo == 'root':
            payload = {
            'username': utenteloggato.username,
            'role': 'fake_root'
            }


        payload = {
            'username': utenteloggato.username,
            'role': utenteloggato.ruolo
        }
        return instance.encode(
            payload,
            signing_key,
            alg='HS256'
        )
    except Exception as e:
        return e