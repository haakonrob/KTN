# -*- coding: utf-8 -*-
import sys, traceback, socket
from time import sleep
from json import dumps as jsonify
from json import loads as dejsonify
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

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
        self.parser = MessageParser()
        self.messagereceiver = MessageReceiver("client", self.connection)
        self.messagereceiver.start()
        self.run()

    def run(self):
        while True:
            try:    
                msg = self.prompt_user()
                self.send_request( bytes(jsonify(msg), 'utf-8') )
                response = self.receive_response()
                print(self.parser.parse(response))
            except Exception:
                traceback.print_exc(file=sys.stdout)
                print("Exceptional")
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
        print("request>>", end='')
        msg['request'] = input()
        print("content>>", end='')
        msg['content'] = input()
        return msg

    def send_request(self, request):
        self.connection.send(request)
        # TODO: Handle sending of a payload
        pass

    def receive_response(self):
        # TODO: Handle incoming message
	# print(MessageParser.parse(message))
        while self.messagereceiver.queue_is_empty() == True:
            pass
        resp = dejsonify(self.messagereceiver.get_next_message().decode("utf-8"))
        return resp 
        
if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
