from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import configparser
import random
app = Flask(__name__)

human_annotations = {0:'Lead', 1:'Position', 2:'Evidence', 3:'Claim', 4:'Concluding Statement', 5:'Counterclaim', 6:'Rebuttal', 7:'blank'}

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')


line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

@app.route("/")
def root():
    return '<link rel="shortcut icon" href="#">Root Page'

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

from langdetect import detect, DetectorFactory

# <To Do> 把 AI 接在這:
def predict_text_annotations(text):
    # 目前是一個 POC code 來驗證 line bot 的效果:
    min = 0
    max = 7
    annotation = random.randint(min, max)
    return human_annotations[annotation]

@handler.add(MessageEvent, message=TextMessage)
def predict_human_annotations(event):
    #if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
    DetectorFactory.seed = 0
    detected_lang = detect(event.message.text)
    print(detected_lang)
    if detected_lang == "en":
        pretty_text = 'Your input text annotation is "{}".'.format(predict_text_annotations(event.message.text))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pretty_text)
        )

if __name__ == "__main__":
    app.run()

if __name__ == "__main__":
    #app.run()
    app.run("0.0.0.0", 5000, debug=True)