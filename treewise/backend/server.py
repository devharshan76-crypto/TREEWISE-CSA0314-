"""
TreeWise Backend API Server
Powered by Python HTTP Server + C Data Structure Engine.
Provides RESTful endpoints for tree manipulation, traversal computation, and algorithm step analysis.
"""

import os
import sys
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from tree_bridge import TreeDS, CTreeEngine

PORT = 8000
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

# In-memory session state for active trees
active_tree = TreeDS()
# Initialize with standard classic BST
for val in [50, 30, 70, 20, 40, 60, 80]:
    active_tree.insert_bst(val)

c_engine = CTreeEngine()

class TreeWiseAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def _send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        url = urlparse(self.path)
        path = url.path

        if path == '/api/tree':
            # Returns current tree structure and properties
            self._send_json_response({
                "status": "success",
                "backend": "Python 3.15 + C Data Structure Engine",
                "tree": active_tree.to_dict(),
                "node_count": len(active_tree.inorder_steps()) if active_tree.val is not None else 0,
                "height": active_tree.height if active_tree.val is not None else 0
            })
            return

        elif path == '/api/traverse':
            query = parse_qs(url.query)
            t_type = query.get('type', ['inorder'])[0].lower()

            if t_type == 'inorder':
                steps = active_tree.inorder_steps()
            elif t_type == 'preorder':
                steps = active_tree.preorder_steps()
            elif t_type == 'postorder':
                steps = active_tree.postorder_steps()
            elif t_type == 'levelorder':
                steps = active_tree.levelorder_steps()
            else:
                self._send_json_response({"status": "error", "message": "Unknown traversal type"}, 400)
                return

            self._send_json_response({
                "status": "success",
                "algorithm": t_type,
                "total_steps": len(steps),
                "steps": steps
            })
            return

        elif path == '/api/search':
            query = parse_qs(url.query)
            val_param = query.get('val', [None])[0]
            if val_param is None:
                self._send_json_response({"status": "error", "message": "Missing 'val' query parameter"}, 400)
                return
            try:
                target = int(val_param)
            except ValueError:
                self._send_json_response({"status": "error", "message": "val must be an integer"}, 400)
                return

            result = active_tree.search_bst(target)
            self._send_json_response({
                "status": "success",
                "target": target,
                "found": result["found"],
                "path": result["path"]
            })
            return

        elif path == '/api/health':
            self._send_json_response({
                "status": "online",
                "platform": sys.platform,
                "c_engine_active": c_engine.lib is not None
            })
            return

        # Serve frontend static assets (HTML/CSS/JS)
        super().do_GET()

    def do_POST(self):
        url = urlparse(self.path)
        path = url.path
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len).decode('utf-8')
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._send_json_response({"status": "error", "message": "Invalid JSON body"}, 400)
            return

        global active_tree

        if path == '/api/insert':
            val = data.get('val')
            if val is None or not isinstance(val, int):
                self._send_json_response({"status": "error", "message": "Field 'val' (int) required"}, 400)
                return
            active_tree.insert_bst(val)
            self._send_json_response({
                "status": "success",
                "message": f"Inserted {val} via C Tree Engine",
                "tree": active_tree.to_dict()
            })
            return

        elif path == '/api/delete':
            val = data.get('val')
            if val is None or not isinstance(val, int):
                self._send_json_response({"status": "error", "message": "Field 'val' (int) required"}, 400)
                return
            active_tree = active_tree.delete_bst(val)
            if active_tree is None:
                active_tree = TreeDS()
            self._send_json_response({
                "status": "success",
                "message": f"Deleted {val} via C Tree Engine",
                "tree": active_tree.to_dict()
            })
            return

        elif path == '/api/preset':
            preset_name = data.get('preset', 'classic')
            presets = {
                "balanced": [50, 25, 75, 12, 37, 62, 87],
                "classic": [50, 30, 70, 20, 40, 60, 80],
                "dense": [40, 20, 60, 10, 30, 50, 70, 5, 15, 25, 35],
                "skewed": [10, 20, 30, 40, 50]
            }
            vals = presets.get(preset_name, presets['classic'])
            active_tree = TreeDS()
            for v in vals:
                active_tree.insert_bst(v)
            self._send_json_response({
                "status": "success",
                "preset": preset_name,
                "values": vals,
                "tree": active_tree.to_dict()
            })
            return

        elif path == '/api/clear':
            active_tree = TreeDS()
            self._send_json_response({
                "status": "success",
                "message": "Tree successfully cleared",
                "tree": None
            })
            return

        self._send_json_response({"status": "error", "message": "Endpoint not found"}, 404)

def run_server(port=PORT):
    server = HTTPServer(('0.0.0.0', port), TreeWiseAPIHandler)
    print("=" * 60)
    print(f"🌲 TreeWise Full-Stack Server Running")
    print(f"📡 Backend API:     http://localhost:{port}/api/tree")
    print(f"🌐 Frontend Web:    http://localhost:{port}/")
    print(f"⚙️  Architecture:   Python HTTP Server + C DSA Engine")
    print("=" * 60)
    server.serve_forever()

if __name__ == '__main__':
    run_server()
