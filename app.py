import os
import json
import botlogic

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()

  # We don't want to reply to ourselves!
	if data['name'] != 'ROBO APE':
	
	#figure out what to send here
	print("recieved msg " + msg)
	msg = botlogic.getResponse(data)
	send_message(msg)

	return "ok", 200

def send_message(msg):
	url  = 'https://api.groupme.com/v3/bots/post'

	data = {
		'bot_id' : os.getenv('GROUPME_BOT_ID'),
		'text'   : msg,
	}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()
  
def log(msg):
	print(str(msg))
	sys.stdout.flush()