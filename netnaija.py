import os
import http.server
import socket
import socketserver
import webbrowser
import pyqrcode
import urllib.parse

PORT = 8010

# Set the desired website link
website_link = "https://www.thenetnaija.com"

# Encode the URL to handle special characters
encoded_link = urllib.parse.quote(website_link, safe=':/#?=&')

# Get the user's home directory in a platform-independent way
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

try:
    os.chdir(desktop)
    print("Current working directory:", os.getcwd())
except FileNotFoundError:
    print("Desktop directory not found.")

# Get the IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = "http://" + s.getsockname()[0] + ":" + str(PORT)
link = IP

# Generate the QR code for the website
url = pyqrcode.create(encoded_link)
url.png('my_website_qr.png', scale=8)

# Open the QR code image in the default web browser
webbrowser.open('my_website_qr.png')

# Serve the website link over HTTP
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(301)
        self.send_header('Location', website_link)
        self.end_headers()

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("Serving at port", PORT)
    print("Website Link:", website_link)
    print("QR Code for the Website Generated")
    httpd.serve_forever()