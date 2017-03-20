from json import loads as dejsonify

class MessageParser():
    def __init__(self):
        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_msg,
            'history': self.parse_history,	
        }
    def parse(self, payload):
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print("Cannot parse server reponse.")

    def parse_error(self, payload):
        # return an error message, maybe the server sends an explanation
        return "Error: "+payload["content"]
    
    def parse_info(self, payload):
        return payload["content"]
    
    def parse_msg(self, payload):
        # return sender, message, and time
        # payload['content']
        return payload["sender"]+": "+ payload["content"]

    def parse_history(self, payload):
        # return full history
        displaytext = "\n"

        for jmsg in payload["content"]:
            try:
                msg = dejsonify(jmsg)
                displaytext = displaytext+msg["sender"] +": "+msg["content"]+"\n"
            except:
                print("Couldn't dejsonify: ( ", jmsg, " )")
        return displaytext[0:-2]
