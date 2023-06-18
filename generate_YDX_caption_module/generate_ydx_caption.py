import json
import os
from typing import Dict
import requests

class GenerateYDXCaption:
    def __init__(self, video_runner_obj: Dict[str, int]):
        self.video_runner_obj = video_runner_obj
    
    def generateYDXCaption(self):
        userId = os.getenv('YDX_USER_ID')
        aiUserId = os.getenv('YDX_AI_USER_ID')
        if(userId == None):
            userId = "65c433f7-ceb2-495d-ae01-994388ce56f5"
        data = {
        "userId" : userId,
        "youtubeVideoId" : self.video_runner_obj.get("video_id"),
        # Change AI ID to the ID of the AI you want to use
        "aiUserId": aiUserId
        }
        ydx_server = os.getenv('YDX_WEB_SERVER')
        if(ydx_server == None):
            ydx_server = 'http://3.101.130.10:4000'
        url = '{}/api/create-user-links/create-new-user-ad'.format(ydx_server)
        headers = {"Content-Type": "application/json; charset=utf-8"}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        data = response.json()
        if(response.status_code == 200):
            print("Success")
            requests.get(data['url'])
        else:
            print("Failure in generating YDX Caption")
            print(data.get('message'))