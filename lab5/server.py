import socket
import select
import string
import types
import pathlib
import os
import random as rnd
from collections import namedtuple


BASE_DIR = pathlib.Path(__file__).parent.resolve()
MEDIA_DIR = os.path.join(BASE_DIR, 'server_media')
SIZE = 1024
UTF8 = 'utf-8'
UPLOAD = 'upload'
DOWNLOAD = 'download'


Session = namedtuple('Session', ['address', 'file'])
sessions = {}
callback = {}
generators = {}


def reactor(host, port):
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)
    sock.setblocking(False)  

    sessions[sock] = None
    print(f'Server up, running, and waiting for call on {host} {port}')

    try:
        while True:
            # Serve existing clients only if they already have data ready
            ready_to_read, _, _ = select.select(sessions, [], [], 0.1)
            for conn in ready_to_read:
                if conn is sock:
                    conn, cli_address = sock.accept()
                    connect(conn, cli_address)
                    continue

                chunk = conn.recv(SIZE)
                if chunk:
                    callback[conn](conn, chunk)
                else:
                    disconnect(conn)

    finally:
        sock.close()


def connect(conn, cli_address):
    sessions[conn] = Session(cli_address, conn.makefile())

    gen = process_request(conn)
    generators[conn] = gen
    callback[conn] = gen.send(None)


def disconnect(conn):
    gen = generators.pop(conn)
    gen.close()
    sessions[conn].file.close()
    conn.close()

    del sessions[conn]
    del callback[conn]


def generate_name(name='f-', format='txt'):
    name += ''.join(rnd.choices(
        string.ascii_uppercase + string.digits, k=8)
    )
    name += f'.{format}'
    return name


async def process_request(conn):
    print(f'Received connection from {sessions[conn].address}')
    filename = generate_name()
    mode = UPLOAD

    while True:
        chunk = await read_chunk(conn)

        if chunk.startswith(f'{UPLOAD}: '.encode(UTF8)):
            mode = UPLOAD
            text = chunk.decode(UTF8)

            fullname = text \
                .split(f'{UPLOAD}: ')[-1] \
                .strip() \
                .split('.')
            format = fullname.pop()
            name = ''.join(fullname)

            filename = generate_name(name, format)
            conn.sendall(b'filename received')
            continue
        elif chunk.startswith(f'{DOWNLOAD}'.encode(UTF8)):
            mode = DOWNLOAD
            text = chunk.decode(UTF8)

            filename = text \
                .split(f'{DOWNLOAD}: ')[-1] \
                .strip()

            conn.sendall(b'filename received')

            with open(os.path.join(MEDIA_DIR, filename), 'rb') as f:
                data = f.read(SIZE)
                while data:
                    conn.sendall(data)
                    data = f.read(SIZE)
                return

        if mode == UPLOAD:
            with open(os.path.join(MEDIA_DIR, filename), 'ab') as f:
                f.write(chunk)


@types.coroutine
def read_chunk(conn):
    def inner(conn, chunk):
        gen = generators[conn]
        try:
            callback[conn] = gen.send(chunk)  # Continue the generator
        except StopIteration:
            disconnect(conn)

    chunk = yield inner
    return chunk


if __name__ == '__main__':
    reactor('localhost', 8081)
