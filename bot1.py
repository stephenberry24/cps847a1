import slack
import os
import requests, json

from pathlib import Path
from dotenv import load_dotenv
# Import Flask
from flask import Flask, request, Response
# Handles events from Slack
from slackeventsapi import SlackEventAdapter

# Load the Token from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
# Configure your flask application
app = Flask(__name__)

# Configure SlackEventAdapter to handle events
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

# Using WebClient in slack, there are other clients built-in as well !!
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

# connect the bot to the channel in Slack Channel
# client.chat_postMessage(channel='#general', text='Bot Connected')

# Get Bot ID
BOT_ID = client.api_call("auth.test")['user_id']

@app.route('/')
def hello():
    return 'up'



# handling Message Events
@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text2 = event.get('text')
    if BOT_ID !=user_id:
        client.chat_postMessage(channel=channel_id, text=text2)

@ app.route('/weather', methods=['POST'])
def message_count():
    data = request.form
    channel_id = "#"+str(data.get('channel_name'))
    city = data.get('text')
    URL = "http://api.openweathermap.org/data/2.5/weather?q="+ city + "&&units=metric&&appid=b1670369ce3f1f0b71e762a85c4040d2"
    returnData = city + " Weather: " + str(round(requests.get(URL).json()["main"]["temp"])) + " °C"
    client.chat_postMessage(channel=channel_id, text=returnData)
    return Response(), 200




# Run the webserver micro-service
if __name__ == "__main__":
    app.run(debug=True)