import threading
import asyncio
import websockets
from .utilities import parse_message

class kurento_connection:

    def __init__(self,on_open,kms_url):
        self.kms_url = kms_url
        self.ws = None
        self.media_elements = list()

    async def connect(self):
        self.ws = await websockets.connect(self.kms_url)
        await self.listen_for_replies()

    async def listen_for_replies(self);
        """listens for replies """
        
        while(True):
            message = await self.ws.recv()
            self.on_message(message)

    def add_media_element(self,media_element):
        """ Adds the element to the kurento connection. Allows the element to send and recieve messages to and from kurento """
        self.media_elements.append(media_element)
        media_element.ws = self.ws
    
    def get_media_element(self,response_id):
        """ Returns the media_element """
        for media_element in self.media_elements:
            if(media_element.object_id in response_id or response_id in media_element.events):
                return media_element 

        return None

    def on_message(self,message):
        """ Gets the message and routes it to the appropriate media_element  or object """
        parsed_message = parse_message(message) 
        event_name = parsed_message["event"]

        media_element = self.get_media_element(event_name)
        media_element.on_message(parsed_message)

    def close_connection(self):
        """ Joins the thread and closes the connection """
        await self.ws.close()
