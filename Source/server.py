# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import csv
import driver as dr
import random

hostName = "localhost"
serverPort = 8069

class MyServer(BaseHTTPRequestHandler):
    service = dr.build_drive_service()
    ids = []
    with open("data/data.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for lines in reader:
            ids.append(lines[0])
    def do_GET(self):
        start = time.time()
        im = dr.get_image(self.service, self.ids[random.randrange(len(self.ids))])
        self.send_response(200)
        self.send_header("Content-type", "image")
        self.end_headers()
        self.wfile.write(im.getbuffer())
        end = time.time()
        print(f"Took {end - start}")


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)

    webServer.server_close()
    print("Server stopped.")