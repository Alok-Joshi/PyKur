import websocket
import json
from kurento_client import generate_json_rpc
from .media_object import  media_object

class end_point(media_object):

    def __init__(self,session_id,object_id,kms_url):
        super.__init__(session_id,object_id)
        self.kms_url = kms_url
        self.event_dictionary = dict()
        self.ws = websocket.WebSocketApp(self.kms_url,on_message= lambda ws,msg: self.on_message(ws,msg))

    def on_message(self,ws,message):
        #handle ice candidate, callback, seperate dictionary for callback
        pass
        
    def _subscribe(self,params):
        """Allows us to subscribe to an event associated with a media_element """
        message = self.generate_json_rpc(params,"subscribe")
        self.ws.send(message)

    def _invoke(self,params):
        """ Allows to invoke a particular operation in the media element """
        message = self.generate_json_rpc(params,"invoke")
        self.ws.send(message)
        
    def connect(self,end_point_object):
        """ Allows us to connect one endpoint to another """
        params = {"object":self.object_id, "operation": "connect", "operationParams": { "sink": end_point_object.object_id }, "sessionId":self.session_id }
        self._invoke(params) 

    def register_on_event(self,event_name,callback):
        """ Allows to attach a callback function if we recieve an event from the KurentoMediaServer"""

        self.add_event(event_name,callback)
        params = { "type":event_name,"object":self.object_id,"sessionId":self.session_id }
        self._subscribe(params)
        
    def add_event(self,event_name,callback):
        self.event_dictionary[event_name] = callback
        

class webrtc_endpoint(end_point):
    def __init__(self, session_id, object_id, kms_url):
        super().__init__(session_id, object_id, kms_url)

    def on_message(self,ws,message):
        message = json.loads(message)
        
        pass

    def process_sdp_offer(self,sdp_offer,callback):
        """ Sends the WebRTC Client SDP Offer to the KurentoMediServer, and returns the SDP Answer from the KurentoMediServer"""

        params = { "object":self.object_id, "operation":"processOffer","operationParams": { "offer" :sdp_offer },"sessionId": self.session_id }
        self._invoke(params) 
       #insert the callback in some callback dictionary, call it when you recieve sdp answer 

    def add_ice_candidate(self,candidate):
        """ Adds ICE Candidate recieved from WebRTC Client to KMS"""

        params = { "object":self.object_id, "operation":"addIceCandidate","operationParams": { "candidate" : candidate },"sessionId": self.session_id }
        self._invoke(params) 

    def gather_ice_candidates(self):
        """ Triggers ICE Candidate generation by the KurentoMediServer, to be called after adding event listener """

        params = { "object":self.object_id, "operation":"gatherCandidates","sessionId": self.session_id }
        self._invoke(params) 
    
class player_endpoint(end_point):

    def __init__(self,session_id,object_id,rtsp_url,kms_url):
        super.__init__(session_id,object_id,kms_url)
        self.rtsp_url = rtsp_url
    
    def on_message(self,ws,message):
        #handle ice candidate, callback, seperate dictionary for callback
        pass

    def play(self):
        """ Start playing the media item """
        params = { "object":self.object_id, "operation":"play","sessionId": self.session_id }
        self._invoke(params) 
        
    def pause(self):
        """ Pause playing the media item """
        params = { "object":self.object_id, "operation":"pause","sessionId": self.session_id }
        self._invoke(params) 

    def stop(self):
        """ stop playing the media item """
        params = { "object":self.object_id, "operation":"stop","sessionId": self.session_id }
        self._invoke(params) 
