import websocket-client
from .media_object import  media_object

class end_point(media_object):
    def __init__(self,session_id,object_id):
        super.__init__(session_id,object_id)

     def _subscribe(self,params):
        """Allows us to subscribe to an event associated with a media_element """
        pass
    
     def _invoke(self,params):
        """ Allows to invoke a particular operation in the media element """
        pass 

     def connect(self,end_point_object):
        """ Allows us to connect one endpoint to another """
        pass
    

class webrtc_endpoint(end_point):

     def process_sdp_offer(self,sdp_offer):
        """ Sends the WebRTC Client SDP Offer to the KurentoMediServer, and returns the SDP Answer from the KurentoMediServer"""
        #Define param and invoke calls
        pass;

     def add_ice_candidate(self):
        """ Adds ICE Candidate recieved from WebRTC Client to KMS"""
        #Define param and invoke calls
        pass;

     def gather_candidates(self):
        """ Triggers ICE Candidate generation by the KurentoMediServer, to be called after adding event listener """
        #Define param and invoke calls
        pass;
    
class player_endpoint(end_point):

    def __init__(self,session_id,object_id,rtsp_url):
        super.__init__(session_id,object_id)
        self.rtsp_url = rtsp_url
    
     def play():
        """ Start playing the media item """
        pass

     def pause():
        """ Pause playing the media item """
        pass

     def stop():
        """ stop playing the media item """
        pass
