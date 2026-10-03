import argparse
import json
import sqlite3
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


LOCK = threading.RLock()


def setup(path):
    with sqlite3.connect(path) as db:
        db.execute('PRAGMA journal_mode=WAL')
        db.execute('CREATE TABLE IF NOT EXISTS requests (id TEXT PRIMARY KEY, prompt TEXT NOT NULL, owner TEXT, state TEXT NOT NULL, result TEXT)')
        db.execute('CREATE TABLE IF NOT EXISTS acknowledgements (request_id TEXT NOT NULL, subscriber TEXT NOT NULL, PRIMARY KEY (request_id, subscriber))')


def handler(path):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

        def db_connection(self):
            db = sqlite3.connect(path)
            db.row_factory = sqlite3.Row
            return db

        def response(self, code, value):
            data = json.dumps(value).encode()
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def body(self):
            try:
                data = json.loads(self.rfile.read(int(self.headers.get('Content-Length', '0'))))
                return data if isinstance(data, dict) else None
            except (ValueError, TypeError):
                return None

        def do_POST(self):
            route = urlparse(self.path).path.strip('/').split('/')
            body = self.body()
            if body is None:
                return self.response(400, {'error': 'invalid_json'})
            with LOCK, self.db_connection() as db:
                if route == ['requests']:
                    prompt = body.get('prompt')
                    if not isinstance(prompt, str) or not prompt.strip():
                        return self.response(400, {'error': 'invalid_prompt'})
                    rid = uuid.uuid4().hex
                    db.execute('INSERT INTO requests VALUES (?, ?, NULL, ?, NULL)', (rid, prompt, 'running'))
                    db.commit()
                    return self.response(201, {'id': rid, 'state': 'running'})
                if len(route) != 3 or route[0] != 'requests' or route[2] not in ('claim', 'ack', 'final'):
                    return self.response(404, {'error': 'not_found'})
                rid, action = route[1], route[2]
                request = db.execute('SELECT * FROM requests WHERE id=?', (rid,)).fetchone()
                if request is None:
                    return self.response(404, {'error': 'not_found'})
                subscriber = body.get('subscriber')
                if subscriber not in ('owner', 'observer'):
                    return self.response(400, {'error': 'invalid_subscriber'})
                if action == 'claim':
                    if subscriber != 'owner':
                        return self.response(403, {'error': 'owner_required'})
                    if request['state'] != 'running' or request['owner'] not in (None, 'owner'):
                        return self.response(409, {'error': 'claim_conflict'})
                    db.execute('UPDATE requests SET owner=? WHERE id=?', ('owner', rid))
                elif action == 'ack':
                    if request['state'] != 'running':
                        return self.response(409, {'error': 'terminal'})
                    db.execute('INSERT OR IGNORE INTO acknowledgements VALUES (?, ?)', (rid, subscriber))
                else:
                    if subscriber != 'owner':
                        return self.response(403, {'error': 'owner_required'})
                    if request['owner'] != 'owner' or request['state'] != 'running':
                        return self.response(409, {'error': 'not_running_or_unclaimed'})
                    result = body.get('result')
                    if not isinstance(result, str):
                        return self.response(400, {'error': 'invalid_result'})
                    db.execute('UPDATE requests SET state=?, result=? WHERE id=?', ('terminal', result, rid))
                db.commit()
                state = db.execute('SELECT state FROM requests WHERE id=?', (rid,)).fetchone()['state']
                return self.response(200, {'id': rid, 'state': state})

        def do_GET(self):
            route = urlparse(self.path).path.strip('/').split('/')
            if len(route) != 2 or route[0] != 'requests':
                return self.response(404, {'error': 'not_found'})
            with self.db_connection() as db:
                row = db.execute('SELECT * FROM requests WHERE id=?', (route[1],)).fetchone()
                if row is None:
                    return self.response(404, {'error': 'not_found'})
                acks = [r['subscriber'] for r in db.execute('SELECT subscriber FROM acknowledgements WHERE request_id=? ORDER BY subscriber', (route[1],))]
                return self.response(200, {**dict(row), 'acknowledged_by': acks})

    return Handler


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8766)
    parser.add_argument('--db', default='/tmp/broker-fixture.sqlite3')
    args = parser.parse_args()
    setup(args.db)
    ThreadingHTTPServer(('127.0.0.1', args.port), handler(args.db)).serve_forever()
