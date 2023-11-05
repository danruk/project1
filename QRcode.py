import os
import http.server
import socket
import socketserver
import webbrowser
import pyqrcode

PORT = 8010

# Getting the user's home directory in a platform-independent way
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

try:
    os.chdir(desktop)
    print("Current working directory:", os.getcwd())
except FileNotFoundError:
    print("Desktop directory not found.")

# Get the hostname
hostname = socket.gethostname()

# Get the IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = "http://" + s.getsockname()[0] + ":" + str(PORT)
link = IP

# Generate the QR code
url = pyqrcode.create(link)
url.png('myqr.png', scale=8)

# Open the QR code image in the default web browser
webbrowser.open('myqr.png')

# Serve the directory over HTTP
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    print("Type this in your Browser:", IP)
    print("or Use the QR Code")
    httpd.serve_forever()