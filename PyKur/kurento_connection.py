import logging
import websockets
from .utilities import parse_message
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError


class kurento_connection:
    def __init__(self, kms_url):
        self.kms_url = kms_url
        self.session_obj = None
        self.ws = None
        self.media_elements = list()

    async def connect(self):
        self.ws = await websockets.connect(self.kms_url)

    async def listen_for_replies(self):
        """listens for replies"""
        while True:
            try:
                message = await self.ws.recv()
                await self.on_message(message)
            except ConnectionClosedOK:
                logging.info("connection closed")
                break
            except ConnectionClosedError:
                logging.info("connection closed. ERROR")
                break

    def add_media_element(self, media_element):
        """Adds the element to the kurento connection. Allows the element to send and recieve messages to and from kurento"""
        self.media_elements.append(media_element)

    def _get_media_element(self, response_id):
        """Returns the media_element"""
        for media_element in self.media_elements:
            if (
                media_element.object_id in response_id
                or response_id in media_element.events
            ):
                return media_element

        return None

    async def on_message(self, message):
        """Gets the message and routes it to the appropriate media_element  or object"""
        parsed_message = parse_message(message)
        event_name = parsed_message["event"]

        media_element = self._get_media_element(event_name)
        await media_element.on_message(parsed_message)

    async def close_connection(self):
        """Joins the connection"""
        await self.ws.close()
