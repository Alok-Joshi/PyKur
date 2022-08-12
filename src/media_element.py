import uuid
import json
import websocket
import threading
import logging
import time
from exception import KurentoException
from utilities import generate_json_rpc,parse_message

#websocket.enableTrace(True)
logging.basicConfig(filename = "kurentoclient.log",level= logging.DEBUG,filemode = "w")

class media_element:

    def __init__(self,session_id,object_id):
        
        self.session_id = session_id
        self.object_id = object_id
        self.event_dictionary = dict()
        self.ws = None #Will be given by the kurento_connection object when we register a media element to it

        
    def on_message(self,ws,message):
        """ Parses the message recieved from the kurento media server and handles the message by calling the appropriate callback function assigned to the server response """

        parsed_message = parse_message(message) 
        try:
            logging.info("Server Response: "+str(parsed_message))
            if(parsed_message["status"] == 1):
                callback  = self.event_dictionary[parsed_message["event"]][0]
                callback_args  = self.event_dictionary[parsed_message["event"]][1]
                logging.debug(f"{callback}  {callback_args}")
                if(callback is not None):
                    server_response = parsed_message["server_response"]
                    if(parsed_message["server_response"] is not None):
                        callback(server_response,*callback_args)
                    else:
                        callback(*callback_args)
            else:
                raise KurentoException(parsed_message["error"])
        except Exception as e:
            print(e)      
            
    def rpc_id_generator(self,event_type):
        # TODO: WIll use the object id and some extra parameters depending on the type of event 
        pass

    def _subscribe(self,params,rpc_id):
        """Allows us to subscribe to an event associated with a media_element """
        message = generate_json_rpc(params,"subscribe",rpc_id)
        self.ws.send(message)

    def _invoke(self,params,rpc_id):
        """ Allows to invoke a particular operation in the media element """
        message = generate_json_rpc(params,"invoke",rpc_id)
        self.ws.send(message)
        
    def connect(self,media_element_object,callback = None,*callback_args):
        """ Allows us to connect one endpoint to another """
        params = {"object":self.object_id, "operation": "connect", "operationParams": { "sink": media_element_object.object_id }, "sessionId":self.session_id }

        rpc_id = str(uuid.uuid4()) 
        self.add_event(rpc_id,callback,*callback_args)
        self._invoke(params,rpc_id)

    def register_on_event(self,event_name,callback = None,*callback_args):
        """ Allows to attach a callback function if we recieve an event from the KurentoMediaServer"""

        self.add_event(event_name,callback,*callback_args)
        params = { "type":event_name,"object":self.object_id,"sessionId":self.session_id }
        rpc_id = "subcribe_"+event_name+"_response"
        self.add_event(rpc_id,None,())
        self._subscribe(params,rpc_id)
        
    def add_event(self,event_name,callback = None,*callback_args):
        self.event_dictionary[event_name] = (callback,callback_args)
        
