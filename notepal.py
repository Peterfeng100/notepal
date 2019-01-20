from flask import Flask
from flask_assistant import Assistant, ask, tell, event
from picture import captureImage
from makePDF import makePDF
import cv2
import time
import requests
import json
import os
import subprocess
import signal

currPage = 1
currName = "Default"
currProc = None
currStatus = "READY"
currDir = None

#start of flask app
app = Flask(__name__)

assist = Assistant(app, '/')

@assist.action("Default Welcome Intent")
def default():
	return ask("Hi, I am notepal!")

@assist.action("startNote", mapping={'name': 'name'})
def startNote(name):
	global currName
	global currProc
	global currStatus
	global currDir
	
	if currStatus != "READY":
		return tell("Your note " + str(currName) + " has already been started!")
	
	currStatus = "STARTED"
	currName = name
	name = name.replace(" ","")
	filepath = "Notes/" + name
	
	counter = 1
	while os.path.exists("%s/Note%d"%(filepath,counter)):
		counter += 1
	directory = "%s/Note%d"%(filepath,counter)

	if not os.path.exists(directory):
		os.makedirs(directory)
	currDir = directory

	recordName = os.path.join(directory,"record1.wav")
	proc_args = ['arecord', '-D' , 'plughw:1,0' , '-c 2' , '-r' , '16' , '-f' , 'S16_LE' , recordName]
	rec_proc = subprocess.Popen(proc_args, shell=False, preexec_fn=os.setsid)
	print("startRecordingArecord()> rec_proc pid= " + str(rec_proc.pid))
	print("startRecordingArecord()> recording started")
	currProc = rec_proc
	
	return ask("Your note for " + str(currName) + " has been started.")
	
@assist.action("newPage")
def newPage():
	global currPage
	global currProc
	global currStatus
	global currDir
	
	if currStatus != "STARTED":
		return tell("OK, I know you weren't the brightest, but I was hoping you would know to start a new note before turning to the next page.")

	captureImage("%s/image%d"%(currDir,currPage))
	os.killpg(currProc.pid, signal.SIGTERM)
	currProc.terminate()
	currProc = None
	print("stopRecordingArecord()> Recording stopped")
	time.sleep(1)
	currPage += 1
	recordName = os.path.join(currDir,"record%d.wav"%(currPage))
	proc_args = ['arecord', '-D' , 'plughw:1,0' , '-c 2' , '-r' , '16' , '-f' , 'S16_LE' , recordName]
	rec_proc = subprocess.Popen(proc_args, shell=False, preexec_fn=os.setsid)
	print("startRecordingArecord()> rec_proc pid= " + str(rec_proc.pid))
	print("startRecordingArecord()> recording started")
	currProc = rec_proc
	return ask("Ok, you are now on page " + str(currPage) + ".")

@assist.action("endNote")
def endNote():
	global currName
	global currPage
	global currProc
	global currStatus
	global currDir

	if currStatus != "STARTED":
		return tell("OK, I know you weren't the brightest, but I was hoping you would know to start a new note before ending it.")
	
	captureImage("%s/image%d"%(currDir,currPage))
	os.killpg(currProc.pid, signal.SIGTERM)
	currProc.terminate()
	currProc = None
	print("stopRecordingArecord()> Recording stopped")
	
	for fname in sorted(os.listdir(currDir)):
		if fname.endswith(".wav"):
			py_args = ['python', 'SpeechToText.py' , '--filename' , os.path.join(currDir,fname)]
			subprocess.Popen(py_args)
	
	temp = currPage
	currPage = 1
	currStatus = "READY"
	currDir = None
	
	return tell("Ok, your note for " + currName + " with " + str(temp) + " sections is now completed. I am now preparing this note for export.")

@assist.action("exportNote")
def exportNote():
	global currName
	
	for dir in sorted(os.listdir("Notes")):
		makePDF("Notes/" + dir, currName)
	
	for pdfs in sorted(os.listdir("PDFs")):
		if pdfs.endswith(".pdf"):
			py_args = ['python', 'gdrive.py' , '--filename' , os.path.join("PDFs", pdfs)]
			subprocess.Popen(py_args)
			
	return tell("All notes have been updated and exported!")
	
if __name__ == "__main__":
	if not os.path.exists("Notes"):
		os.makedirs("Notes")
	if not os.path.exists("PDFs"):
		os.makedirs("PDFs")
	app.run(debug=True)


