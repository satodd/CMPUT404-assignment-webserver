#  coding: utf-8 
import SocketServer, os, socket

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
	path = (self.data.split('\r\n')[0]).split(' ')[1]
	request = (self.data.split('\r\n')[1]).split(': ')[1]

	#os.chdir(hostline + path)

	host = request.split(':')[0]
	port = request.split(':')[1]

	print(host+path,port)


	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#serverSocket.bind(("0.0.0.0", 6666))
	serverSocket.listen(5)

	while True:
		(incomingSocket, address) = serverSocket.accept()

		childPid = os.fork()
		if (childPid != 0):
			#must be still in the connecting accepting process
			continue
		#else, we must be in a client talking process

		outgoingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		outgoingSocket.connect(("host+path", port))
	
		done = False
		while not done:
			incomingSocket.setblocking(0)
			try:
				part = incomingSocket.recv(2048)
			except IOError, exception:
				if exception.errno == 11:
					part = None
				else:
					raise 		
			if (part):
				outgoingSocket.sendall(part) 


			outgoingSocket.setblocking(0)
			try:
				part = outgoingSocket.recv(2048)
			except IOError, exception:
				if exception.errno == 11:
					part = None
				else:
					raise 		
			if (part):
				incomingSocket.sendall(part) 





	
	#self.request.sendall(request+path)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
