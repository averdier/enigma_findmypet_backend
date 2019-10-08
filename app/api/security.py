# coding: utf-8

import cognitojwt
from flask import g, current_app
from flask_httpauth import HTTPTokenAuth


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    try:
        user = cognitojwt.decode(
            token,
            current_app.config['PROVIDER_REGION'],
            current_app.config['AUTH_POOL'],
            app_client_id=current_app.config['AUTH_CLIENT_ID']
        )
        if user:
            g.user = user
            return True
        
        return False

    except Exception as ex:
        return False