import os
import json
import requests
import datetime

URL = 'https://api.groupme.com/v3'
TOKEN = os.getenv('GROUPME_TOKEN')
BOT_ID = os.getenv('GROUPME_BOT_ID')

def getGroupMembers():
	"""
    returns data from groupme API with all members of the group the bot is in
	"""
	params = {'per_page' : 100}
	bots = get(requests.get(URL + '/bots' + TOKEN, params=params))
	groupid = 0
    for bot in bots:
        if bot['bot_id']==BOT_ID:
            groupid = bot['group_id']
    
    if groupid==0
        return
    
    return get(requests.get(URL+ '/groups/:'+ groupid + TOKEN, params=params))['members']

def getMessagesForUser(name):
    members = getGroupMembers()
    userID = 0
    for member in members:
        if name in member['nickname']:
            userID = member['user_id']

def getNumFavorited(msg):
	"""Counts the number of favorites the mssage received."""
	num_favorited = msg['favorited_by']
	return len(num_favorited)



def countMsgs(group_name, group_id):
	"""
	Function that calls GroupMe API and processes messages of a particular group.

	Params:
	group_id: group_id of group
	csv_file: name of output csv file
	processTextFunc: a function that processes a msg and returns a value that is appended to user data
	sinceTs: only process messages after this timestamp
	"""
	totalCount = getGroupCount(group_id, direct_msgs)
	print ("Counting messages for {} (Total: {})".format(group_name, totalCount))
	curCount = 0
	users = {}
	lastMsgId = str(int(getLastMsgId(group_id, direct_msgs))+1) # get current msg as well
	while (curCount < totalCount):
		if curCount % 100 == 0:
			print (curCount)
		msgs = getMessages(group_id, direct_msgs, lastMsgId)
		if not msgs:
			break
		if direct_msgs:
			msgs = msgs['direct_messages']
		else:
			msgs = msgs['messages']
		for msg in msgs:
			#make sure that sinceTs is not == None
			if sinceTs!=None:
				if msg['created_at'] < sinceTs:
					return curCount, users
			curCount += 1
			try:
				created_at = datetime.datetime.fromtimestamp(msg['created_at']).strftime('%Y-%m-%d %H:%M:%S')
			except:
				print ("Error parsing created_at")
				created_at = ""
			user = msg['name']
			user_id = msg['user_id']
			text = msg['text']
			attachments = msg['attachments']
			likes = getNumFavorited(msg)

		lastMsgId = msgs[-1]['id']
	if csv_file:
		f.close()
	return users

