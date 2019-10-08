# coding: utf-8

import os
from app import create_app

app = create_app(os.environ.get('APP_CONFIG', 'default'))


if __name__ == '__main__':
    host = os.environ.get('HOST', 'localhost')
    try:
        port = int(os.environ.get('PORT', '5000'))
    except ValueError:
        port = 5000
    
    app.run(host, port)