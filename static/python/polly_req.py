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
    
    def generateMP3File(self):
        with closing(self.response["AudioStream"]) as stream:
            fileName = f"{random.randrange(1000,9999)}.mp3"
            output = os.path.join(gettempdir(), fileName)
            # Open a file for writing the output as a binary stream
            with open(output, "wb") as file:
                file.write(stream.read())
            return output


    
    def deleteMP3File(self, filePath):
        os.remove(filePath)
    
    def getError(self):
        return self.error

