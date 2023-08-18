from flask import Flask, render_template, request
import os
import pandas as pd
import datetime
import time
import cv2
import numpy as np
import csv
from PIL import Image, ImageTk
from random import randint
from only_morse import Morse
import sqlite3

con = sqlite3.connect('userinfo.db')
cr = con.cursor()
cr.execute('create table if not exists user(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT, mpassword TEXT)')

app = Flask(__name__)

@app.route('/')
def index():
   return render_template("index.html")

@app.route('/home')
def home():
   return render_template("index.html")

@app.route('/signup')
def signup():
   return render_template("signup.html")

@app.route('/password')
def password():
   return render_template("password.html")

@app.route('/userhome')
def userhome():
   return render_template("userhome.html")

@app.route('/logout')
def logout():
   return render_template("index.html")

@app.route('/create_datsets',  methods=['POST','GET'])
def create_datsets():
   if request.method == 'POST':
      con = sqlite3.connect('userinfo.db')
      cr = con.cursor()

      cr.execute('SELECT id FROM user ORDER BY id DESC LIMIT 1')
      Id = cr.fetchall()
      print(Id)
      
      Name = request.form['Name']
      password = str(request.form['password'])
      mpassword = str(request.form['mpassword'])

##      if Id is None:
      if len(Id) == 0:
         Id = '1'
      else:
         Id = str(Id[0][0]+1)

      print(Id+' '+Name+' '+password+' '+mpassword)
      
      cam = cv2.VideoCapture(0)
      harcascadePath = "haarcascade_frontalface_default.xml"
      detector=cv2.CascadeClassifier(harcascadePath)
      sampleNum=0
      while True:
         ret, img = cam.read()
         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
         faces = detector.detectMultiScale(gray, 1.3, 5)
         for (x,y,w,h) in faces:
               cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
               #incrementing sample number 
               sampleNum=sampleNum+1
               #saving the captured face in the dataset folder TrainingImage
               cv2.imwrite("datasets/"+Name +"."+Id +'.'+ str(sampleNum) + ".png", gray[y:y+h,x:x+w])
               #display the frame
         cv2.imshow('frame',img)
         #wait for 100 miliseconds 
         if cv2.waitKey(1) & 0xFF == ord('q'):
               break
         # break if the sample number is morethan 100
         elif sampleNum>100:
               break
      cam.release()
      cv2.destroyAllWindows() 
      msg = "Images Saved for ID : " + Id +" Name : "+ Name 
      row = [Name, password, mpassword]

      cr.execute('insert into user (name, password, mpassword) values(?,?,?)', row)
      con.commit()

      return render_template("signup.html", msg=msg)
   return render_template("index.html")

@app.route('/training')
def training():
   def getImagesAndLabels(path):
      #get the path of all the files in the folder
      imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
      #print(imagePaths)
      
      #create empth face list
      faces=[]
      #create empty ID list
      Ids=[]
      #now looping through all the image paths and loading the Ids and the images
      for imagePath in imagePaths:
         #loading the image and converting it to gray scale
         pilImage=Image.open(imagePath).convert('L')
         #Now we are converting the PIL image into numpy array
         imageNp=np.array(pilImage,'uint8')
         #getting the Id from the image
         Id=int(os.path.split(imagePath)[-1].split(".")[1])
         # extract the face from the training image sample
         faces.append(imageNp)
         Ids.append(Id)        
      return faces,Ids
   #recognizer=cv2.face.LBPHFaceRecognizer_create()
   recognizer=cv2.face_LBPHFaceRecognizer.create()
   #recognizer = cv2.createLBPHFaceRecognizer()
   harcascadePath = "haarcascade_frontalface_default.xml"
   detector =cv2.CascadeClassifier(harcascadePath)
   faces,Id = getImagesAndLabels("datasets")
   recognizer.train(faces, np.array(Id))
   recognizer.save("Trainner.yml")
   msg = "Datsets trained successfully"
 
   return render_template("signup.html", msg=msg)

@app.route('/recognition')
def recognition():
   con = sqlite3.connect('userinfo.db')
   cr = con.cursor()
   #recognizer=cv2.face.LBPHFaceRecognizer_create()
  # recognizer=cv2.face_LBPHFaceRecognizer.create()
   #recognizer = cv2.createLBPHFaceRecognizer()
   recognizer = cv2.face.LBPHFaceRecognizer_create()
   recognizer.read("Trainner.yml")
   harcascadePath = "haarcascade_frontalface_default.xml"
   faceCascade = cv2.CascadeClassifier(harcascadePath);    
   cam = cv2.VideoCapture(0)
   font = cv2.FONT_HERSHEY_SIMPLEX        
   now = datetime.datetime.now()
   count = 0
   List = []
   while True:
      ret, im =cam.read()
      gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
      faces=faceCascade.detectMultiScale(gray, 1.2,5)    
      
      for(x,y,w,h) in faces:
         Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
         Id = str(Id)
         print(Id)
         if(conf < 40):
            count += 1
            print(count)
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            cr.execute("select name from user where id = '"+Id+"'")
            Name = cr.fetchone()
            print(Name)
            Name = Name[0]
            List.append(Name)
            print(Name)
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            cv2.putText(im,'{}'.format(Name),(x, y-10), font, 1,(255,255,255),2)
         else:
            List.append('unknown')
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            cv2.putText(im,'unknown',(x, y-10), font, 1,(255,255,255),2)
            
      cv2.imshow('im',im)
      if cv2.waitKey(100) & count >= 20:
         break
   cam.release()
   cv2.destroyAllWindows()

   counter = 0
   num = List[0]

   for i in List:
      curr_frequency = List.count(i)
      if(curr_frequency> counter):
         counter = curr_frequency
         num = i

   if num == 'unknown':
      return render_template("signup.html", msg = 'Face mismatched')
   else:
      return render_template("signin.html", msg1 = 'Face matched')

@app.route('/morse_login',  methods=['POST','GET'])
def morse_login():
   if request.method == 'POST':
      con = sqlite3.connect('userinfo.db')
      cr = con.cursor()

      Name = request.form['Name']
      Password = request.form['password']
      print(Name, Password)
      cr.execute("select id from user where name = '"+Name+"' and password = '"+Password+"'")
      row = cr.fetchone()

##      if (row is None):
      if row:
         row = str(row[0])
         cr.execute("select mpassword from user where id = '"+row+"'")
         password = cr.fetchone()
         mor_pass = password[0]
         print(mor_pass)
         try:
            data = Morse(mor_pass)
            if data == 'match':   
               f = open('session.txt', 'w')
               f.write(row)
               f.close()
               return render_template("loged.html")
            else:
               return render_template("signup.html", msg = 'Morsecode unsuccessfull')
         except:
            return render_template("signup.html", msg = 'Somthing went wrong')
      else:
            return render_template("signup.html", msg='Entered wrong username or password')
   return render_template("index.html")


@app.route('/change_password',  methods=['POST','GET'])
def change_password():
   if request.method == 'POST':
      con = sqlite3.connect('userinfo.db')
      cr = con.cursor()

      f = open('session.txt', 'r')
      ID = f.read()
      f.close()

      newpassword = str(request.form['newpassword'])

      print(ID, newpassword)
      def random_with_N_digits(n):
          range_start = 10**(n-1)
          range_end = (10**n)-1
          return randint(range_start, range_end)
         
      OTP = str(random_with_N_digits(4))
      
      import telepot       
      bot = telepot.Bot("6184690831:AAGNuLwll-jHcyrJ20XQpPBP0tOISxcnsXc")
      bot.sendMessage("819762402", str(OTP))

      file1 = open("myfile.txt","w")
      file1.write(OTP+','+ID+','+newpassword)
      file1.close()
      
      cr.execute("update user set mpassword = '"+newpassword+"' where id = '"+ID+"' ")
      con.commit()

      return render_template("password.html", msg2='otp sent')
   return render_template("password.html")

@app.route('/confirm',  methods=['POST','GET'])
def confirm():
   if request.method == 'POST':
      con = sqlite3.connect('userinfo.db')
      cr = con.cursor()

      newotp = str(request.form['newotp'])
      file1 = open("myfile.txt","r")
      row=str(file1.read())
      row  = row.split(',')
      otp_old = row[0]
      ID = row[1]
      newpassword = row[2]
      file1.close()

      if otp_old == newotp:
         cr.execute("update user set mpassword = '"+newpassword+"' where id = '"+ID+"' ")
         con.commit()
         return render_template("password.html", msg='password successfully updated')
      else:
         return render_template("password.html", msg='entered wrong otp')
   return render_template("password.html")

if __name__ == "__main__":
   app.run(debug=True, use_reloader=False)
