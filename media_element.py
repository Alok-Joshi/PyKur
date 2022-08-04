import uuid
import json
import websocket

class media_element:

    def __init__(self,session_id,object_id,kms_url):
        
        self.session_id = session_id
        self.object_id = object_id
        self.kms_url = kms_url
        self.event_dictionary = dict()

        self.ws = websocket.WebSocketApp(self.kms_url,on_message= lambda ws,msg: self.on_message(ws,msg))

    def on_message(self,ws,message):
        """ Handles the responses from the server """

        message = json.loads(message)
        
        if "method" in message:
            event_type = message["params"]["type"]

            callback = self.event_dictionary[event_type][0]
            callback_args = self.event_dictionary[event_type][1]
            callback(*callback_args)

        elif "result" in message:
            callback = self.event_dictionary[message["id"]][0]
            callback_args = self.event_dictionary[message["id"]][1]
            callback(*callback_args)

        elif "error" in message:
            pass #raise exception of Kurento
        
    def _subscribe(self,params,rpc_id):
        """Allows us to subscribe to an event associated with a media_element """
        message = self.generate_json_rpc(params,"subscribe",rpc_id)
        self.ws.send(message)

    def _invoke(self,params,rpc_id):
        """ Allows to invoke a particular operation in the media element """
        message = self.generate_json_rpc(params,"invoke",rpc_id)
        self.ws.send(message)
        
    def connect(self,end_point_object,callback,*callback_args):
        """ Allows us to connect one endpoint to another """
        params = {"object":self.object_id, "operation": "connect", "operationParams": { "sink": end_point_object.object_id }, "sessionId":self.session_id }

        rpc_id = str(uuid.uuid4()) 
        self.add_event(rpc_id,callback,*callback_args)
        self._invoke(params,rpc_id)

    def register_on_event(self,event_name,callback,*callback_args):
        """ Allows to attach a callback function if we recieve an event from the KurentoMediaServer"""

        self.add_event(event_name,callback,*callback_args)
        params = { "type":event_name,"object":self.object_id,"sessionId":self.session_id }
        
        rpc_id = str(uuid.uuid4())
        self._subscribe(params,rpc_id)
        
    def add_event(self,event_name,callback,*callback_args):
        self.event_dictionary[event_name] = (callback,callback_args)
        
    def generate_json_rpc(self,params,method,rpc_id):
        """ generates the json string for sending to the server """

        message = {"jsonrpc":"2.0","id":rpc_id,"method":method,"params":params}
        return json.dumps(message)
        


