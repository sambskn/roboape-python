import os
import json
import requests


URL = 'https://api.groupme.com/v3'
TOKEN = '?token=' + os.getenv('GROUPME_TOKEN')
BOT_ID = os.getenv('GROUPME_BOT_ID')

def get(response):
	"""Get the resposne portion of the JSON object"""
	print(response)
	if response.json()['meta']['code'] != 200:
		print('Error retrieving response')
		print(response.json())
		return
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

def getAllMessages(user_ID=None):
	"""
	this will return a list of msg dicts, 
	with the optional check to only get ones matching the given user_id
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
	msgs = get(requests.get(URL + '/groups/' + group_id + '/messages' + TOKEN, params=params))['messages']
	while count < totalCount:
		for msg in msgs:
			if user_ID is None:
				output.append(msg)
			else:
				if msg['user_id'] == user_ID:
					output.append(msg)
			count += 1
			before_id = msg['id']
		#before_id = int(before_id) - 100
		params = {
			'before_id': before_id,
			'limit': 100
		}
		msgs = get(requests.get(URL + '/groups/' + group_id + '/messages' + TOKEN, params=params))['messages']
	return output