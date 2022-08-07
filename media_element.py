import uuid
import json
import websocket
import threading
import logging
import time
#websocket.enableTrace(True)
logging.basicConfig(filename = "kurentoclient.log",level= logging.DEBUG,filemode = "w")

class media_element:

    def __init__(self,session_id,object_id,kms_url):
        
        self.session_id = session_id
        self.object_id = object_id
        self.kms_url = kms_url
        self.event_dictionary = dict()

        self.ws = websocket.WebSocketApp(self.kms_url,on_message= lambda ws,msg: self.on_message(ws,msg))
        self.ws_thread = threading.Thread(target = self.ws.run_forever,args=(None, None, 60, 30))
        self.ws_thread.start()
        time.sleep(2) #to allow the websocket connection to properly initialise, will replace this with a method ot check connection status

    def ping(self):
        params = {"interval":240000}
        rpc_id = str(uuid.uuid4())
        message = self.generate_json_rpc(params,"ping",rpc_id) 
        self.ws.send(message)  

    def _parse_message(self, message):
            """ Parses the server response into a standard format. 
            {event_id : message["id"], status: success/failure, server_response (in event of success) :  message["result"]["value"] OR server_error: message["error"] } """

            parsed_message = dict()
            message = json.loads(message)
            if "method" in message:
                message["event"] = message["params"]["value"]["type"]
                message["server_response"] = message["params"]["value"]
                message["status"] = "SUCCESS" 

            elif "result" in message:
                parsed_message["event"] = message["id"]
                parsed_message["status"] = 1 

                if "value" in message["result"]:
                    parsed_message["server_response"] = message["result"]["value"]
                else:
                    parsed_message["server_response"] = None

            elif "error" in message:
                parsed_message["event"] = message["id"]
                parsed_message["status"] = 0
                parsed_message["error"] = message["error"]

            return parsed_message

    def on_message(self,ws,message):
        parsed_message = self._parse_message(message) 

        if(parsed_message["status"] == 1):
            callback  = self.event_dictionary[parsed_message["event"]][0]
            callback_args  = self.event_dictionary[parsed_message["event"]][1]
            
            if(callback is not None):
                server_response = parsed_message["server_response"]
                if(parsed_message["server_response"] is not None):
                    callback(server_response,*callback_args)
                else:
                    callback(*callback_args)
        else:
            pass #throw exception OR use given on_error callback 
            
            
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
        rpc_id = "subcribe_"+event_name 
        self._subscribe(params,rpc_id)
        
    def add_event(self,event_name,callback,*callback_args):
        self.event_dictionary[event_name] = (callback,callback_args)
        
    def generate_json_rpc(self,params,method,rpc_id):
        """ generates the json string for sending to the server """

        message = {"jsonrpc":"2.0","id":rpc_id,"method":method,"params":params}
        return json.dumps(message)
    def _response_parser(self,response):
        """ Parses the response into a standardised format. Returns a dictionary """ 
        parsed_response = dict()
        if "method" in response:
            pass #handle onevents
        else:
            parsed_response["event_id"] = parsed_response["id"]
