import os
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import botlogic
from flask import Flask, request
import requests

from dotenv import load_dotenv
import json
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()

  # We don't want to reply to ourselves!
	if data['name'] != 'ROBO APE':

		#figure out what to send here
		msg = botlogic.getResponse(data)
		if msg:
			send_message(msg)

		return "ok", 200

def send_message(msg):
	url  = 'https://api.groupme.com/v3/bots/post'

	data = {
		'text'   : msg,
		'bot_id' : os.getenv('GROUPME_BOT_ID')
	}
	print(json.dumps(data))
	response = requests.post(url, params=data)
	log(response.text)
  
def log(msg):
	print(str(msg))
	sys.stdout.flush()