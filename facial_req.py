# -*- coding: utf-8 -*-
#! /usr/bin/python
# import the necessary packages
import face_recognition, imutils, pickle, time, cv2, os, numpy as np, threading, sys
from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager
from imutils.video import VideoStream, FPS
from datetime import datetime
from worker import abort_all_thread
# tuz tanıma app fonksiyonlar
from train_model import run_train, run_train_pro, run_haritalar
from ses_kaydi import ses_kaydi_al, ses_dosyalarini_sil
from ses_to_yazi import ses_to_yazi_fonk

class thread_with_trace(threading.Thread):
  def __init__(self, *args, **keywords):
    threading.Thread.__init__(self, *args, **keywords)
    self.killed = False

  def start(self):
    self.__run_backup = self.run
    self.run = self.__run      
    threading.Thread.start(self)

  def __run(self):
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup

  def globaltrace(self, frame, event, arg):
    if event == 'call':
      return self.localtrace
    else:
      return None

  def localtrace(self, frame, event, arg):
    if self.killed:
      if event == 'line':
        raise SystemExit()
    return self.localtrace

  def kill(self):
    self.killed = True





def yuz_tani():

	if not os.access("dataset/_kimler/", os.W_OK):
		os.mkdir("dataset/_kimler/")	
	# yeni yuz algılandığında kaydedilecek yer
	kimler = os.getcwd() + "/dataset/_kimler/"
	# hassiyet oranı resimler ile uyuşmasının ayarı olsun
	hassasiyet_oran = 0.49
	#Initialize 'currentname' to trigger only when a new person is identified.
	currentname = "Unknown"
	#Determine faces from encodings.pickle file model created from train_model.py
	encodingsP = "/encodings.pickle"
	# load the known faces and embeddings along with OpenCV's Haar
	print("[INFO] loading encodings + face detector... " + os.getcwd() +encodingsP)
	# cascade for face detection
	data = pickle.loads(open(os.getcwd() +encodingsP, "rb").read())
	# initialize the video stream and allow the camera sensor to warm up
	# Set the ser to the followng
	# src = 0 : for the build in single web cam, could be your laptop webcam
	# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
	vs = VideoStream(src=0,framerate=10).start()

	
	
	# start the FPS counter
	fps = FPS().start()
	sayac, bos = 0, 0
	mesaj = "Yüz tanıma başladı"
	mesaj = "start."

	f1 = threading.Thread(target=ses_kaydi_al)
	f1.start()

	f2 = threading.Thread(target=ses_to_yazi_fonk)
	f2.start()



	global frame
	global suret_var

	def fotograf_cek_step():
		print("[auto] yüz algılandı 5 saniyede bir toplam 5 foto çelilecek")
		fotocek = 0
		while fotocek < 5:
			if suret_var:
				fotograf_cek()
				fotocek += 1
				print("[auto] foto çelildi 5 /", fotocek)
				time.sleep(5)
		print("[auto] otomatik foto kapandı.")
			


	def fotograf_cek():
		if suret_var:
			file_name = kimler + datetime.now().strftime('%Y-%m-%d_%H-%M-%S.jpg' ) 
			cv2.imwrite(file_name, frame)
			lst = os.listdir("dataset/_kimler/")
			print("[INFO] kimler klasöründeki fotoğraf sayısı.", len(lst))

	

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
	resim_var = 0
	name_new_sayac = 0
	foto_cek_sayac = 0
	name = "Unknown"
	name_new = "Unknown"



	pipeline_out = "appsrc ! videoconvert ! video/x-raw, framerate=20/1, format=RGBA ! glimagesink sync=false"
	fourcc = cv2.VideoWriter_fourcc(*'H264')

	stream_out = cv2.VideoWriter(pipeline_out, cv2.CAP_GSTREAMER, fourcc, 20.0, (1280,720))


	yuz_casc=cv2.CascadeClassifier("classifier/haarcascade_frontalface_default.xml")
		
	goz_casc=cv2.CascadeClassifier("classifier/haarcascade_eye.xml")


	bulunan_kisiler, bulunan_kisiler_final  = [], []


	def zoom(frame, zoom_factor=2):
		return cv2.resize(frame, None, fx=zoom_factor, fy=zoom_factor)
	writer = None
	while True:
		suret_var = False

		# grab the frame from the threaded video stream and resize it
		# to 500px (to speedup processing)
		frame = vs.read()

		stream_out.write(frame)

		frame = imutils.resize(frame, width=900)
		# Detect the fce boxes
		boxes = face_recognition.face_locations(frame, model="VGG-Face")
		boxes = face_recognition.face_locations(frame, model="detection_method")
		# compute the facial embeddings for each face bounding box
		encodings = face_recognition.face_encodings(frame, boxes)
		names = []
		# loop over the facial embeddings
		iki_say = 0, 0
		if encodings:
			resim_var += 1
		# auto foto çekimi
		if writer is None and "output.avi" is not None:
			fourcc = cv2.VideoWriter_fourcc(*'MJPG')
			writer = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480), True)
		if writer is not None:
			writer.write(frame)
		# loop over the recognized faces



		# göz algılama
		griTon=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		yuzler=yuz_casc.detectMultiScale(griTon,1.3,5)
		gozler=goz_casc.detectMultiScale(griTon,1.3,5)

		for (x,y,w,h) in yuzler:
			if len(yuzler)>0 and len(gozler)>0 :
				suret_var = False
				file_name = kimler + datetime.now().strftime('%Y-%m-%d_%H-%M-%S.jpg' ) 
				file_name_zoom = kimler + "zoom_"+datetime.now().strftime('%Y-%m-%d_%H-%M-%S.jpg' ) 
				file_name_kesinlestirilmis = kimler + "Konst_keskin"+datetime.now().strftime('%Y-%m-%d_%H-%M-%S.jpg' ) 

				cropped = frame[x:y, w:h]
				#zoomed = zoom(frame, 3)
				#zoomed_and_cropped = zoom(cropped, 3)
				zo = (-50,50 )# zoom_oran

            	#cv2.rectangle(frame, (x-100,y-100), ( (x+100) + (w) ,y+h+100), (0, 250, 250) ,5) # test kısmı sarı
				face = frame[  (y-100) : (y) + (h) + 100,     (x)-100 : (x) + (w)  + 100]  # (x,y,w,h) 


				if face.any():
					# Keskinlestirme cekirdegi olusturalim.
					kernel = np.array ( [[-1,-1,-1],	[-1, 9,-1],	[-1,-1,-1] ])
					# Keskinlestirme filtresi uygulayalm.
					sharpened_image = cv2.filter2D(face, -1, kernel)
					# Kontrast artirma islemi yapalim.Alpha degeri yükseldikçe kontrast degeri artar.
					alpha = 1.5
					sharpened_image = cv2.convertScaleAbs (sharpened_image, alpha=alpha)
					# Görüntüyü kaydedip,açalim.
					cv2.imwrite(file_name_kesinlestirilmis, sharpened_image)
					cv2.imwrite(file_name_zoom, face)
					cv2.waitKey(1)
					#cv2.imwrite(file_name, frame)
					print("[INFO] Foto çekildi")

			#cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3) # SURETİ YEŞİL ÇERÇEVE YAPIYOR
			roi_griTon=griTon[y:y+h,x:x+w]
			roi_renkli=frame[y:y+h,x:x+w]
			gozler=goz_casc.detectMultiScale(roi_griTon)
			if len( gozler ) > 0:
				suret_var = True
				for (ex,ey,ew,eh) in gozler:
					
					cv2.rectangle(roi_renkli,(ex,ey),(ex+ew,ey+eh),(0,0,255),3)
					cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3) # SURETİ YEŞİL ÇERÇEVE YAPIYOR




		
		

		for encoding in encodings:
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"],
				encoding)
			#if face is not recognized, then print Unknown
			#cv2.putText(frame, mesaj, (5, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
			frame = print_utf8_text(frame,(5, 30),mesaj, (255,255,255)) # Türkçe karakterler
			# check to see if we have found a match
			counts = {}
			sayac += 1
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
				hassasiyet = round(counts[name] / len(matchedIdxs),1 )
				name_new_sayac += 1
				if  hassasiyet > hassasiyet_oran and len(matchedIdxs) > 2:
					name_new = max(counts, key=counts.get)
				else:
					if hassasiyet < 0.3 and counts[name] <2:
						#print(hassasiyet , counts[name] )
						name_new = "Unknown"
						#print("Fotograf için  Tanımsız Yüz algılandı:", "hassasiyet:", hassasiyet,  "cont.names:", counts[name],  "len.matchedIdxs :", len(matchedIdxs), "name_new:",name_new, "counts:", counts, matchedIdxs)
				#print("counts:",counts, "name:", name, "sayac", sayac)
				#If someone in your dataset is identified, print their name on the screen
				if currentname != name_new:
					currentname = name_new
					#print(currentname, name, names, counts)
				suret_var = True
				#print("[INFO] yüz tespit edildi")
			else:
				suret_var = False
				#name_new = "Unknown"
				#print("Tanımsız Yüz algılandı:", "hassasiyet:", hassasiyet,  "cont.names:", counts[name],  "len.matchedIdxs :", len(matchedIdxs), "name_new:",name_new, "counts:", counts, matchedIdxs)

			if  len(boxes) == 1 and name_new == "Unknown" and sayac > 20 and len(matchedIdxs) > 3:
				#print("Tanımsız Yüz algılandı:", "hassasiyet:", hassasiyet,  "cont.names:", counts[name],  "len.matchedIdxs :", len(matchedIdxs), "name_new:",name_new, "counts:", counts, matchedIdxs)
				# fotograf_cek() # düzelt
				#run_train() kapatıldı test
				data = pickle.loads(open(os.getcwd()+encodingsP, "rb").read())
				sayac = 0	
			# update the list of names
			if name_new_sayac >8:
				name_new_sayac = 0

			names.append(name_new)
			#print(hassasiyet, len(matchedIdxs), len(boxes), name_new, counts, matchedIdxs)
			if foto_cek_sayac > 0 :
				f4 = threading.Thread(target=fotograf_cek_step)
				f4.start()
				foto_cek_sayac -= 1

		#cv2.waitKey(1) 
		# loop over the recognized faces
		#suret_var = False

		key = cv2.waitKey(1) & 0xFF

		if key  == ord("f"):
			foto_cek_sayac += 1
			print("[İNFO] Otomatik foto aktif.")
		
		if key  == ord("k"):
			lst = os.listdir("dataset/_kimler/")
			for row in lst:
				print("[INFO] Silindi "+ kimler+row)
				os.remove(kimler+row)

		if key == ord("l"): # data bilgileri load
			print("[İNFO] Yüz haritaları taranacak.")
			bulunan_kisiler = ["", "", "", "", "", "", "", "", "", "", ""]
			bulunan_kisiler_final = ["", "", "", "", "", "", "", "", "", "", ""]
			run_train() 
			run_train_pro()
			run_haritalar()
			data = pickle.loads(open(os.getcwd()+encodingsP, "rb").read())
		# quit when 'q' key is pressed
		if key == ord("ç"):
			print("[İNFO] Uygulamadan çıkış yapıldı.")
			break
		
		if not bulunan_kisiler:
			bulunan_kisiler = ["", "", "", "", "", "", "", "", "", "", ""]
			bulunan_kisiler_final = ["", "", "", "", "", "", "", "", "", "", ""]

		
		for ((top, right, bottom, left), name) in zip(boxes, names):
			# ulunan kişileri listelemek için
			# (x,y,w,h

			if len(bulunan_kisiler) == 10:
					bulunan_kisiler.remove(bulunan_kisiler[0])
					bulunan_kisiler_final.remove(bulunan_kisiler[0])

			if name != bulunan_kisiler[-1]:
				bulunan_kisiler.append(name )
				bulunan_kisiler_final.append(str(datetime.now().strftime("%H:%M")) + " " + name )
				
			for i in range(0, 10):
				if len(bulunan_kisiler) > i:
					pass
					#print(bulunan_kisiler[i], i)
					#mesaj =  str(datetime.now().strftime("%H:%M")) + " - " + name 
			

			# draw the predicted face name on the image - color is in BGR
			cv2.rectangle(frame, (left, top), (right, bottom),
				(0, 255, 225), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				.8, (0, 255, 255), 2)
			



			
			
		

		#cv2.getTextSize(text, font, font_scale, thickness)
		korr = (10, 100, 30)

		'''
			enum HersheyFonts = {
				FONT_HERSHEY_SIMPLEX        = 0, //!< normal size sans-serif font
				FONT_HERSHEY_PLAIN          = 1, //!< small size sans-serif font
				FONT_HERSHEY_DUPLEX         = 2, //!< normal size sans-serif font (more complex than FONT_HERSHEY_SIMPLEX)
				FONT_HERSHEY_COMPLEX        = 3, //!< normal size serif font
				FONT_HERSHEY_TRIPLEX        = 4, //!< normal size serif font (more complex than FONT_HERSHEY_COMPLEX)
				FONT_HERSHEY_COMPLEX_SMALL  = 5, //!< smaller version of FONT_HERSHEY_COMPLEX
				FONT_HERSHEY_SCRIPT_SIMPLEX = 6, //!< hand-writing style font
				FONT_HERSHEY_SCRIPT_COMPLEX = 7, //!< more complex variant of FONT_HERSHEY_SCRIPT_SIMPLEX
				FONT_ITALIC                 = 16 //!< flag for italic font
		};
		https://stackoverflow.com/questions/25931692/how-to-print-a-text-to-a-frame-in-opencv-python
		'''
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame,  bulunan_kisiler_final[-10], (korr[0] , korr[1] +( korr[2] * 1) ), font, 0.8, (0, 255, 255), 2, cv2.LINE_AA) 
		cv2.putText(frame,  bulunan_kisiler_final[-9], (korr[0] , korr[1] + (korr[2] * 2)), font, 0.8, (0, 255, 255), 2, cv2.LINE_AA) 
		cv2.putText(frame,  bulunan_kisiler_final[-8], (korr[0] , korr[1] + (korr[2] * 3)), font, 0.8, (0, 255, 255), 2, cv2.LINE_AA) 
		cv2.putText(frame,  bulunan_kisiler_final[-7], (korr[0] , korr[1] + (korr[2] * 4) ), font, 0.8, (0, 255, 255), 2, cv2.LINE_AA) 
		cv2.putText(frame,  bulunan_kisiler_final[-6], (korr[0] , korr[1] + (korr[2]*5) ), font, 0.8, (0, 255, 255), 2, cv2.LINE_AA) 
		cv2.putText(frame,  bulunan_kisiler_final[-5], (korr[0] , korr[1] + (korr[2] * 6) ), font, 0.8, (0, 255, 255), 2, cv2.LINE_AA) 
		cv2.putText(frame,  bulunan_kisiler_final[-4], (korr[0] , korr[1] + (korr[2]*7)), font, 0.8, (0, 255, 255), 2, cv2.LINE_AA) 
		cv2.putText(frame,  bulunan_kisiler_final[-3], (korr[0] , korr[1] + (korr[2]*8)), font, 0.8, (0, 255, 255), 2, cv2.LINE_AA) 
		cv2.putText(frame,  bulunan_kisiler_final[-2], (korr[0] , korr[1] + (korr[2]*9)), font, 0.8, (0, 255, 255), 2, cv2.LINE_AA) 
		cv2.putText(frame,  bulunan_kisiler_final[-1], (korr[0] , korr[1] + (korr[2]*10)), font, 0.8, (0, 255, 255), 2, cv2.LINE_AA) 

		# display the image to our screen
		cv2.imshow("Facial Recognition is Running", frame)
		# update the FPS counter
		fps.update()


	#  thread to stop
	abort_all_thread()
	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
	# do a bit of cleanup	
	cv2.destroyAllWindows()
	vs.stop()
	writer.release()
	stream_out.release()


run_train()
run_train_pro()
run_haritalar()
ses_dosyalarini_sil()
yuz_tani()

