import os
import webbrowser
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json


with open("setup.json", "r") as setup_file:
    setup = json.load(setup_file)
    imageServerPort = int(setup["imageServerPort"])
    imageServerFile = setup["imageServerFile"]
    
        
def open_browser(url):
    webbrowser.open_new(url)

def start_web_server(imageServerPort, imageServerFile):
    handler = SimpleHTTPRequestHandler
    server_address = ("", imageServerPort)

    httpd = HTTPServer(server_address, handler)
    
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Open the default web browser
    url = f"http://localhost:{imageServerPort}/{imageServerFile}"
    threading.Timer(1, open_browser, args=(url,)).start()

    print(f"Server started at http://localhost:{imageServerPort}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    start_web_server(imageServerPort,imageServerFile)
