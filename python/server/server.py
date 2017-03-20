# -*- coding: utf-8 -*-
import sys, socketserver, traceback
from datetime import datetime
from json import dumps as jsonify
from json import loads as dejsonify

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
messagehistory = []
clients = []

def generate_response(sender, response, content):
        resp = {}
        resp["sender"]= sender
        resp["response"] = response                
        resp["content"]= content
        return resp

def broadcast(client, message):
    for c in clients:
        if client != c:
            c.send_response(message)


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

        self.username = ""
        self.loggedIn = False
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        clients.append(self)
        print("New client - ", self.ip, ":", self.port)

        self.possible_requests = {
            "login":    self.parse_login,
            "logout":   self.parse_logout,
            "msg":      self.parse_msg,
            "names":    self.parse_names,
            "help":     self.parse_help,
        }
        
        while True:
            try:
                payload = self.connection.recv(4096)
                request = dejsonify(payload.decode("utf-8"))

                if request["request"] in self.possible_requests:
                    response = self.possible_requests[request["request"]](request)
                    self.send_response(response)
                   
                else:
                    response = generate_response("server", "error", "Invalid request")
                    self.send_response(response)

            except:
                print("Exception in handler for", self.username, ". Removing handler.")
                traceback.print_exc()
                clients.remove(self)
                return self
                
    def send_response(self, resp):
        resp["timestamp"] = datetime.now().strftime("%H:%M:%S %Y-%m-%d")
        msg = jsonify(resp) +"\0"
        payload = bytes(msg,"utf-8")
        self.connection.send(payload)
        
        
    
                     
    def parse_login(self, request):
        if self.loggedIn == True:
            resp = generate_response("server", "error", "You are already logged in")
        elif len(request["content"]) is 0:
            return generate_response("server", "error", "login needs an argument.")
        else:
            self.username = request["content"]
            self.loggedIn = True

            welcomemsg = generate_response("server", "info", "You are logged in as "+self.username+".")
            self.send_response(welcomemsg)
            return generate_response("server", "history", messagehistory)
            
    def parse_logout(self, request):
        if self.loggedIn == False:
            return generate_response("server", "error", "You are not logged in.")
        else:
            self.loggedIn = False
            return generate_response("server", "info", "You are now logged out.")

    def parse_msg(self, request):
        if self.loggedIn == False:
            return generate_response("server", "error", "You are not logged in.")
        elif len(request["content"]) is 0:
            return generate_response("server", "error", "msg needs an argument.")
        else:
            bcastmsg = generate_response(self.username, "message", request["content"])
            broadcast(self, bcastmsg)
            messagehistory.append(jsonify(bcastmsg))
            return bcastmsg
                                          
    def parse_names(self, request):
        if self.loggedIn == False:
            return generate_response("server", "error", "You are not logged in.")
        else:
            resp = "Users online:"
        for client in clients:
            resp = resp + "\n" + client.username
        return generate_response("server", "info", resp)

    def parse_help(self, request):
        resp = "Possible requests: "
        for key in self.possible_requests.keys():
            resp = resp + "\n"+key
        return generate_response("server", "info", resp)



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True



if __name__ == "__main__":
    HOST, PORT = "localhost", 9997
    print ("Server running...")

    startmsg = generate_response("server", "message", "Chat started")
    startmsg["timestamp"] = datetime.now().strftime("%H:%M:%S %Y-%m-%d")
    messagehistory.append(jsonify(startmsg))

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    # serve_forever() will ignore all timeouts!
    server.serve_forever()
