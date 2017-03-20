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
                self.send_request( bytes(jsonify(msg), 'utf-8') )
                
            except Exception:
                print("Exception in client. Restarting client.")
                traceback.print_exc()
                return self

    def connect(self):
        while True:
            errno = self.connection.connect_ex((self.host, self.server_port))
            if errno == 0:
                print("Connected to server.")
                return
            else:
                print("Connection failed. Retrying...")
                sleep(1)

    def prompt_user(self):
        msg = {}

        inp = input()
        print("\033[1A\033[K", end='')

        args = inp.split()
        if len(args) is not 0:
            msg['request'] = args[0]
            msg['content'] = ""
            if len(args)>1:
                msg['content'] = inp[len(args[0])+1:]
            return msg
        
        else:
            msg["content"] = ""
            msg["request"] = ""
            return msg

    def send_request(self, request):
        self.connection.send(request)
        
if __name__ == '__main__':
    
    while True:
        try:
            Client('localhost', 9997)
        except (KeyboardInterrupt, SystemExit) : 
            sys.exit()
        except:
            print("unknown exception")
            sys.exit()
