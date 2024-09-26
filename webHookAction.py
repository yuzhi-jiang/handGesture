
import requests


HOME_ASSISTANT_URL = "http://ip:8123/api/webhook/"
HEADERS = {
    "Authorization": "xxxxx",
}

webHookAction = {
    "切换卧室灯": "-_rZ-VozytptvKVGdnTwJ49v9",
    "切换卧调大音量": "-_rZ-VozytptvKVGdnTwJ49v9"
}

def send_gesture(gesture):
    #从webHookAction 中获取key 对应的value是webhook的id
    try:
        webhook_id = webHookAction.get(gesture)
        if webhook_id is None:
            return
        requests.post(HOME_ASSISTANT_URL+webhook_id, headers=HEADERS)
    except:
        print('无法发起请求')
