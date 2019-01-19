from flask import Flask
from flask_assistant import Assistant, ask, tell, event
from picture import captureImage
import cv2
import time
import requests
import json

currPage = 1
currName = "Default"

#POST function
def post(r):
	with open("/home/linaro/Desktop/image.jpg", "rb") as f:
		data = f.read()
		image = data.encode("base64")
		r = requests.post("http://34.201.113.132:3000/post_data", data={"img":image})
		return r

#start of flask app
app = Flask(__name__)

assist = Assistant(app, '/')

@assist.action("Default Welcome Intent")
def default():
	return ask("Hi, I am notepal!")

@assist.action("startNote", mapping={'name': 'name'})
def startNote(name):
	global currName
	currName = name
	#start recording
	return tell("Your note " + str(currName) + " has been started.")
	
@assist.action("newPage")
def newPage():
	global currPage
	#capture photo, stop recording, start new recording
	currPage += 1
	return tell("Ok, you are now on page " + str(currPage) + ".")

@assist.action("endNote")
def endNote():
	global currName
	global currPage
	temp = currPage
	currPage = 1
	#capture photo, stop recording
	#call speech to text APIs, upload text and images
	return tell("Ok, your note " + currName + " with " + str(temp) + " pages is now completed. It has been saved automatically and should be viewable in your account in a few minutes!")


if __name__ == "__main__":
	app.run(debug=True)


