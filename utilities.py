import json
import logging

def generate_json_rpc(self,params,method,rpc_id):
    """ generates the json string for sending to the server """

    message = {"jsonrpc":"2.0","id":rpc_id,"method":method,"params":params}
    return json.dumps(message)


def  parse_message(self, message):
            """ Parses the server response into a standard format. 
            {event_id : message["id"], status: success/failure, server_response (in event of success) :  message["result"]["value"] OR server_error: message["error"] } """

            parsed_message = dict()
            logging.info("Server Response:"+message)
            message = json.loads(message)
            if "method" in message:
                parsed_message["event"] = message["params"]["value"]["type"]
                parsed_message["server_response"] = message["params"]["value"]
                parsed_message["status"] = 1 

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



