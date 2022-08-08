class KurentoException(Exception):
    """ Custom exception for dealing with kurento media responses """
    def __init__(self,server_error):

        server_error = self.parse_error(server_error)
        super().__init__(server_error)
        pass

    def parse_error(self, server_error_dict):
        return f" Error Code {server_error_dict['code']} : {server_error_dict['message']} "
            
        
