# -*- coding: utf-8 -*-
import threading, queue
from time import sleep


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
        self.messageQueue = queue.Queue(10)
        #self.run()

    def run(self):
        while True:
            message = self.connection.recv(4096)
            self.add_message_to_queue(message)
            #sleep(3)

    def add_message_to_queue(self, message):
        self.messageQueue.put(message)

    def queue_is_empty(self):
        return self.messageQueue.empty()

    def get_next_message(self):
        return self.messageQueue.get()
        
