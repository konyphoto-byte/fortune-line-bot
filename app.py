import os
import random
from datetime import datetime
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
MessageEvent, TextMessage, TextSendMessage,
ImageSendMessage, FlexSendMessage
)

app = Flask(**name**)

# 環境変数から取得(後で設定します)

line_bot_api = LineBotApi(os.environ.get(‘CHANNEL_ACCESS_TOKEN’, ‘YOUR_CHANNEL_ACCESS_TOKEN’))
handler = WebhookHandler(os.environ.get(‘CHANNEL_SECRET’, ‘YOUR_CHANNEL_SECRET’))

# 占い機能

def get_daily_fortune():
“”“今日の運勢を生成”””
# 日付をシードにして毎日同じ結果になるように
today = datetime.now().strftime(’%Y%m%d’)
random.seed(today)

```
# 運勢スコア (0-100点)
score = random.randint(30, 100)

# スコアに応じたメッセージ
if score >= 90:
    level = "🌟 絶好調!"
    advice_list = [
        "今日は何でもうまくいく日!積極的にチャレンジしてみて!",
        "最高の一日になりそう!新しいことを始めるのに最適!",
        "運気MAX!やりたかったこと、今日やっちゃいましょ!"
    ]
elif score >= 75:
    level = "✨ 好調!"
    advice_list = [
        "良い流れが来てます!周りの人に感謝を伝えると◎",
        "調子いい日!ただし調子に乗りすぎ注意w",
        "チャンスが舞い込みそう!アンテナ張っておいてね!"
    ]
elif score >= 60:
    level = "😊 まずまず"
    advice_list = [
        "普通にいい日!無理せずマイペースでいきましょ",
        "安定した運気!いつも通りで大丈夫です",
        "平和な一日になりそう!リラックスして過ごして"
    ]
elif score >= 45:
    level = "😐 普通"
    advice_list = [
        "可もなく不可もなく!焦らず着実にいきましょ",
        "地道な努力が大事な日!コツコツやっていこ",
        "慌てず騒がず!落ち着いて行動すれば問題なし"
    ]
else:
    level = "😅 要注意"
    advice_list = [
        "ちょっと慎重に!財布とか忘れ物注意してね",
        "今日は守りの日!無理な挑戦は避けた方がいいかも",
        "トラブル回避モードで!いつもより確認を丁寧に"
    ]

advice = random.choice(advice_list)

# ラッキーカラー
colors = [
    "❤️ 赤", "💙 青", "💚 緑", "💛 黄色", 
    "🧡 オレンジ", "💜 紫", "🤍 白", "🖤 黒",
    "💗 ピンク", "🤎 茶色"
]
lucky_color = random.choice(colors)

# ラッキーアイテム
items = [
    "☕ コーヒー", "📱 スマホケース", "🎧 イヤホン",
    "⌚ 腕時計", "👓 メガネ", "📝 ノート",
    "🍀 四つ葉のクローバー", "💍 アクセサリー", "🔑 鍵",
    "🎒 バッグ", "🧸 ぬいぐるみ", "🍫 チョコレート",
    "🌸 花", "📚 本", "🎵 音楽",
    "🍵 お茶", "🕯️ キャンドル", "✨ キラキラしたもの"
]
lucky_item = random.choice(items)

message = f"""🔮 今日の運勢 🔮
```

{datetime.now().strftime(’%Y年%m月%d日’)}

【総合運】{score}点
{level}

【今日のアドバイス】
{advice}

【ラッキーカラー】
{lucky_color}

【ラッキーアイテム】
{lucky_item}

良い一日を〜!✨”””

```
return message
```

# 定期送信用エンドポイント(cronから呼ばれる)

@app.route(’/send_fortune’, methods=[‘POST’])
def send_fortune():
“”“毎朝8時に占いを送信”””
try:
# ここにユーザーIDを設定(後で説明します)
user_id = os.environ.get(‘LINE_USER_ID’, ‘YOUR_USER_ID’)

```
    # 画像のURL(後でRenderにアップロードした画像URLに変更します)
    image_url = os.environ.get('AI_IMAGE_URL', 'https://i.imgur.com/u5n4AAu.png')
    
    fortune_message = get_daily_fortune()
    
    # 画像とテキストを送信
    messages = [
        ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        ),
        TextSendMessage(text=fortune_message)
    ]
    
    line_bot_api.push_message(user_id, messages)
    
    return 'Fortune sent!', 200
except Exception as e:
    print(f"Error: {e}")
    return 'Error', 500
```

# LINEからのメッセージ受信用

@app.route(”/callback”, methods=[‘POST’])
def callback():
signature = request.headers[‘X-Line-Signature’]
body = request.get_data(as_text=True)

```
try:
    handler.handle(body, signature)
except InvalidSignatureError:
    abort(400)

return 'OK'
```

# メッセージに反応

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
“”“ユーザーからメッセージが来た時の処理”””
text = event.message.text

```
if '占い' in text or '運勢' in text:
    # 画像のURL
    image_url = os.environ.get('AI_IMAGE_URL', 'https://i.imgur.com/u5n4AAu.png')
    
    fortune = get_daily_fortune()
    
    # 画像とテキストを返信
    messages = [
        ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        ),
        TextSendMessage(text=fortune)
    ]
    
    line_bot_api.reply_message(event.reply_token, messages)
else:
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="「占い」って送ってくれたら今日の運勢教えるで〜!✨")
    )
```

if **name** == “**main**”:
port = int(os.environ.get(“PORT”, 5000))
app.run(host=“0.0.0.0”, port=port)
