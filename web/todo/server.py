import http.server
import os

class TodoHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save-todos':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Pad naar de jsonl file (gezien vanaf project root)
            file_path = '../data/output/todos/todo_master_list.jsonl'
            
            try:
                with open(file_path, 'wb') as f:
                    f.write(post_data)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'OK')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    port = 8000
    print(f"Server gestart op http://localhost:{port}")
    httpd = http.server.HTTPServer(('localhost', port), TodoHandler)
    httpd.serve_forever()