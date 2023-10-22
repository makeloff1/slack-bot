#
# Bolt App
#
import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from flask import Flask

logging.basicConfig(level=logging.DEBUG)

# app = App(token=os.environ["SLACK_BOT_TOKEN"])
bot_token = "xoxb-811268029777-6071567405539-eqQejM44eAdC2LbIBapwdV69"
app = App(token=bot_token)

#
# Socket Mode
#
app_token = "xapp-1-A062SF7EGAC-6069648164662-44a6307085f83d0eec811f841d46ed9015fddc6fa0bb7c629b675d4ba70a8e0a"
# handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
handler = SocketModeHandler(app, app_token)
# Use connect() method as start() blocks the current thread
handler.connect()

# なぜかショートカットがエラー


# Add middleware / listeners here
@app.command("/hi")
def hello(body, ack):
    user_id = body["user_id"]
    ack(f"Hi <@{user_id}>!")


@app.event("app_mention")
def mention_handler(body, say):
    mention = body["event"]

    # ここがJiraへ起票される内容

    text = mention["text"]
    channel = mention["channel"]
    thread_ts = mention["ts"]
    say(text=text, channel=channel, thread_ts=thread_ts)


#
# Web App
#
flask_app = Flask(__name__)

# You won't use the Flask adapter as all the event requests are handled by
# the above Socket Mode connection
# from slack_bolt.adapter.flask import SlackRequestHandler
# handler = SlackRequestHandler(app)


@flask_app.route("/", methods=["GET"])
def index():
    return "Hello World"


# You can run this app by the following command:
# gunicorn --bind :3000 --workers 1 --threads 2 --timeout 0 app:flask_app
