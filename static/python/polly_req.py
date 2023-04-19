from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from flask import Response
from contextlib import closing
import os
import random
from tempfile import gettempdir

class PollySession:
    def __init__(self, ssml):
        session = Session()
        polly = session.client("polly")
        self.error = None
        self.response = None

        try:
            self.response = polly.synthesize_speech(Text=f'<speak>{ssml}</speak>',
                                                    Engine="standard",
                                                    TextType="ssml", 
                                                    OutputFormat="mp3", 
                                                    VoiceId="Brian")
        except (BotoCoreError, ClientError) as error:
            self.error = error

    def getMP3Blob(self):
        def generate():
            with closing(self.response["AudioStream"]) as stream:
                data = stream.read(1024)
                while data:
                    yield data
                    data = stream.read(1024)
        return Response(generate(), mimetype="audio/mpeg")
    
    def getError(self):
        return self.error

