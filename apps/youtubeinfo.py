from googleapiclient.discovery import build
import os

class YouTubeInfo:
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    QUOTA_INITIAL=20000

    def __init__(self):
        self.quota = 20000
        self.developerkey = os.environ.get("YOUTUBE_API_KEY",None)
    
    def CheckQuotaRemain(self):
        if self.quota > 11000:
            self.developerkey = os.environ.get("YOUTUBE_API_KEY",None)
        elif self.quota > 2000:
            self.developerkey = os.environ.get("YOUTUBE_API_KEY2",self.developerkey)

    def BuildApiService(self):
        return build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=self.developerkey)
    
    def QuotaSub(self, minus):
        self.quota -= minus

    def QuotaReset(self):
        self.quota = self.QUOTA_INITIAL
