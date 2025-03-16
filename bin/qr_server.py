#!/usr/bin/env python3
'''
    qr_server.py
    Oliver Calder
    Created 1 March 2022

    A simple server to generate QR codes for data following the / in the URL.
'''
import argparse
import flask
import io
import os
import subprocess
import sys

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
    parser = argparse.ArgumentParser(
            prog=os.path.basename(sys.argv[0]),
            description='A simple server to generate QR codes, built using Flask and qrencode.')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    parser.add_argument('--max-content-length', type=int, default=100, help='the maximum content length in request bodies, in MiB')
    arguments = parser.parse_args()
    app.config['MAX_CONTENT_LENGTH'] = arguments.max_content_length * 1024 * 1024
    app.run(host=arguments.host, port=arguments.port)
