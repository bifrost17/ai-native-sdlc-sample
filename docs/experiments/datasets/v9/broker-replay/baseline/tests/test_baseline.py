import importlib.util
import json
import sqlite3
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('broker_fixture', HERE / 'server.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BaselineTest(unittest.TestCase):
    def test_ack_is_running_until_final(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / 'broker.sqlite3')
            module.setup(path)
            with sqlite3.connect(path) as db:
                db.execute('INSERT INTO requests VALUES (?, ?, ?, ?, ?)', ('r1', 'test', 'owner', 'running', None))
                db.execute('INSERT INTO acknowledgements VALUES (?, ?)', ('r1', 'owner'))
                self.assertEqual(db.execute('SELECT state FROM requests WHERE id=?', ('r1',)).fetchone()[0], 'running')

    def test_http_owner_observer_ack_and_final(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / 'broker.sqlite3')
            module.setup(path)
            server = ThreadingHTTPServer(('127.0.0.1', 0), module.handler(path))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base = f'http://127.0.0.1:{server.server_port}'
            def call(method, route, body=None):
                request = Request(base + route, data=json.dumps(body).encode() if body is not None else None, method=method, headers={'Content-Type': 'application/json'})
                with urlopen(request) as response:
                    return json.load(response)
            try:
                rid = call('POST', '/requests', {'prompt': 'test'})['id']
                request = Request(base + f'/requests/{rid}/claim', data=b'{"subscriber":"observer"}', method='POST', headers={'Content-Type': 'application/json'})
                with self.assertRaises(HTTPError) as denied:
                    urlopen(request)
                self.assertEqual(denied.exception.code, 403)
                call('POST', f'/requests/{rid}/claim', {'subscriber': 'owner'})
                call('POST', f'/requests/{rid}/ack', {'subscriber': 'owner'})
                call('POST', f'/requests/{rid}/ack', {'subscriber': 'observer'})
                self.assertEqual(call('GET', f'/requests/{rid}')['state'], 'running')
                call('POST', f'/requests/{rid}/final', {'subscriber': 'owner', 'result': 'done'})
                self.assertEqual(call('GET', f'/requests/{rid}')['state'], 'terminal')
            finally:
                server.shutdown()
                server.server_close()


if __name__ == '__main__':
    unittest.main()
