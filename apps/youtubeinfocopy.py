from googleapiclient.discovery import build
import os

class YouTubeInfo:
    DEVELOPER_KEY = "AIzaSyAX_Q6kIbXlUuV6BIwfjaA5IZipMhchWn8"
    DEVELOPER_KEY2 = "AIzaSyC6VAjJ_pxJ9MwFKzB93o55r0y1FFiRa-4"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    QUOTA_INITIAL=20000

    def __init__(self):
        self.quota = 20000
        self.developerkey=self.DEVELOPER_KEY
    
    def CheckQuotaRemain(self):
        if self.quota > 11000:
            self.developerkey = self.DEVELOPER_KEY
        elif self.quota > 2000:
            self.developerkey = self.DEVELOPER_KEY2

    def BuildApiService(self):
        return build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=self.developerkey)
    
    def QuotaSub(self, minus):
        self.quota -= minus

    def QuotaReset(self):
        self.quota = self.QUOTA_INITIAL
