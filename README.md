# roboape-python

This is a simple bot written in Python3 that will post messages to a GroupMe group. For each message posted in the group the bot is assgined to, the bot will parse the message, compare it to keywords in it's message bank, then randomly select on of theassoicited responses form it's message bank. It will also check the frequency value associted with the keyword, and as a result will only post the response with some regularity relating to frequency. 

Right now theres a bunch of dumb jokes that probably only make sense to my college ultiamte frisbee team in the json file containing the message bank, but you could customize it.

In order to make this bot your own, first make an account at dev.groupme.com.
Next, you'll want to hos the bot somewhere, I use heroku.
On dev.groupme.com you'll want to create a bot for a group, with your project's heroku URL as the callback URL.
Then you'll have to modify the config variables on heroku to have the GROUPME_BOT_ID variable, set to the value GroupMe provides.
Then feel free to screw around with the message bank and personalize it to have your own terrible bot.



As a testement to it's functionality, many freshmen in our GroupMe are unaware if Robo Ape is a bot or just a really dumb human.
