import uuid
import json

class media_object:
    def __init__(self,session_id,object_id):
        self.session_id = session_id
        self.object_id = object_id

    def release(self):
        """ Frees the resources of the specified object on the Kurento Media Server. Supposed to call when the media object has served its purpose """
        pass

    def generate_json_rpc(self,params,method):
        """ generates the json string for sending to the server """

        message = {"jsonrpc":"2.0","id":str(uuid.uuid4()),"method":method,"params":params}
        return json.dumps(message)

