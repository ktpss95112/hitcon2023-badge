from datetime import datetime
import sys
import socketserver


HOST, PORT = '0.0.0.0', 9999
LOGFILE = 'recv.log'


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def log(data):
    time = datetime.now()
    print(f'{time} {data}', flush=True)
    with open(LOGFILE, 'a') as fp:
        print(f'{time} {data}', file=fp, flush=True)


class Handler(socketserver.StreamRequestHandler):
    def __log(self, info):
        peer = self.client_address[0]
        log(f'{peer} {info}')

    def setup(self):
        self.__log('accept')

    def handle(self):
        while True:
            uid = self.request.recv(8)
            if len(uid) != 8:
                break

            self.__log(f'{uid=}')

    def finish(self):
        self.__log('disconnect')


if __name__ == '__main__':
    with ThreadedTCPServer((HOST, PORT), Handler) as server:
        log('Server started.')
        print('Server running (press Ctrl+C to exit)', file=sys.stderr)
        server.serve_forever()
