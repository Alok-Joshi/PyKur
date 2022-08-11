import websocket
import uuid
import json
import logging
from media_element import  media_element

logging.basicConfig(filename = "kurentoclient.log",level= logging.DEBUG)

class webrtc_endpoint(media_element):
    def __init__(self, session_id, object_id, kms_url):
        super().__init__(session_id, object_id, kms_url)

    def process_sdp_offer(self,sdp_offer,callback = None,*callback_args):
        """ Sends the WebRTC Client SDP Offer to the KurentoMediServer, and returns the SDP Answer from the KurentoMediServer"""

        params = { "object":self.object_id, "operation":"processOffer","operationParams": { "offer" :sdp_offer },"sessionId": self.session_id }

        rpc_id = str(uuid.uuid4())+"_process_sdp_offer_response"
        self.add_event(rpc_id,callback,*callback_args)
        self._invoke(params,rpc_id) 
       #insert the callback in some callback dictionary, call it when you recieve sdp answer 

    def add_ice_candidate(self,candidate,callback = None,*callback_args):
        "Adds the ice candidate recieved from the other WebRTC Peer to the WebRTC Endpoint "

        params = { "object":self.object_id, "operation":"addIceCandidate","operationParams": { "candidate" : candidate },"sessionId": self.session_id }

        rpc_id = str(uuid.uuid4())+"_add_ice_candidate"+"_response"
        self.add_event(rpc_id,callback,*callback_args)
        self._invoke(params,rpc_id) 

    def gather_ice_candidates(self,callback = None,*callback_args):
        """ Triggers ICE Candidate generation by the KurentoMediServer, to be called after adding event listener """

        params = { "object":self.object_id, "operation":"gatherCandidates","sessionId": self.session_id }

        rpc_id = str(uuid.uuid4())+"_gather_ice_candidates"+"_response"
        self.add_event(rpc_id,callback,*callback_args)
        self._invoke(params,rpc_id) 
    
class player_endpoint(media_element):

    def __init__(self,session_id,object_id,rtsp_url,kms_url):
        super().__init__(session_id,object_id,kms_url)
        self.rtsp_url = rtsp_url

    def play(self,callback = None,*callback_args):
        """ Start playing the media item """
        params = { "object":self.object_id, "operation":"play","sessionId": self.session_id }

        rpc_id = str(uuid.uuid4())+"_play" +"_response"
        self.add_event(rpc_id,callback,*callback_args)
        self._invoke(params,rpc_id) 
        
    def pause(self,callback = None,*callback_args):
        """ Pause playing the media item """
        params = { "object":self.object_id, "operation":"pause","sessionId": self.session_id }

        rpc_id = str(uuid.uuid4())+"_pause"+"_response"
        self.add_event(rpc_id,callback,*callback_args)
        self._invoke(params,rpc_id) 

    def stop(self,callback = None,*callback_args):
        """ stop playing the media item """
        params = { "object":self.object_id, "operation":"stop","sessionId": self.session_id }

        rpc_id = str(uuid.uuid4())+"_stop" + "_response"
        self.add_event(rpc_id,callback,*callback_args)
        self._invoke(params,rpc_id) 
