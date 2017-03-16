

class MessageParser():
    def __init__(self):
        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history,	
        }
    def parse(self, payload):
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            # Response not valid
            print("Invalid message response in MessageParser")
    def parse_error(self, payload):
        # return an error message, maybe the server sends an explanation
        return "ERROR\n"+payload["content"]
    
    def parse_info(self, payload):
        return payload["response"]+" from "+payload["sender"]+"\n"+payload["content"]
    
    def parse_message(self, payload):
        # return sender, message, and time
        # payload['content']
        return "Not implemented"
    def parse_history(self, payload):
        # return full history
        return "Not implemented"
