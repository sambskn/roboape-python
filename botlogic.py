import os
import json
import random
from collections import Counter
from watson_developer_cloud import PersonalityInsightsV3
import retrieval

def getResponse(data):
	#see groupme API for details about dat JSON object
	with open('chatBank.json') as json_data:
		chatBank =json.load(json_data)
	message = data['text']
	for template in chatBank['templates']:
		for keyword in template['keywords']:
			if keyword in message.lower():
				#check if it has a special tag
				if template['special'] is None:
					potentialResponses = template['responses']
					if random.uniform(0, 1)<template['frequency'][0]:
						return random.choice(potentialResponses)
				else:
					if template['special'] == 'personality':
						#TODO Make a Watson Call
						print('watson process started')
						msgs = retrieval.getAllMessages(data['user_id'])
						prepared = prepareForWatson(msgs)
						print('output prepared for watson')
						print('prepared data')
						print(prepared)
						watsonresults = getWatsonPersonalityData(prepared)
						print(watsonresults)
						
						#watson results looking good
						output = "ROBO APE HAS DETERMINED YOU HAVE THE FOLLOWING NEEDS:\n"
						for need in watsonresults['needs']:
							if (need['percentile']>=0.60):
								output = output + need['name'] + '\n'
							
						return output



					

def prepareForWatson(msgs):
	"""
	prepare suitable data to be sent to Watson for analysis
	reccomended amount for precision is ~3000 words
	probably not all fromt he same source but oh well
	"""
	MAX_WORDS = 3000
	output = []
	wordCount = 0
	wordsInMsg = 0
	for msg in msgs:
		if wordCount<3000:
			wordsInMsg = len(msg['text'].split())
			output.append(msg['text'] + " ")
			wordCount += wordsInMsg
		else:
			break
	output = ''.join(output)
	return output

def getWatsonPersonalityData(input):
	psycheval = PersonalityInsightsV3(
		version = '2016-10-20',
		username = os.getenv('WATSON_PERSON_USERNAME'),
		password = os.getenv('WATSON_PERSON_PASSWORD') 
	)
	return psycheval.profile(input)
