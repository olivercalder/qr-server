#!/usr/bin/env python3
'''
    qr_server.py
    Oliver Calder
    1 March 2022

    A simple QR generator server which renders a QR code given data following
    the leading / of the path following the domain.
'''
import sys
import argparse
import flask
import subprocess
import io

app = flask.Flask(__name__)

@app.route('/')
def home():
    return f'Please include data following the slash after the hostname[:port]'

@app.route('/<path:path>')
def render_path_as_qr(path):
    args = ['qrencode', '--output', '-', '--size', '10', '--margin', '2', path]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    io_result = io.BytesIO(proc.communicate()[0])
    return flask.send_file(io_result, mimetype='image/png')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A simple QR code generator API built using Flask.')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port)
