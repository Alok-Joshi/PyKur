import json
import logging
from .exception import KurentoException
from .utilities import generate_json_rpc,parse_message,rpc_id_generator

#websocket.enableTrace(True)
logging.basicConfig(filename = "kurentoclient.log",level= logging.DEBUG,filemode = "w")

class media_element:

    def __init__(self,session_id,object_id):
        
        self.session_id = session_id
        self.object_id = object_id
        self.event_dictionary = dict()
        self.ws = None #Will be given by the kurento_connection object when we register a media element to it
        self.events = set() #Contains all the legal events on can subscribe to for the media element

    def set_connection(self,konn_obj):
        """ Function assigns a websocket connection object to the media element. Also registers the media element with the connection object for routing of messages. enables the media element to communicate with the server  """
        self.ws = konn_obj.ws
        konn_obj.add_media_element(self)

    async def on_message(self,parsed_message):
        """ Parses the message recieved from the kurento media server and handles the message by calling the appropriate callback function assigned to the server response """

        try:
            logging.info("Server Response: "+str(parsed_message))
            if(parsed_message["status"] == 1):
                callback  = self.event_dictionary[parsed_message["event"]][0]
                callback_args  = self.event_dictionary[parsed_message["event"]][1]
                logging.debug(f"{callback}  {callback_args}")
                if(callback is not None):
                    server_response = parsed_message["server_response"]
                    if(parsed_message["server_response"] is not None):
                        await callback(server_response,*callback_args)
                    else:
                        await callback(*callback_args)
            else:
                raise KurentoException(parsed_message["error"])
        except Exception as e:
            print(e)      
            

    async def _subscribe(self,params,rpc_id):
        """Allows us to subscribe to an event associated with a media_element """
        message = generate_json_rpc(params,"subscribe",rpc_id)
        await self.ws.send(message)

    async def _invoke(self,params,rpc_id):
        """ Allows to invoke a particular operation in the media element """
        message = generate_json_rpc(params,"invoke",rpc_id)
        await self.ws.send(message)
        
    async def connect(self,media_element_object,callback = None,*callback_args):
        """ Allows us to connect one endpoint to another """
        params = {"object":self.object_id, "operation": "connect", "operationParams": { "sink": media_element_object.object_id }, "sessionId":self.session_id }

        rpc_id = rpc_id_generator(self.object_id,"connect_response") 
        self.add_event(rpc_id,callback,*callback_args)
        await self._invoke(params,rpc_id)

    async def register_on_event(self,event_name,callback = None,*callback_args):
        """ Allows to attach a callback function if we recieve an event from the KurentoMediaServer"""
        if(event_name not in self.events):
            raise KurentoException(f"Illegal event : {event_name}")

        self.add_event(event_name,callback,*callback_args)
        params = { "type":event_name,"object":self.object_id,"sessionId":self.session_id }
        rpc_id = rpc_id_generator(self.object_id,"subscribe_response")

        self.add_event(rpc_id) #for the subscribe response 
        await self._subscribe(params,rpc_id)
        
    def add_event(self,event_name,callback = None,*callback_args):
        self.event_dictionary[event_name] = (callback,callback_args)

    async def release(self):
        """  releases the media element on the kurento server """
        params = {"object":self.object_id, "sessionId":self.session_id }

        rpc_id = rpc_id_generator(self.object_id,"release_response")
        message = generate_json_rpc(params,"release",rpc_id)

        self.add_event(rpc_id)
        await self.ws.send(message)

        



