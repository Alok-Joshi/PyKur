import websocket-client
from .pipeline import pipeline

class kurento_client:

    def __init__(self,kms_url) -> None:
        self.kms_url = kms_url

    def create_media_pipeline(self) -> None:
        #create pipeline object
        #use .create function to create it
        pass
