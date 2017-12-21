# roboape-python

This is a simple bot written in Python3 that will post messages to a GroupMe group. For each message posted in the group the bot is assgined to, the bot will parse the message, compare it to keywords in it's message bank, then randomly select on of theassoicited responses form it's message bank. It will also check the frequency value associted with the keyword, and as a result will only post the response with some regularity relating to frequency. 

Right now there's a bunch of dumb jokes that probably only make sense to my college ultiamte frisbee team in the json file containing the message bank, but you could customize it.

I've also implemented functionality to have the responses have a "special" field where specific acitons other than the standard random response could be enacted (see the Watson Functionality below).

## Make your Own ROBOAPE
In order to make this bot your own, first make an account at dev.groupme.com.
Next, you'll want to hos the bot somewhere, I use heroku.
On dev.groupme.com you'll want to create a bot for a group, with your project's heroku URL as the callback URL.
Then you'll have to modify the config variables on heroku to have the GROUPME_BOT_ID variable, set to the value GroupMe provides.
Then feel free to screw around with the message bank and personalize it to have your own terrible bot.

## Message Bank Format
The message bank is a big json file with an array called 'templates'. Each entry in the array has an array of string triggers that will be checked against in the source message called 'keywords'. Then there is an array of possible response strings called 'responses'. The 'frequency' value is a float between 0 and 1 that determines the chance that the bot will actually send it's response to the group. The 'special' string should be null unless you want to implement special functionality for a certain response

## Watson Functionality
Currently the bot will query the Watson Personality Insights service, feeding it all the messages the user has posted in the given group, then randomly selecting from the siginicant repsonses something to send back to the chat. It's pretty neat. To make it work you'll need to put your Watson login info into the environemnt variables as WATSON_PERSON_USERNAME and WATSON_PERSON_PASSWORD


