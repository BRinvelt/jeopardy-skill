#    Mycroft Jeopardy Skill
#    Copyright (C) 2021  Ben Rinvelt
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from mycroft import MycroftSkill, intent_file_handler
import requests
import json

class JeopardySkill(MycroftSkill):

	def __init__(self):
		super(JeopardySkill, self).__init__(name="JeopardySkill")

	@intent_file_handler('Jeopardy.intent')
	def handle_jeopardy_question_intent(self,message):
		questionResponse = requests.get("https://jservice.io/api/random")#Get a random Jeopardy Question
		if(questionResponse.status_code != 200):#Ensure that the request was successful
			self.speak("Unable to access Jeopardy Questions at this moment, please try again later.")
			return
		questionDetails = json.loads(questionResponse.text)[0]#Load the response into a JSON for easy parsing
		category = questionDetails.get("category").get("title")
		value = str(questionDetails.get("value"))
		clue = questionDetails.get("question")
		answer = questionDetails.get("answer").lower()#Make the answer lowercase as mycroft always takes a users voice as lowercase

		self.speak_dialog('jeopardy-question',{"category":category,"value":value,"clue":clue},wait = True)
		guess = self.get_response()

		#Question answers are provided as the answer itself, ie "george washington" not "who is george washington"
		#This segment simply removes "who is " or "what is " from the users answer so they may provide
		if guess is not None:
			if "who is " in guess:
				guess = guess.split("who is ")[1]
			if "what is" in guess:
				guess = guess.split("what is ")[1]

		#Compare answer to user guess and let them know how they did
		if guess == answer:
			self.speak_dialog('jeopardy-correct-answer')
		else:
			self.speak_dialog('jeopardy-incorrect-answer',{"answer":answer})

def create_skill():
	return JeopardySkill()
