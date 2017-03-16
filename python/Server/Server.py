# -*- coding: utf-8 -*-
import socketserver
from datetime import datetime
from json import dumps as jsonify
from json import loads as dejsonify

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

messagehistory = []

class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.possible_requests = {
            'login':    self.parse_login,
            'logout':   self.parse_logout,
            'msg':      self.parse_msg,
            'history':  self.parse_history,
            'names':    self.parse_names,
            'help':     self.parse_help,
        }
        self.username = ""
        self.loggedIn = False
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        print("New client.", self.ip)
        
        # Loop that listens for messages from the client
        while True:
            payload = self.connection.recv(4096)
            request = dejsonify(payload.decode("utf-8"))

            if request['request'] in self.possible_requests:
                response = self.possible_requests[request['request']](request)
                self.send_response(response)
               
            else:
                response = self.generate_response(self, "server", "error", "Invalid request")
                self.send_response(response)
                print("Invalid message response in server")
                
    def send_response(self, resp):
        resp["timestamp"] = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
        msg = jsonify(resp)
        payload = bytes(msg,"utf-8")
        self.connection.send(payload)
        
        
    def generate_response(self, sender, response, content):
        resp = {}
        resp["sender"]= sender
        resp["response"] = response                
        resp["content"]= content
        return resp
                     
    def parse_login(self, request):
        if self.loggedIn == True:
            return self.generate_response("server", "error", "You are already logged in")
        else:
            self.username = request['content']
            self.loggedIn = True
            # should send message history
            return self.generate_response("server", "info", "You are logged in as "+self.username+".")
            
    def parse_logout(self, request):
        if self.loggedIn == False:
            return self.generate_response("server", "error", "You are not logged in.")
        else:
            return self.generate_response("server", "info", "You are now logged out.")

    def parse_msg(self, request):
        if self.loggedIn == False:
            return self.generate_response("server", "error", "You are not logged in.")
        else:
            return self.generate_response("server", "info", "You are now logged out.")
        print("msg")
        print(request['content'])
                                          
    def parse_history(self, request):
        if self.loggedIn == False:
            return self.generate_response("server", "error", "You are not logged in.")
        else:
            return self.generate_response("server", "info", "You are now logged out.")

    def parse_names(self, request):
        if self.loggedIn == False:
            return self.generate_response("server", "error", "You are not logged in.")
        else:
            return self.generate_response("server", "info", "You are now logged out.")

    def parse_help(self, request):
        return self.generate_response("server", "info", "You are now logged out.")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.
    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print ('Server running...')
    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    # serve_forever() will ignore all timeouts!
    server.serve_forever()
