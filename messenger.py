import requests
import json

class Messenger():

    def __init__(self):
        with open('webhook_url.txt') as f:
            self._webhook_url = f.read()

    def send_post(self, usr, img_url):
        post_data = {
            "attachments": [{
                "color": "#FFC0CB",
                "fields": [
                    {
                        "value": "{}さんがプロフィール画像を変更しました!".format(usr)
                    }
                ],
                "image_url" : img_url
            }]
        }

        requests.post(self._webhook_url, data=json.dumps(post_data))