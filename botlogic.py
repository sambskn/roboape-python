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
						#Make a Watson Call
						print('watson process started')
						#here I told the thing to look at max 400 msgs from the user
						#watson docs say you hit max accuracy with ~3000 words 
						#so i chose 400 as a guess assuming that will get us kinda in the range of 3000
						msgs = retrieval.getMessages(data['user_id'], 400)
						print(msgs)
						prepared = prepareForWatson(msgs)
						print('output prepared for watson')
						print('prepared data')
						print(prepared)
						watsonresults = getWatsonPersonalityData(prepared)
						output = []
						#add needs response
						outputAddition = "ROBO APE HAS DETERMINED YOU HAVE THE FOLLOWING NEEDS:\n"
						for need in watsonresults['needs']:
							if (need['percentile']>=0.60):
								outputAddition = outputAddition + need['name'] + '\n'
						output.append(outputAddition)
						#add personality traits
						outputAddition = "ROBO APE HAS DETERMINED YOU HAVE THE FOLLOWING VALUES:\n"
						for value in watsonresults['values']:
							if (value['percentile']>=0.50):
								outputAddition = outputAddition + value['name'] + '\n'
						output.append(outputAddition)
						#lets do each of the "big 5"
						for big5Trait in watsonresults['personality']:
							outputAddition = "ROBO APE HAS LOOKED AT YOUR TRAIT: '" + big5Trait['name'] + "' AND HAS DETERMINED IT HAS THE FOLLOWING CHARACTERISTICS: \n"
							addedChild = 0
							for child in big5Trait['children']:
								if (child['percentile']>=0.50):
									outputAddition = outputAddition + child['name'] + '\n'
									addedChild = 1
							if(addedChild==1):
								output.append(outputAddition)
							
						return random.choice(output)
					if template['special']=="markov":
						msgs = retrieval.getMessages(data['user_id'], 400)
						output = generateMarkovMsg(msgs)
						print(output)
						return output

def generateMarkovMsg(msgs):
	"""
	makes a basic markov chain and returns a generated msg
	"""
	initial = []
	terminal = []
	chain = {}

	for msg in msgs:
		words = msg['text'].split(' ')
		for word in words:
			#check if terminal
			if words.index(word)==(len(words)-1):
				terminal.append(word)
			else:
				#check if initial
				if words.index(word)==0:
					initial.append(word)
				if(word in chain):
					if chain[word] is not None:
						chain[word] = chain[word].append(words[words.index(word)+1])
					else:
						chain[word] = [words[words.index(word)+1]]
				else:
					chain[word] = [words[words.index(word)+1]] 
	print(initial)			
	print(terminal)
	print(chain)
	output = ""
	word = random.choice(initial)
	print("starting word is: " + word)
	while word not in terminal:
		output = output + " " + word
		print(output)
		print(chain[word])
		word = random.choice(chain[word])
	#if it is in terminal, check if it has anything else in the chain
	#this just doesn't really work ugh
	output =  output + " " + word

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
