# importing libraries

import cv2
from tkinter import messagebox
from facepplib import FacePP, exceptions
from tkinter import filedialog
import os, os.path, shutil


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

def System():
    root.destroy()

    import cv2

    from facepplib import FacePP
    from playsound import playsound
    import pygame
    import tkinter
    from tkinter import messagebox
    ROOT = tkinter.Tk()
    LABEL = tkinter.Label(ROOT, text="")
    LABEL.pack()
    LOOP_ACTIVE = True

    facepp = FacePP(api_key='s8mLxoLyPGBB5TiH_LWMB9dUg2s2nJvz',
                    api_secret='Qp-MZSPEGff8uwic7qRGdh1SX5khvY6t')

    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video file")

    # Read until video is completed
    happy = True
    happy1 = False
    sad = True
    sad1 = False
    count = 0
    c = 0
    trig=0
    while cap.isOpened():

        # Capture frame-by-frame

        ret, frame = cap.read()
        if ret:

            # Display the resulting frame
            cv2.imwrite("frame.jpg", frame)

            image = facepp.image.get(image_file="frame.jpg",
                                     return_attributes=["gender", "age", "smiling", "headpose", "facequality", "blur",
                                                        "eyestatus", "emotion", "ethnicity"])
            num_faces = len(image.faces)
            emotion = image.faces[0].emotion
            eye = image.faces[0].eyestatus
            left_eye = eye["left_eye_status"]
            right_eye = eye["right_eye_status"]
            # conditions
            if left_eye["no_glass_eye_close"] and right_eye["no_glass_eye_close"] >= 98.00:
                count += 1
                print(count)
                playsound('venv/alarm.wav')
                if count == 3:

                    import requests

                    import os.path

                    ERROR_API = "Error during API call"
                    ERROR_FILE = "The specified file does not exist"
                    URL = 'https://api.smsmode.com/http/1.6/'
                    PATH_SEND_SMS = "sendSMS.do"
                    PATH_SEND_SMS_BATCH = "sendSMSBatch.do"

                    final_url = URL + PATH_SEND_SMS
                    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                    payload = {
                        #
                        'accessToken': "VPnKiGaDui7Ujkz0paVZbP0iqPif07Kj",
                        'message': "Drive Sleep Alert . Regards: DA System ",
                        'numero': +923123808376
                        # 'emetteur': emetteur,
                        # 'stop': option_stop
                    }
                    r = requests.post(final_url, data=payload, headers=headers)
                    if not r:
                        print("Wrong")

            if emotion["happiness"] >= 97.0 and (happy or happy1):
                trig=True
                pygame.init()
                pygame.mixer.init()
                song = f'venv/music/happy.mp3'
                print("playing")
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                happy = False
                happy1 = True

            if emotion["surprise"] >= 70.0 and (sad or sad1):
                trig = True
                pygame.init()
                pygame.mixer.init()
                song = f'venv/music/sad.mp3'
                print("playing")
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                sad = False
                sad1 = True
            if trig:
                c+=1
                print(c)
            if c==20:
                ROOT.update()
                answer = messagebox.askyesno("Ask Question", "Do you want to continue music ? ")
                print(answer)
                if answer:
                    c = 0
                    trig=False
                    continue

                else:
                    c = 0
                    trig = False
                    pygame.mixer.music.stop()

                    continue


            # image.image_id
            # '8g2nrvINBnpyFseprStfyA=='
            cv2.putText(frame, "Num of Face" + str(num_faces), (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,
                        cv2.LINE_4)
            cv2.putText(frame, "Angre" + str(emotion["anger"]), (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2,
                        cv2.LINE_4)
            cv2.putText(frame, "disgust" + str(emotion["disgust"]), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 255),
                        2, cv2.LINE_4)
            cv2.putText(frame, "fear" + str(emotion["fear"]), (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2,
                        cv2.LINE_4)
            cv2.putText(frame, "happiness" + str(emotion["happiness"]), (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 255), 2, cv2.LINE_4)
            cv2.putText(frame, "neutral" + str(emotion["neutral"]), (50, 220), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 255),
                        2, cv2.LINE_4)
            cv2.putText(frame, "sadness" + str(emotion["sadness"]), (50, 260), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 255),
                        2, cv2.LINE_4)
            cv2.putText(frame, "surprise" + str(emotion["surprise"]), (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 255),
                        2, cv2.LINE_4)
            cv2.putText(frame, "LefteyeOpen" + str(left_eye["no_glass_eye_open"]), (50, 350), cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 0), 2, cv2.LINE_4)
            cv2.putText(frame, "LefteyeClose" + str(left_eye["no_glass_eye_close"]), (50, 400),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 0), 2, cv2.LINE_4)
            cv2.putText(frame, "RighteyeOpen" + str(right_eye["no_glass_eye_open"]), (50, 450),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 0), 2, cv2.LINE_4)
            cv2.putText(frame, "RighteyeClose" + str(right_eye["no_glass_eye_close"]), (50, 500),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 0), 2, cv2.LINE_4)

            cv2.imshow('Frame', frame)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release
    # the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()
    restart_program()

def login():
    # Python program for face
    # comparison
    folder = 'venv/database_folder'

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print("pp")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    import time
    import cv2

    # define global variables
    face_detection = ""
    faceset_initialize = ""
    face_search = ""
    face_landmarks = ""
    dense_facial_landmarks = ""
    face_attributes = ""
    face_comparing_localphoto = ""
    beauty_score_and_emotion_recognition = ""
    face_comparing_websitephoto = ""

    # define face comparing function
    def face_comparing(app, Image1, Image2):

        print()
        print('-' * 30)
        print('Comparing Photographs......')
        print('-' * 30)

        cmp_ = app.compare.get(image_file1=Image1,
                               image_file2=Image2)

        print('Photo1', '=', cmp_.image1)
        print('Photo2', '=', cmp_.image2)

        # Comparing Photos
        if cmp_.confidence > 70:
            r = 'Both photographs are of same person'

            print(r)
            r = 1

        else:
            r = 'Both photographs are of two different persons'

            print(r)
            r = 0
        return r

    # Driver Code
    if __name__ == '__main__':

        # api details
        api_key = 'yXLVF_QqYNuZc2xpS5VOKL2e9zqzWkn9'
        api_secret = 'mbm8Qp6jVApwgpow1eCWHwwjVpWIu1Hd'

        try:

            print("hell")

            # call api
            app_ = FacePP(api_key=api_key,
                          api_secret=api_secret)
            funcs = [
                face_detection,
                face_comparing_localphoto,
                face_comparing_websitephoto,
                faceset_initialize,
                face_search,
                face_landmarks,
                dense_facial_landmarks,
                face_attributes,
                beauty_score_and_emotion_recognition
            ]

            # Pair 1

            # Create a VideoCapture object and read from input file
            cap = cv2.VideoCapture(0)

            # Check if camera opened successfully
            if (cap.isOpened() == False):
                print("Error opening video file")
            count = 0
            # Read until video is completed
            label = 0
            import sqlite3

            conn = sqlite3.connect('image_db.db')
            cursor = conn.cursor()

            data = cursor.execute("""SELECT * FROM my_data""")

            c = 0
            for i in data.fetchall():
                m = i[2]
                #
                with open(f"venv/database_folder/{c}st.png", 'wb') as f:
                    f.write(m)
                    c += 1

            conn.commit()
            cursor.close()
            conn.close()

            ls = os.listdir('venv/database_folder')
            print(ls)
            for i in range(len(ls)):
                triger = True
                while triger:

                    # Capture frame-by-frame
                    ret, frame = cap.read()
                    if ret == True:

                        # Display the resulting frame
                        cv2.imwrite("framee.jpg", frame)
                        image2 = "framee.jpg"
                        image1 = "venv/database_folder/" + str(ls[i])
                        r = face_comparing(app_, image1, image2)
                        r = str(r)
                        if r == ("1"):
                            label = "Face Match Succesfully"
                            print("Face Match Succesfully")
                            cv2.putText(frame, str(label), (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,
                                        cv2.LINE_4)

                            cv2.imshow('Frame', frame)
                            time.sleep(10)
                            if cv2.waitKey(25) & 0xFF == ord('q'):
                                break
                            # Create a VideoCapture object and read from input file
                            System()



                        elif r == ("0"):
                            label = "Face Didn't Match"

                            print("Face Didn't Match")

                            triger = False

                # When everything done, release
                # the video capture object
            cap.release()

            # Closes all the frames
            cv2.destroyAllWindows()


        except exceptions.BaseFacePPError as e:
            print('Error:', e)
    print("Hello")

def show():
    p = password.get()
    s = Label(root, text="Your Password is: " + str(p))
    s.place(x=660, y=280)


def login_with_pass(user, pws):
    import tkinter
    user = user.get()
    pwd = pws.get()
    if str(user) == "admin" and str(pwd) == "admin":
        # importing libraries

        System()
    else:
        tkinter.messagebox.showerror(title="Incorrect Password", message="Please Enter a valid Password / UserName")


def browseFiles(text_entry, U):
    name = str(text_entry.get())
    print(name)
    U.destroy()

    open_file = filedialog.askopenfilenames(
        filetypes=[("image", ".jpeg"),
                   ("image", ".png"),
                   ("image", ".jpg"), ])  # returns a tuple with opened file's complete path
    path = str(open_file[0])
    print(path)
    import sqlite3
    conn = sqlite3.connect('image_db.db')
    cursor = conn.cursor()

    with open(path, 'rb') as f:
        data = f.read()
        print(data)

    cursor.execute("""INSERT INTO my_data (name,data) VALUES (?,?)""", (name, data,))

    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("showinfo", "Successfully added user to Database . ")


def user_name():
    U = Toplevel(root)
    U.geometry('200x200')
    Label(U, text="Please Enter Username").pack()
    text_entry = StringVar()
    en = Entry(U, width=25, textvariable=text_entry)
    en.pack()

    Button(U, text="Ok", command=lambda: browseFiles(text_entry, U)).pack()


def user_name_for_cam():
    U = Toplevel(root)
    U.geometry('200x200')
    Label(U, text="Please Enter Username").pack()
    text_entry = StringVar()
    en = Entry(U, width=25, textvariable=text_entry)
    en.pack()

    Button(U, text="Ok", command=lambda: add_user_cam(text_entry, U)).pack()


def add_user_cam(text_entry, U):
    name = str(text_entry.get())
    print(name)
    U.destroy()

    import cv2

    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0)
    while True:
        try:
            check, frame = webcam.read()
            print(check)  # prints true as long as the webcam is running
            print(frame)  # prints matrix values of each framecd
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'):
                cv2.imwrite('venv/access_photo/saved_img.jpg', img=frame)
                webcam.release()
                path = 'venv/access_photo/saved_img.jpg'
                print(path)
                import sqlite3
                conn = sqlite3.connect('image_db.db')
                cursor = conn.cursor()

                with open(path, 'rb') as f:
                    data = f.read()
                    print(data)

                cursor.execute("""INSERT INTO my_data (name,data) VALUES (?,?)""", (name, data,))

                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("showinfo", "Successfully added user to Database . ")
                cv2.destroyAllWindows()
                break
            elif key == ord('q'):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break


def create_db():
    import sqlite3
    conn = sqlite3.connect('image_db.db')

    cursor = conn.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS my_data(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT,data BLOB)
                    """)

    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Success", "Database Build successfully.")


if __name__ == '__main__':
    from tkinter import *

    from PIL import Image, ImageTk

    from tkinter import messagebox

    root = Tk()

    # Code to add widgets will go here...
    root.title("Driver Alert System")
    windowWidth = 1020
    windowHeight = 650
    print("Width", windowWidth, "Height", windowHeight)

    # Gets both half the screen width/height and window width/height
    x = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
    y = int(root.winfo_screenheight() / 2 - windowHeight / 2)

    # Positions the window in the center of the page.
    root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, x, y-30))

    i = cv2.imread("venv/back.png")
    img = cv2.resize(i, (windowWidth, windowHeight))
    cv2.imwrite("venv/back.png", img)

    bg = PhotoImage(file="venv/back.png")

    background_label = Label(root, image=bg)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    head = Label(root, text="Driver Alert System", bg="white", font=("Phosphate", 40))
    head.place(x=275, y=30)

    img = ImageTk.PhotoImage(Image.open("venv/icon.png"))
    # l3 = Label(, width=40, height=42)
    # l3.place(x=605, y=380)
    pre_rec = Button(root, image=img, text="  Login With Face  ", compound="left", font=('Verdana', 16), command=login)

    pre_rec.place(x=420, y=380)

    password = StringVar()
    username = StringVar()


    # Add an Entry widget for accepting User Password

    def on_entry_click(event):
        """function that gets called whenever entry is clicked"""
        if user.get() == 'Enter your user name...':
            user.delete(0, "end")  # delete all the text in the entry
            user.insert(0, '')  # Insert blank for user input
            user.config(fg='black')


    user = Entry(root, bd=1, width=25)
    #
    l2 = Label(root, text="UserName", font=('Verdana', 10)).place(x=330, y=221)
    user.insert(0, 'Enter your user name...')
    user.bind('<FocusIn>', on_entry_click)

    user.config(fg='grey')
    user.place(x=420, y=220)

    # user = Entry(root, width=25, textvariable=username)
    # user.insert(0,'Username')
    # user.pack(pady=10,padx=40,)
    pws = Entry(root, width=25, textvariable=password, bd=1, show="*")
    Label(root, text="Password", font=('Verdana', 10)).place(x=330, y=251)
    pws.place(x=420, y=250)

    Button(root, text="Login", bg="#2079EB", font=('Verdana', 12), command=lambda: login_with_pass(user, pws)).place(
        x=420, y=300)
    # # Add a Button to reveal the password
    Button(root, text="Show Password", command=show).place(x=660, y=250)

    # command = lambda: login(root)

    button_explore = Button(root,
                            text="Add User", width=37,
                            command=user_name).place(x=420, y=455)

    cam_button = Button(root,
                        text="Add User By Camera", width=37,
                        command=user_name_for_cam).place(x=420, y=485)

    bd = Button(root,
                text="Create DataBase", width=37,
                command=create_db).place(x=420, y=515)

    Button(root, text=" X ", font=('Verdana', 10), background="red", foreground="black", command=exit).place(
        x=40, y=50)

    root.resizable(0, 0)
    root.mainloop()
