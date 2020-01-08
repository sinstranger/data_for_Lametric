import sys
from wsgiref.simple_server import make_server

import settings


def my_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)

    return [b'Make code, not war!']


if __name__ == '__main__':
    with make_server(settings.HOST, settings.PORT, my_app) as srv:
        srv.serve_forever()
