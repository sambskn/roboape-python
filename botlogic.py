import os
import json
import random

def getResponse(data):
	#see groupme API for details about data JSON object
	with open('chatBank.json') as json_data:
		chatBank = json.load(json_data)
	message = data['text']
	print(chatBank)
	for template in chatBank['templates']:
		print(template)
		for keyword in template['keywords']:
			if keyword in message:
				potentialResponses = template['responses']
				return random.choice(potentialResponses)

	if "roboape" in message:
		return "lol idk fam"
