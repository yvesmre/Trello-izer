from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import import_myob_data
import sys
import json
import pandas as pd

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)


        JSON_Response = json.loads(import_myob_data.acquire_access(query_params['code']))

        f = open("access_token.json", "w")
        with f as json_file:
            json.dump(JSON_Response, json_file, indent=4)    
        f.close()
        
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send a simple response
        message = """""<script> window.close() </script>"""
        self.wfile.write(message.encode('utf-8'))
        sys.exit()

# Set up and start the server
def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 8000)  # Listen on all interfaces at port 8000
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
