#  coding: utf-8 
import SocketServer, socket

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

	path = (self.data.split('\r\n')[0]).split(' ')[1] 				#path
	requestType = (self.data.split('\r\n')[0]).split(' ')[2] 		#HTTP/1.1

	if path.startswith('/'):
		path = path[1:]
		
	host = "127.0.0.1"
	port = 8080
#split by splash, count 
	try:

		path = 'www/' + path

		if (path.endswith('/')):									#checks to see if looking for directory, serves index.html file
			path = path +'/index.html' 
			
		#checks for correct pathing
		#counts direction of paths, if less then 0, OK, if greater then 0, throw 404
		tmppath = path
		
		tmppath = tmppath.split('/')
				
		x = 0
		for item in tmppath:
			if (item == ".."):
				x = x + 1
			else:
				x = x - 1
			
		if (x > 0):
			raise IOError											#throws 404 error
			
		f = open(path, 'r')											#reads path file
		html = f.read()
		
		if ('css' in (path.split('/'))[-1].split('.')): 				#checks for html vs css
			acceptType = "text/css"
		else:
			acceptType = "text/html"
			
			
		self.request.sendall(requestType+" 200 OK\n"				#Sends 200 message
	        +"Content-Type:" + acceptType +" \n\n"
        	+ html + "\r\n")

	except IOError, exception:
		self.request.sendall(requestType+" 404 Not Found \n\n"		#Sends 404 messages
		+ "<html><body>404 Error</body></html>\r\n")
		print(exception)
			
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
