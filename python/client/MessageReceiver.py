# -*- coding: utf-8 -*-
import sys, threading
from time import sleep
from json import loads as dejsonify
from MessageParser import MessageParser


class MessageReceiver(threading.Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """
    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        threading.Thread.__init__(self, name=client)
        # Flag to run thread as a deamon
        self.daemon = True
        self.connection = connection
        self.parser = MessageParser()
        #self.run()

    def run(self):
            while True:
                payload = self.connection.recv(4096)
                jresponses = payload.decode("utf-8").split("\0")
                for jresponse in jresponses:
                    if jresponse is not None and len(jresponse) > 0:
                        try:
                            response = dejsonify(jresponse)
                            print(self.parser.parse(response))#, end='')
                        except:
                            print("Couldn't dejsonify: ( ", jresponse, " )")
                        """
                        try:
                            response = dejsonify(jresponse)
                            print(self.parser.parse(response))
                        except:
                            print("Invalid response: ", response)
                        """
                


        
