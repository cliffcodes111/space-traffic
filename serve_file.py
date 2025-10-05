from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/connect_plot_to_app.py':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('connect_plot_to_app.py', 'r') as f:
                code = f.read()
            # Display code in a <pre> block for formatting
            html = f"<html><body><h2>connect_plot_to_app.py</h2><pre>{code}</pre></body></html>"
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8081)
    httpd = HTTPServer(server_address, SimpleHandler)
    print('Serving on http://localhost:8081/connect_plot_to_app.py')
    httpd.serve_forever()