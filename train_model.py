# -*- coding: utf-8 -*-
#! /usr/bin/python

# import the necessary packages
from imutils import paths
import face_recognition
#import argparse
import pickle
import cv2
import os, re, json, time




remove_photo = 4


def encode_resimler():
	from simple_facerec import SimpleFacerec
	import os
	sfr = SimpleFacerec()
	sfr.load_encoding_images(os.getcwd() + "/dataset/")


def run_train():
	encodingsP = "/encodings.pickle"

	# our images are located in the dataset folder
	print("[INFO] start processing faces...")
	#print("paths.list_images(dataset):", os.getcwd())
	imagePaths = list(paths.list_images("dataset"))

	# initialize the list of known encodings and known names
	knownEncodings = []
	knownNames = []

	# loop over the image paths
	for (i, imagePath) in enumerate(imagePaths):
		# extract the person name from the image path
		print("[INFO] processing image {}/{}".format(i + 1,	len(imagePaths)))
		name = imagePath.split(os.path.sep)[-2]

		# load the input image and convert it from RGB (OpenCV ordering)
		# to dlib ordering (RGB)
		image = cv2.imread(imagePath)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# detect the (x, y)-coordinates of the bounding boxes
		# corresponding to each face in the input image
		boxes = face_recognition.face_locations(rgb,
			model="hog")

		# compute the facial embedding for the face
		encodings = face_recognition.face_encodings(rgb, boxes)

		# loop over the encodings
		for encoding in encodings:
			# add each encoding + name to our set of known names and
			# encodings
			knownEncodings.append(encoding)
			knownNames.append(name)

	# dump the facial encodings + names to disk
	print("[INFO] serializing encodings... " + os.getcwd()+"/encodings.pickle")
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open(os.getcwd()+"/encodings.pickle", "wb")
	f.write(pickle.dumps(data))
	data = pickle.loads(open(os.getcwd()+encodingsP, "rb").read())

	f.close()

def test():
	KNOWN_FACES_DIR =  os.getcwd() + "/dataset/"
	UNKNOWN_FACES_DIR =  os.getcwd() + "unknownFaces"
	TOLERANCE = 0.6
	FRAME_THICKNESS = 3
	FONT_THICKNESS = 2
	MODEL = "cnn"
	print("loading known faces…")
	known_faces = []
	known_names = []


	for name in os.listdir(KNOWN_FACES_DIR):
		print(name, re.search(".DS_Store", name))
		if not re.search(name, ".DS_Store"):
			dosyalar = os.listdir(f"{KNOWN_FACES_DIR}/{name}")
			if len(dosyalar) >0:
				for filename in dosyalar:
					image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
					encoding = face_recognition.face_encodings(image)
					
					if not len(encoding):
						print(filename, "can't be encoded", f"{KNOWN_FACES_DIR}/{name}/{filename}")
						continue
					known_faces.append(encoding)
					known_names.append(name)
				print("processing unknown faces...", f"{KNOWN_FACES_DIR}/{name}/{filename}")

def run_train_pro():


	filtre = ""


	print("[INFO] Başkalarına benziyen kayıtlar taranıyor.")

	silinen = 0
	klasor_ad_kontrol = ""


	encodingsP = "/encodings.pickle"

	currentname = "Unknown"

	data = pickle.loads(open(os.getcwd() +encodingsP, "rb").read())

	imagePaths = list(paths.list_images("dataset"))


	# initialize the list of known encodings and known names
	knownEncodings = []
	knownNames = []

	match_filtre = []
	filtre = False


	# loop over the image paths
	for (i, imagePath) in enumerate(imagePaths):
		name = imagePath.split(os.path.sep)[-2]

		image = face_recognition.load_image_file(imagePath)
		
		encodings = face_recognition.face_encodings(image)
		names = []
		# loop over the facial embeddings
	

		for encoding in encodings:
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"],
				encoding)
			#if face is not recognized, then print Unknown
			#cv2.putText(frame, mesaj, (5, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
			# check to see if we have found a match
			counts = {}
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
					#print(i, data["names"])
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1
				# will select first entry in the dictionary)
				name = max(counts, key=counts.get)
				
				if currentname != name:
					currentname = name
					#print(currentname, name, names, counts)
				suret_var = True
				#print("[INFO] yüz tespit edildi")
				# update the list of names
				names.append(name)
				if filtre != name:	
					filtre = name
					filtre = True


				
				klasor_ad = imagePath.split("/")[1]
				resim_ad = imagePath.split("/")[2]


				
				
				if klasor_ad not in ["_Demiroren_personel", "_kimler"]:

				
					if klasor_ad != "Ersen_aslan":
						oran = round(len(counts) / counts[name], 1)
						#print(imagePath, oran, counts)

						match_filtre.append({"path":imagePath, "lenarr":len(matchedIdxs)})

						# klosördeki resim klosör adindan farklı birinin ise sil
						image_len = list(paths.list_images("dataset"+klasor_ad))
						if klasor_ad != name and len(image_len) > remove_photo :
							#print("bunlar başkalarına benziyor silinmeli:", imagePath, klasor_ad, name) 
							if os.path.isfile(imagePath):
								os.remove(imagePath)
								silinen += 1


	print("[INFO] BAŞKALARINA BENZEYEN SİLENEN KAYIT SAYISI", silinen)


	print("incelecek Haritalar:", len(match_filtre))
	with open(os.getcwd()+"/incelencek_haritalar.json", 'w', encoding='utf-8') as f:
		json.dump(match_filtre, f, ensure_ascii=False, indent=4)




		
def run_haritalar():




	imagePaths = list(paths.list_images("dataset"))
	yuzprogramı = cv2.CascadeClassifier("classifier/haarcascade_frontalface_default.xml")

	for row in imagePaths:
			

		resim = cv2.imread(row) #resmimizi belirtme
		
		griresim = cv2.cvtColor(resim,cv2.COLOR_BGR2GRAY)#resmimizi griye donuştürme
		
		program = yuzprogramı.detectMultiScale(griresim,1.3,3)#programı çalıştırma (taranacak resim,büyütme oranı,kontrol sayısı)

		for (a,b,c,d) in program :
			cv2.rectangle(resim,(a,b),(a+c,b+d),(255,0,0),2) #burada bulduğumuz insan yüzlerini kare içide alma işlemini yapıyoruz
			#(yüzlerin gösterileceği resim,(köşe ayarlama)(köşe ayarlama),(karenin rengi),karenin kalınlığı)
		'''
		cv2.imshow("kapatmak için herhangi bir tuşa basınız",resim) #resmin son halini gösterme
    
		cv2.waitKey(0)
		cv2.destroyAllWindows() #herhangi bir tuşa basınca kapatmak için

		'''
		if len(program) == 0:
			#cv2.imshow("kapatmak için herhangi bir tuşa basınız",resim)
			#cv2.waitKey(0)
			#cv2.destroyAllWindows() #herhangi bir tuşa basınca kapatmak için
			os.remove(os.getcwd()+"/"+row)
			print("silindi")
		else:
			#cv2.imshow("kapatmak için herhangi bir tuşa basınız",resim)
			#cv2.waitKey(0)
			#cv2.destroyAllWindows() #herhangi bir tuşa basınca kapatmak için
			pass

		




	def extract_time(json): # json sıralama json sort
		try:
			return int(json['lenarr'])
		except KeyError:
			return 0

	with open(os.getcwd() +"/incelencek_haritalar.json") as f:
		data = json.load(f)
	
	 

    # ulkeinfo.sort(key=extract_time, reverse=True)
	
	aprt_kont, rows, sayac = [], [], 0
	for row in data: # {'path': 'dataset/ali_kilic/2025-02-22_09-52-06.jpg', 'lenarr': 23}


		if row["path"].split("/")[1] not in aprt_kont:
			aprt_kont.append(row["path"].split("/")[1])

	final_rows = []
	for p in aprt_kont:
		for row in data:
			if p == row["path"].split("/")[1]:
				rows.append(row)
		rows.sort(key=extract_time, reverse=True)
		final_rows.append(rows[:1])
		rows = []
	
	eniyi_resimler = []
	for rows in final_rows:
		for row in rows:
			eniyi_resimler.append(row["path"])
	

	imagePaths = list(paths.list_images("dataset"))

	for row in imagePaths: # {'path': 'dataset/ali_kilic/2025-02-22_09-52-06.jpg', 'lenarr': 23}
		if row.split("/")[1] != "ssali_kilic":

			if os.path.isfile(os.getcwd()+"/dataset/"+row.split("/")[1]+"/.DS_Store"):
				os.remove(os.getcwd()+"/dataset/"+row.split("/")[1]+"/.DS_Store")
				
			if row not in eniyi_resimler:
				image_len = os.listdir("dataset/"+row.split("/")[1])
				if os.path.isfile(os.getcwd()+"/"+row) and len(image_len) > remove_photo : # ['.DS_Store', '2025-02-17_10-39-13.jpg', '2025-02-22_10-41-36.jpg']
					os.remove(row)
					#print("silinecek:", row)
					print(row, len(image_len), os.getcwd()+"/"+row,     os.path.isfile(os.getcwd()+"/"+row))


				







#run_train()
#run_train_pro()
#run_haritalar()
