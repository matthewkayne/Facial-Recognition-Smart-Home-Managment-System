import cv2
import os
import glob
import smtplib
import asyncio
import requests
import numpy as np
import tkinter as tk
from tkinter import *
from kasa import SmartBulb
import face_recognition
from dotenv import load_dotenv
from PIL import Image, ImageTk
import database # Imports from local database.py file

load_dotenv() # Gets secrets from .env
EMAIL = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
BULB_IP = os.getenv('BULB_IP')


video_capture = cv2.VideoCapture(0) # Get a reference to webcam #0 (the default one)

known_face_encodings = []
known_face_names = []
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'known_people/')

list_of_files = [f for f in glob.glob(path+'*.jpg')] # Make an array of all the saved jpg files' paths

number_files = len(list_of_files) # Find number of known faces

names = list_of_files.copy()

for i in range(number_files):
    globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
    globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
    known_face_encodings.append(globals()['image_encoding_{}'.format(i)])

    names[i] = names[i].replace("known_people/", "")
    known_face_names.append(names[i])

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
name = None
in_name = None
in_pass = None
temp_name = None
entryName = None
entryPass = None
entryEmail = None
top = None
settingsPage = None
userId = None
logInName = None
logInPass = None

def run():
    global process_this_frame
    global name

    ret, frame = video_capture.read() # Grab a single frame of video
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # Resize frame of video to 1/4 size for faster face recognition processing
    
    rgb_small_frame = small_frame[:, :, ::-1] # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding) # See if the face is a match for the known face(s)

            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index] # Creates and cleans up the name of the matching image
                name = name.replace("known_people"," ")
                name = name.replace(".jpg"," ")
                name = name.replace("/Users/matthewkayne/Documents/School/A-Levels/Computer Science/Project/Code/","")
                
                text_box.delete(1.0, "end-1c")
                text_box.insert("end-1c", name)


                return name
            
            face_names.append(name)
            
    process_this_frame = not process_this_frame

i=0


class Device:
  def __init__(self, deviceid, state):
    self.deviceid = deviceid
    self.state = state


def saveAccount():
    global in_name
    global in_pass
    
    in_name = entryName.get() # Gets the name inputted
    in_pass = entryPass.get() # Gets the password inputted
    in_email = entryEmail.get() # Gets the email inputted

    fileName = in_name.lower()
    fileName = fileName.replace(" ","-")
    fileName= fileName+'.jpg'

    database.addAccount(in_name,in_pass,in_email,fileName)

    os.rename(temp_name,('known_people/'+fileName))
    top.destroy()


def new_person():
    global temp_name
    global i
    global entryName
    global entryPass
    global entryEmail
    global top

    ret, frame = cap.read()

    temp_name='image'+str(i)+'.jpg'
    cv2.imwrite(temp_name, frame)
    i+=1

    top = Toplevel(window)
    top.title("Create Account")
    top.geometry("750x250")
    
    labelName = Label(top, text = "Name")
    entryName = Entry(top, width= 25) # Create an Entry Widget in the Toplevel window for name
    labelName.pack()
    entryName.pack()

    labelEmail = Label(top, text = "Email")
    entryEmail = Entry(top, width= 25) # Create an Entry Widget in the LogInPage window for email
    labelEmail.pack()
    entryEmail.pack()
    
    labelPass = Label(top, text = "Password")
    entryPass = Entry(top, width= 25) # Create an Entry Widget in the Toplevel window for password
    entryPass.config(show="*")
    labelPass.pack()
    entryPass.pack()
    
    button= Button(top, text="Ok", command=saveAccount) # Creates a Button Widget in the Toplevel Window
    button.pack(pady=5, side= TOP)
    
      
def storeLink(tempDeviceId,deviceState):
    database.cursor.execute("SELECT id from link WHERE userid = ? AND deviceid = ?",(userId,tempDeviceId))
    if not database.cursor.fetchall():  # An empty result evaluates to False.
        database.cursor.execute("""INSERT INTO link (userid, deviceid, state) VALUES (?, ?, ?)""",(userId,tempDeviceId,deviceState))
    else:
        database.cursor.execute("""UPDATE link SET state=? WHERE userid=? AND deviceid=?""",(deviceState,userId,tempDeviceId))
    database.connection.commit()
    

def sendData(recipientEmail,recipientData): # Sends email to email supplied in parameter
    gmail_user = EMAIL
    gmail_password = EMAIL_PASSWORD

    to = [recipientEmail]
    subject = 'Your Private Data'
    body = recipientData

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (gmail_user, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(gmail_user, to, email_text)
        smtp_server.close()
    except Exception as ex:
        print ("Something went wrong….",ex)

     
def settings():
    global settingsPage
    
    settingsPage = Toplevel(window)
    settingsPage.title("Settings")

    settingsPage.geometry("1000x1000")

    tempLabel = Label(settingsPage, text = "Settings Page")
    tempLabel.pack()
    
    light_1 = Device(1, BooleanVar())
    light_1.state.set(True)
    light_1CheckButton = Checkbutton(settingsPage, text = "Light On/Off", variable=light_1.state, command = lambda: storeLink(light_1.deviceid,light_1.state.get()))
    light_1CheckButton.pack()
    
    spotify = Device(2, BooleanVar())
    spotify.state.set(True)
    spotifyCheckButton = Checkbutton(settingsPage, text = "Spotify On/Off", variable=spotify.state, command = lambda: storeLink(spotify.deviceid,spotify.state.get()))
    spotifyCheckButton.pack()
    
    database.cursor.execute("SELECT email FROM accounts WHERE username = ? AND password = ?",(logInName.get(),logInPass.get()))
    email = database.cursor.fetchone()
    database.cursor.execute("SELECT * FROM accounts WHERE username = ? AND password = ?",(logInName.get(),logInPass.get(),))
    data = database.cursor.fetchall()

    dataButton = Button(settingsPage, text="Send My Private Data", command= lambda: [sendData(email[0],str(data))])
    dataButton.pack(pady=5, side = BOTTOM)
    
    confirmButton = Button(settingsPage, text="Confirm", command=settingsPage.destroy)
    confirmButton.pack(pady=5, side = BOTTOM)


def getUserId(userName):
    database.cursor.execute("SELECT id FROM accounts WHERE username=?",(userName,))
    return sum(database.cursor.fetchone())


def accountCheck(inName, inPass):
    global userId

    database.cursor.execute("SELECT username FROM accounts WHERE username = ? AND password = ?",(inName,inPass))
    if not database.cursor.fetchall():
        pass
    else:
        userId = getUserId(inName)
        settings()


def log_in():
    global logInName
    global logInPass

    logInPage = Toplevel(window)
    logInPage.title("Log In")
    logInPage.geometry("750x250")
    
    labelName = Label(logInPage, text = "Full Name")
    logInName = Entry(logInPage, width= 25) # Create an Entry Widget in the LogInPage window for name
    labelName.pack()
    logInName.pack()
    
    labelPass = Label(logInPage, text = "Password") # Create an Entry Widget in the LogInPage window for password
    logInPass= Entry(logInPage, width= 25)
    logInPass.config(show="*")
    labelPass.pack()
    logInPass.pack()
    
    button= Button(logInPage, text="Ok", command=lambda: [accountCheck(logInName.get(),logInPass.get()),logInPage.destroy()]) # Creates a Button Widget in the LogInPage Window
    button.pack(pady=5, side= TOP)


def faceControl():
    light_1APIClass = SmartBulb(BULB_IP)

    if name == None:
        pass
    else:
        database.cursor.execute("SELECT COUNT(*) FROM link")
        db = sum(database.cursor.fetchone())


        for x in range(db):
                database.cursor.execute("SELECT id FROM accounts WHERE filename = ?",((name+".jpg").replace(" ",""),))
                fcUserId = sum(database.cursor.fetchone())
                database.cursor.execute("SELECT deviceid FROM link WHERE userid = ? AND id= ?",(fcUserId,x+1,))
                fcDeviceId = sum(database.cursor.fetchone())
                database.cursor.execute("SELECT devicename FROM devices WHERE id = ?",(fcDeviceId,))
                fcDeviceName = database.cursor.fetchone()[0]
                database.cursor.execute("SELECT state FROM link WHERE userid = ? AND deviceId = ?",(fcUserId,fcDeviceId))
                fcState = sum(database.cursor.fetchone())

                if fcState == 0:
                    fcStateString = "_off"
                else:
                    fcStateString = "_on"
                    
                if fcDeviceId == 1 and fcState == 1:
                    asyncio.run(light_1APIClass.turn_on())
                    print("Light On")
                if fcDeviceId == 1 and fcState == 0:
                    asyncio.run(light_1APIClass.turn_off())
                    print("Light Off")
                else:
                    requests.post("https://maker.ifttt.com/trigger/"+fcDeviceName+fcStateString+"/with/key/fZQacqZEzguEOUTC2dSECFBo0xcNEk4ofpmJJoy2yIg")
                
window = tk.Tk() # Sets up GUI
window.title("A-Level-Project")
window.geometry("1000x1000")

window.bind('<Escape>', lambda e: window.quit()) # Allows the esc key to be used to close the GUI

text_box = tk.Text(window, width = 25, height = 10, font=("Helvetica", 15))
text_box.grid(row = 30, column = 200)
text_box.insert("end-1c", " ")

who_btn = tk.Button(window,text="Who am I?", height = 2, width = 10, command=lambda: [run(), faceControl()])
who_btn.grid(row = 300, column = 90)

new_btn = tk.Button(window,text="New Person?", height = 2, width = 10, command=new_person)
new_btn.grid(row = 300, column = 250)

login_btn = tk.Button(window,text="Log In", height = 2, width = 10, command=log_in)
login_btn.grid(row = 300, column = 300)

label = Label(window, width=450, height=450)
label.grid(row=140, column=190)

cap = cv2.VideoCapture(0)

def show_frames(): # Define function to show frame

    cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB) # Get the latest frame and convert into Image
    img = Image.fromarray(cv2image)
    
    imgtk = ImageTk.PhotoImage(image = img) # Convert image to PhotoImage

    label.imgtk = imgtk
    label.configure(image=imgtk)
    
    label.after(20, show_frames) # Repeat after an interval to capture continiously

show_frames() # Function to show the GUI and video frame
tk.mainloop()