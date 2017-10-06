import os
import json
import requests
import datetime

URL = 'https://api.groupme.com/v3'
TOKEN = os.getenv('GROUPME_TOKEN')
BOT_ID = os.getenv('GROUPME_BOT_ID')


def getGroupID():
    """Returns the group id asscoicated with the bot"""
    bots = get(requests.get(URL + '/bots' + TOKEN, params=params))
	groupid = 0
	for bot in bots:
		if bot['bot_id'] == BOT_ID:
			groupid = bot['group_id']
	return groupid


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


def getNumFavorited(msg):
	"""Counts the number of favorites the mssage received."""
	num_favorited = msg['favorited_by']
	return len(num_favorited)


def getAllMessages(user_ID=None):
    group_id = getGroupID()
	group = get(requests.get(URL + '/groups/' + group_id + TOKEN)
    totalCount=group['messages']['count']
    before_id=group['messages']['last_message_id']  # might need to add a -1
    output=[]
    params={'before_id': before_id, 'limit': 100}
	count=0
	msgs=get(requests.get(URL + '/groups/:' + group_id + \
	         '/messages' + TOKEN, params=params))
    while count < totalCount:
		for msg in msgs:
			if user_ID is None:
				output.append(msg)
			else:
				if msg['user_id'] == user_ID:
					output.append(msg)
			count += 1
		before_id=before_id - 100

		params={'before_id': before_id, 'limit': 100}
		msgs=get(requests.get(URL + '/groups/:' + group_id + \
		         '/messages' + TOKEN, params=params))
	return output
