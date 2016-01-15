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

	path = (self.data.split('\r\n')[0]).split(' ')[1] #/www

	requestType = (self.data.split('\r\n')[0]).split(' ')[2] #HTTP/1.1
	request = (self.data.split('\r\n')[1]).split(': ')[1] #host:port
	#acceptType = ((self.data.split('\r\n')[3]).split(' ')[1]).split(',')[0] #text/html
	#acceptType =  ((self.data.split('\r\n')[3]).split(' ')[1])

	if path.startswith('/'):
		path = path[1:]

	#host = request.split(':')[0]
	#port = request.split(':')[1]

	host = "127.0.0.1"
	port = 8080


	try:
		#filepath = path[1:]
		
		path = 'www/' + path


		if ('index.html' not in path.split('/')) and ("base.css" not in path.split('/')): #pulls up index.html, checks html or css
			path = path +'/index.html'

		f = open(path, 'r')
		html = f.read()
		
		if ('base.css' in path.split('/')):
			acceptType = "text/css"
		else:
			acceptType = "text/html"
		
		print(requestType+" 200 OK\n"
	        +"Content-Type:" + acceptType +" \n\n"
        	+ html + "\r\n")
        	
        	
		self.request.sendall(requestType+" 200 OK\n"
	        +"Content-Type:" + acceptType +" \n\n"
        	+ html + "\r\n")

	except IOError, exception:
		self.request.sendall(requestType+" 404 Not Found \n\n" 
		+ "<html><body>404 Error</body></html>\r\n")
		print(exception)
	
	
	print(host,path,port)
	print(request, requestType)
	

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
