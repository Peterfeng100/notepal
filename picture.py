import cv2
import time

def captureImage(name):
	cam = cv2.VideoCapture(0)
	cam.set(3, 2304)
	cam.set(4, 1536)
	time.sleep(0.5)
	ret, frame = cam.read()
	if not ret:
		return
	img_name = name + ".jpg"
	cv2.imwrite(img_name, frame)
	print("{} written!".format(img_name))
	cam.release()
	#consider autocropping here

if __name__ == "__main__":
	print ("initialized")
	while True:
		k = raw_input("Input command: ")
		if k == 't':
			print("Capturing")
			captureImage("test")
		elif k == 'e':
			print("Exiting")
			break

