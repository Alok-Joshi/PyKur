class media_object:
    def __init__(self,session_id,object_id):
        self.session_id = session_id
        self.object_id = object_id

    def release(self):
        """ Frees the resources of the specified object on the Kurento Media Server. Supposed to call when the media object has served its purpose """
        pass

    def _create_json_rpc(method,params):
        """ Takes the method and params, and returns a json string """

