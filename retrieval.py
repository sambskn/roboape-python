import os
import json
import requests

from dotenv import load_dotenv
load_dotenv()

URL = 'https://api.groupme.com/v3'
TOKEN = '?token=' + os.getenv('GROUPME_TOKEN')
BOT_ID = os.getenv('GROUPME_BOT_ID')

def get(response):
	"""Get the resposne portion of the JSON object"""
	status = response.status_code
	if status != 200:
		print('Error retrieving response')
		return None
	return response.json()['response']

def getGroupMembers():
	"""get list of members in the group the bot is asscoiated with"""
	group_id = getGroupID()
	group = get(requests.get(URL + '/groups/:' + group_id + TOKEN))
	return group['members']

def getUserIDForUser(name):
    """
    This fucntion, given a name will look up the associated userID
    """
    members = getGroupMembers()
    userID = 0
    for member in members:
        if name == member['nickname']:
            userID = member['user_id']

    return userID


def getGroupID():
	"""returns the group ID associated with the bot"""
	bots = get(requests.get(URL + '/bots' + TOKEN))
	groupid = 0
	for bot in bots:
		if bot['bot_id'] == BOT_ID:
			groupid = bot['group_id']
			return groupid
	return 0


def getNumFavorited(msg):
	"""Counts the number of favorites the mssage received."""
	num_favorited = msg['favorited_by']
	return len(num_favorited)

def getMessages(user_ID=None, maxMsgs=None):
	"""
	this will return a list of msg dicts, 
	with the optional check to only get ones matching the given user_id
	and the optional max number of messages to receive
	(to avoid timeout use the max number of messages option)
	"""
	group_id = getGroupID()
	group = get(requests.get(URL + '/groups/' + group_id + TOKEN))
	totalCount = group['messages']['count']
	before_id = group['messages']['last_message_id'] #might need a '-1' here
	output = []
	params = {
		'before_id': before_id,
		'limit': 100
	}
	count = 0
	userMsgCount = 0
	if maxMsgs is None:
		maxMsgs = 100000
		#i picked that number arbitrarily
		#let me know if that was a problem
	msgs = get(requests.get(URL + '/groups/' + group_id + '/messages' + TOKEN, params=params))['messages']
	if msgs is None:
		return output
	while count < totalCount and userMsgCount < maxMsgs:
		for msg in msgs:
			if user_ID is None:
				output.append(msg)
				output.append(' ')
			else:
				if msg['user_id'] == user_ID:
					output.append(msg)
					userMsgCount += 1
			count += 1
			before_id = msg['id']
		#before_id = int(before_id) - 100
		params = {
			'before_id': before_id,
			'limit': 100
		}
		result = get(requests.get(URL + '/groups/' + group_id + '/messages' + TOKEN, params=params))
		if result is None:
			return output
		msgs = result['messages']
	return output