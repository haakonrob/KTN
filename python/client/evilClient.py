# -*- coding: utf-8 -*-
import sys, traceback, socket
from time import sleep
from json import dumps as jsonify

from MessageReceiver import MessageReceiver


class Client:
    """
    This is the chat client class
    """
    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """
        # Set up the socket connection to the server
        self.host = host
        self.server_port = server_port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.messagereceiver = MessageReceiver("client", self.connection)
        self.messagereceiver.start()
        self.run()

    def run(self):
        while True:
            try:    
                msg = self.prompt_user()
                self.send_request(msg)
                
            except Exception:
                print("Exception in client. Restarting client.")
                traceback.print_exc()
                return self
                #sys.exit()

    def connect(self):
        while True:
            errno = self.connection.connect_ex((self.host, self.server_port))
            if errno == 0:
                print("Connected to server.")
                return
            else:
                print("Connection failed. Retrying...")
                sleep(1)

    def disconnect(self):

        print("Disconnected. Try to reconnect? y/n")
        if input() == 'y':
            self.connect()
        else:
            sys.exit()

    def prompt_user(self):
        msg = {}
        print(">>", end='')
        inp = input()
        args = inp.split()
        msg['request'] = args[0]
        msg['content'] = ""
        if len(args)>1:
            msg['content'] = args[1]
        return msg

    def send_request(self, request):
        #bytes(jsonify(request), 'utf-8')
        self.connection.send(bytes("asdfasdf", "utf-8"))
        
if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    while True:
        client = Client('localhost', 9997)
