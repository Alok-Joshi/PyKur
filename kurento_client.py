import websocket
import uuid
import json
import logging
from endpoints import player_endpoint, webrtc_endpoint


logging.basicConfig(filename = "kurentoclient.log",level= logging.DEBUG,filemode ="w")

class kurento_client:

    def __init__(self,kms_url) -> None:

        self.kms_url = kms_url
        self.pipeline_id = None
        self.session_id = None
        self.ws = websocket.create_connection(kms_url)
        self._create_media_pipeline()
        #seperate thread for ping pong        
        
    def _create_media_pipeline(self) -> None:
        """Creates the media pipeline """
        params = { "type": "MediaPipeline", "constructorParams":{}, "properties": {} }
        response = self._create(params)

        if "result" in response:
            self.pipeline_id  = response["result"]["value"]
            self.session_id = response["result"]["sessionId"]

        elif "error" in response:
            pass #throw exception


    def _create(self,params):
        """ Creates the media element as mentioned in the params, and returns the response in the form of a python dictionary  """ 

        message = self.generate_json_rpc(params,"create")
        self.ws.send(message)
        response = json.loads(self.ws.recv())
        return response
         
    def add_endpoint(self,media_element,**kwargs):
            """ Creates the media element  and  it. Argument for PlayerEndpoint: uri """
        
            params = { "type": media_element, "constructorParams": kwargs, "properties": {} }
            message= self.generate_json_rpc(params,"create")

            self.ws.send(message)
            response = json.loads(self.ws.recv())

            if "result" in response:
                endpoint = None
                logging.info("server response: "+str(response))
                object_id = response["result"]["value"]

                if(media_element == "WebRtcEndpoint"):
                    endpoint = webrtc_endpoint(self.session_id,object_id,self.kms_url)

                elif(media_element == "PlayerEndpoint"):
                    endpoint = player_endpoint(self.session_id,object_id,kwargs["uri"],self.kms_url)

                return endpoint

            else:
                logging.error("server response ERROR: "+str(response))
                pass #handle error

    def generate_json_rpc(self,params,method):
        """ generates the json string for sending to the server """

        message = {"jsonrpc":"2.0","id":str(uuid.uuid4()),"method":method,"params":params}
        return json.dumps(message)
