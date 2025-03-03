# -*- coding: utf-8 -*-
#! /usr/bin/python
# import the necessary packages
import face_recognition, imutils, pickle, time, cv2, os, numpy as np, threading
from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager
from imutils.video import VideoStream, FPS
from datetime import datetime
from train_model import run_train
from ses_kaydi import ses_kaydi_al
from ses_to_yazi import ses_to_yazi


kimler = os.getcwd() + "/dataset/_kimler/"
print("kimler:", kimler)

workdir = "dataset/_kimler/"
if not os.access(workdir, os.W_OK):
	os.mkdir(workdir)	


#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "Unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "/encodings.pickle"
# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector... " + os.getcwd() +encodingsP)
data = pickle.loads(open(os.getcwd() +encodingsP, "rb").read())
# initialize the video stream and allow the camera sensor to warm up
# Set the ser to the followng
# src = 0 : for the build in single web cam, could be your laptop webcam
# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop

run_train() # yuz bilgilerini haritala
time.sleep(1.0)

vs = VideoStream(src=0,framerate=10).start()
#vs = VideoStream(usePiCamera=True).start()
# start the FPS counter
fps = FPS().start()
sayac, bos = 0, 0
mesaj = "Yüz tanıma başladı"


f1 = threading.Thread(target=ses_kaydi_al)
#f2 = threading.Thread(target=ses_to_yazi)
f1.start()
#f2.start()

def print_utf8_text(image, xy, text, color):  # utf-8 karakterleri
	fontName = 'FreeSerif.ttf'  # 'FreeSansBold.ttf' # 'FreeMono.ttf' 'FreeSerifBold.ttf'
	
	fontName = font_manager.findfont('Helvetica Neue')
	font = ImageFont.truetype(fontName, 24)  # font seçimi
	img_pil = Image.fromarray(image)  # imajı pillow moduna dönüştür
	draw = ImageDraw.Draw(img_pil)  # imajı hazırla
	draw.text((xy[0],xy[1]), text, font=font,
              fill=(color[0], color[1], color[2], 0))  # b,g,r,a
	image = np.array(img_pil)  # imajı cv2 moduna çevir (numpy.array())
	return image
# loop over frames from the video file stream
while True:

	# grab the frame from the threaded video stream and resize it
	# to 500px (to speedup processing)
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	# Detect the fce boxes
	boxes = face_recognition.face_locations(frame)
	# compute the facial embeddings for each face bounding box
	encodings = face_recognition.face_encodings(frame, boxes)
	names = []
	# loop over the facial embeddings
	sayac = sayac + 1
	

	for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown" #if face is not recognized, then print Unknown
		#cv2.putText(frame, mesaj, (5, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
		frame = print_utf8_text(frame,(5, 30),mesaj, (255,255,255)) # Türkçe karakterler
		# check to see if we have found a match

		
			
		if True in matches:
			

			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}
			#print("matchedIdxs", matchedIdxs)
			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1
			# determine the recognized face with the largest number
			# of votes (note: in the event of an unlikely tie Python
			# will select first entry in the dictionary)
			name = max(counts, key=counts.get)
			print("counts:",counts, "name:", name, "sayac", sayac)
			#If someone in your dataset is identified, print their name on the screen
			if currentname != name:
				currentname = name
				sayac = 0
				print(currentname, name, names)
			
		# update the list of names
		names.append(name)

		


	if sayac > 20 and len(boxes) == 1 and name == "Unknown":
		#names = []
		file_name = kimler + datetime.now().strftime('%Y-%m-%d_%H-%M-%S.jpg' ) 
		mesaj = "Tanımsız Yüz algılandı. Foto çekiliyor."
		frame = print_utf8_text(frame,(5, 30),mesaj, (255,255,255)) # Türkçe karakterler
		cv2.imwrite(file_name,frame)
		print("fotoğraf çekildi:", file_name)
		cv2.waitKey(2000)
		mesaj = "Fotoğraf haritaları güncelleniyor."
		frame = print_utf8_text(frame,(5, 30),mesaj, (255,255,255)) # Türkçe karakterler
		run_train()
		data = pickle.loads(open(os.getcwd()+encodingsP, "rb").read())
		sayac = 0	

	# loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		# draw the predicted face name on the image - color is in BGR
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 225), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			.8, (0, 255, 255), 2)

	# display the image to our screen
	cv2.imshow("Facial Recognition is Running", frame)
	key = cv2.waitKey(1) & 0xFF

	# quit when 'q' key is pressed
	if key == ord("q"):
		break

	# update the FPS counter
	fps.update()




# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
