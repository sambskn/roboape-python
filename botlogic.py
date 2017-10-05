import os
import json
import random

def getResponse(data):
	#see groupme API for details about data JSON object
	with open('chatBank.json') as json_data:
		chatBank = json.load(json_data)
	message = data['text']
	for template in chatBank['templates']:
		for keyword in template['keywords']:
			if keyword in message.lower():
				#check if we are doing something special
				print(template.keys())
				potentialResponses = template['responses']
				if random.uniform(0, 1)<template['frequency'][0]:
					return random.choice(potentialResponses)


