# Imports all the needed libraries
import face_recognition, cv2, os, glob, sqlite3
import numpy as np
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import database


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Make array of sample pictures with encodings
known_face_encodings = []
known_face_names = []
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'known_people/')

# Make an array of all the saved jpg files' paths
list_of_files = [f for f in glob.glob(path+'*.jpg')]

# Find number of known faces
number_files = len(list_of_files)

names = list_of_files.copy()

for i in range(number_files):
    globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
    globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
    known_face_encodings.append(globals()['image_encoding_{}'.format(i)])

    # Creates array of known names
    names[i] = names[i].replace("known_people/", "")  
    known_face_names.append(names[i])

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
previous_name = None 
name=None

def run():
    global process_this_frame
    global previous_name
    global name

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:

            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:

                # Creates and cleans up the name of the matching image
                name = known_face_names[best_match_index]
                name = name.replace("known_people"," ")
                name = name.replace(".jpg"," ") 
                name = name.replace("/Users/matthewkayne/Documents/School/A-Levels/Computer Science/Project/Code/","")               

                # Returns the name on the GUI
                text_box.delete(1.0, "end-1c")
                text_box.insert("end-1c", name)

                return name
                
            face_names.append(name)
            
   
    process_this_frame = not process_this_frame

i=0

def printValue():
    global in_name
    global in_pass

    # Gets the name inputted
    in_name = entryName.get()
    in_pass = entryPass.get()

    fileName = in_name.lower()
    fileName = fileName.replace(" ","-")
    fileName= fileName+'.jpg'

    database.addAccount(in_name,in_pass,fileName)

    os.rename(temp_name,('known_people/'+fileName))
    top.destroy()

def new_person():
    global temp_name
    global i
    global entryName
    global entryPass
    global top

    ret, frame = cap.read()

    
    temp_name='image'+str(i)+'.jpg'
    cv2.imwrite(temp_name, frame)
    i+=1


    top = Toplevel(window)
    top.geometry("750x250")

    # Create an Entry Widget in the Toplevel window for name
    labelName = Label(top, text = "Name")
    entryName = Entry(top, width= 25)
    labelName.pack()
    entryName.pack()

    # Create an Entry Widget in the Toplevel window for password
    labelPass = Label(top, text = "Password")
    entryPass = Entry(top, width= 25)
    labelPass.pack()
    entryPass.pack()

    # Creates a Button Widget in the Toplevel Window
    button= Button(top, text="Ok", command=printValue)
    button.pack(pady=5, side= TOP)




# Sets up GUI    
window = tk.Tk()
window.geometry("1000x1000")

# Allows the esc key to be used to close the GUI
window.bind('<Escape>', lambda e: window.quit())

# Creates all the widgets on the GUI
text_box = tk.Text(window, width = 25, height = 10, font=("Helvetica", 15))
text_box.grid(row = 30, column = 200)
text_box.insert("end-1c", " ")

who_btn = tk.Button(window,text="Who am I?", height = 2, width = 10, command=run)
who_btn.grid(row = 300, column = 90)

new_btn = tk.Button(window,text="New Person?", height = 2, width = 10, command=new_person)
new_btn.grid(row = 300, column = 250)

label = Label(window, width=450, height=450)
label.grid(row=140, column=190)

cap = cv2.VideoCapture(0)

# Define function to show frame
def show_frames():
    global i

    # Get the latest frame and convert into Image
    cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)

    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image = img)

    label.imgtk = imgtk
    label.configure(image=imgtk)

    # Repeat after an interval to capture continiously
    label.after(20, show_frames)

# Function to show the GUI and video frame
show_frames()
tk.mainloop()