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

# Set the max content length to the maximum number of arbitrary bytes which can
# be encoded in a QR code. See: https://www.qrcode.com/en/about/version.html
app.config['MAX_CONTENT_LENGTH'] = 2953

@app.route('/', methods=['GET', 'POST'])
def render_body_as_qr():
    data = flask.request.get_data(cache=False)
    if len(data) == 0:
        return 'Please include data in the request body or following the slash after the hostname[:port]', 400
    args = ['qrencode', '--output', '-', '--size', '10', '--margin', '2']
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    io_result = io.BytesIO(proc.communicate(input=data)[0])
    return flask.send_file(io_result, mimetype='image/png')

@app.route('/<path:path>', methods=['GET', 'POST'])
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
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port)
