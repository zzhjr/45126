from flask import Flask, request, abort
from line_bot_sdk import LineBotApi, WebhookHandler
from line_bot_sdk.exceptions import InvalidSignatureError
from line_bot_sdk.models import TextMessage, MessageEvent

# 填入你的 Channel Access Token 和 Channel Secret
CHANNEL_ACCESS_TOKEN = 'YOUR_CHANNEL_ACCESS_TOKEN'
CHANNEL_SECRET = 'YOUR_CHANNEL_SECRET'

app = Flask(__name__)

# 初始化 LineBotApi 和 WebhookHandler
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
line_handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/")
def home():
    return "home page"
# webhook 路由，LINE 平台會將訊息發送到這裡
@app.route("/callback", methods=["POST"])
def callback():
    # 取得請求的簽名與 Body
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    # 驗證訊息簽名
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# 處理來自用戶的訊息事件
@line_handler.add(MessageEvent)
def handle_message(event):
    if isinstance(event.message, TextMessage):
        # 用戶發送的是文字訊息
        text = event.message.text
        reply_text = f"你說了：{text}"
        # 回應用戶的訊息
        line_bot_api.reply_message(event.reply_token, TextMessage(text=reply_text))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
