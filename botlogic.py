import os
import json
import random
from watson_developer_cloud import PersonalityInsightsV3
import retrieval
from collections import Counter

def getResponse(data):
	#see groupme API for details about data JSON object
	with open('chatBank.json') as json_data:
		chatBank = json.load(json_data)
	message = data['text']
	for template in chatBank['templates']:
		for keyword in template['keywords']:
			if keyword in message.lower():
				#check if we are doing something special
				if template['special'] is None:
					potentialResponses = template['responses']
					if random.uniform(0, 1)<template['frequency'][0]:
						return random.choice(potentialResponses)
				else:
					if template['special'] == 'personality':
						#TODO Make a watson call here
						print('watson process started')
						msgs = retrieval.getAllMessages(data['user_id'])
						prepared = prepareForWatson(msgs)
						print('output prepared for watson')
						watsonresults = getWatsonPersonalityData(prepared)
						print(watsonresults)
						return 'ooh yeah lets see them results'
					return template['special']

def prepareForWatson(msgs):
	"""
	preparing suitable data to be sent to the Watson API
	reccomended amount for maxium precison is 3000 words
	"""
	MAX_WORDS = 3000
	output= []
	wordCount = 0
	wordsInMsg = 0
	for msg in msgs:
		if wordCount<3000:
			wordsInMsg = Counter(msg['text'].split())
			output.append(msg['txt'])
			wordCount += wordsInMsg
		else:
			break
		
	output = ''.join(output)
	return output

def getWatsonPersonalityData(input):
	psycheval = PersonalityInsightsV3(
		version='2016-10-20',
		username=os.getenv('WATSON_PERSON_USERNAME'),
		password=os.getenv('WATSON_PERSON_PASSWORD')
	)
	return psycheval.profile(input)


	