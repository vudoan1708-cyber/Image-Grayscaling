import cv2 as cv
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
import pyautogui as pgui

# setup speech recognition instance
r = sr.Recognizer()

# Sample rate is how often values are recorded 
sample_rate = 48000

# Chunk is like a buffer. It stores 2048 samples (bytes of data) here
# it is advisable to use powers of 2 such as 1024 or 2048 
chunk_size = 2048

# set an instance for live webcam feed
cap = cv.VideoCapture(0)

# creates root for tkinter interfaces
root = tk.Tk()

# choosn images will be passed to this array variable
path_imgs = []
#############################


#############################
def speakCmd():
    with sr.Microphone(sample_rate = sample_rate,  
                    chunk_size = chunk_size) as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
        try:

            # format: 'capture' + a number + 'image(s)/frame(s)/...'
            cmd = r.recognize_google(audio).lower()
            print(cmd)
            
            # if 'cap' is in a speech
            if 'cap' in cmd:

                # if 'image' is in a speech
                if 'image' in cmd:
                    # split a string with spacebar as separator
                    cmd = cmd.split(' ')

                    print(cmd[0], cmd[1], entry.get())

                    # pass the first, the second array element and the text input field into initCamera function
                    initCamera(cmd[0], int(cmd[1]), entry.get())
                else: initCamera(None, None, entry.get())

            # if 'open' is in a speech
            elif 'open' in cmd:

                # trigger the function to open file directory
                openFolder(entry.get())

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e)) 
##########################


##########################
def initCamera(cmd, cmd_num, cd_PATH):

    # start counter
    counter = 0

    # a boolean var to check the final number of cmd_num
    # if the folder directory contains existing images
    added = False

    # loop this function
    while True:

        # Path to a directory, put it the loop to reset the path every iteration
        PATH = r'assets\img'

        # show sequence of images
        _, frame = cap.read()
        
        # use imshow function to display sequence of images
        cv.imshow('Webcam', frame)

        # grayscale the frames
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # blur the frames to remove background noises
        blur_size = (5, 5)
        blur = cv.GaussianBlur(gray, blur_size, 3)
        
        # binarise the frames
        # _, thresh = cv.threshold(gray, 20, 255, cv.THRESH_BINARY)

        # # Kernel matrices for morphological transformation
        # kernel = np.ones((5, 5), np.uint8)

        # # Dilation and Erosion to remove background noises (morphological transformation) 
        # dil = cv.dilate(thresh, kernel, iterations=2)
        # er = cv.erode(dil, kernel, iterations=1)

        # open a folder that will contain all the captured images/frames            
        # check if a new directory path is mentioned
        if cd_PATH:

            # check if a path doesn't exist
            if not os.path.exists(os.path.join(PATH, cd_PATH)):

                # if not, create one
                os.mkdir(os.path.join(PATH, cd_PATH))
                PATH = os.path.join(PATH, cd_PATH)

            # otherwise
            else:
                PATH = os.path.join(PATH, cd_PATH)

                # update counter with the total number of files
                # in a folder directory
                counter = len(os.listdir(PATH))

                # check if the cmd_num has been added to the total number of files
                # in a folder directory, to extend the upper limit
                if added == False and cmd_num:
                    cmd_num += counter
                    added = True

            # check if a number of images being captured is mentioned
            if cmd_num:

                # open the folder directory
                os.startfile(PATH)

        else: 

            # check if a number of images being captured is mentioned
            if cmd_num:

                # open the folder directory
                os.startfile(PATH)
        

        # check if cmd_num is in integer
        if isinstance(cmd_num, int) and cv.waitKey(1):

            # if a counter is less than a requested number
            if counter < cmd_num:

                # count up the counter by 1
                counter += 1

                # write each frame into an image file (counter starts at 1)
                cv.imwrite(os.path.join(PATH, f'{counter}.png'), blur)

                # automate keypress
                pgui.press('down')

            # otherwise
            else:

                # label output folder
                outputLabel = tk.Label(root, text=f'Output Directory: {PATH}', fg='red')
                outputLabel.pack()

                # break the loop
                break
        
        # or if the keyword 'image' is not mentioned, and a key interrupted
        elif cv.waitKey(1) & 0xFF == ord('s'):

            # count the counter whenever 's' is pressed
            counter += 1

            # write a single frame
            cv.imwrite(os.path.join(PATH, f'{counter}.png'), blur)
    cap.release()
    cv.destroyAllWindows()
#############################


#############################
def openFolder(FOLDER_NAME):

    # clean the array container whenever the function is called
    path_imgs = []

    # open a directory
    path_imageFiles = filedialog.askopenfilename(initialdir='/', title='Select File',
                                        filetypes=( ('img files', '*.png'), ('img files', '*.jpg'), ('all files', '*.*') ),
                                        multiple=True)
                                        
    # make the tuple into a string, then turn it into an array of strings, ultimately to get the path to img files                                      
    path_imageFiles = str(path_imageFiles).split("'")

    # when split the single quotes, total length of the array variable is now doubled
    for count in range( len(path_imageFiles) ):

        # find odd numbers, in order to find the actual path to the imgs
        if count % 2 == 1:

            # append all the paths to the img files into this array
            path_imgs.append(path_imageFiles[count])
    

    # loop through the length of the paths of the chosen imgs
    for path_img in range(len(path_imgs)):

        # path to a directory
        PATH = r'assets\img'

        # read the img files from chosen paths
        i = cv.imread(path_imgs[path_img])

        # convert imgs into numpy array
        i = np.asarray(i)
        
        # grayscale the img
        gray = cv.cvtColor(i, cv.COLOR_BGR2GRAY)

        # blur the frames to remove background noises
        blur_size = (5, 5)
        blur = cv.GaussianBlur(gray, blur_size, 3)

        # if a folder directory is provided
        if FOLDER_NAME:
    
            # check if a path doesn't exist
            if not os.path.exists(os.path.join(PATH, FOLDER_NAME)):

                # if not, create one
                os.mkdir(os.path.join(PATH, FOLDER_NAME))
                PATH = os.path.join(PATH, FOLDER_NAME)

            # otherwise
            else:
                PATH = os.path.join(PATH, FOLDER_NAME)

            # open the folder directory
            os.startfile(PATH)

            # write each frame into an image file to the folder directory
            cv.imwrite(os.path.join(PATH, f'{path_img + 1}.png'), blur)

        # otherwise
        else: 
            os.startfile(PATH)

            # write each frame into an image file to the folder directory
            cv.imwrite(os.path.join(PATH, f'{path_img + 1}.png'), blur)
#############################


#############################
# TKINTER

# change windows title
root.title('Image Grayscaling')

# change windows icon
# root.iconbitmap('')

cv_w = 500
cv_h = cv_w

colour = '#263d42'
canvas = tk.Canvas(root, width = cv_w, height = cv_h, bg = colour)

# attach canvas to the root
canvas.pack()

# add a frame (similar to adding a html tag)
frame = tk.Frame(root, bg = 'white')

# attach frame to the root, set its width, height, x, y
# rel means relative
frame.place(relwidth = 0.8, relheight = 0.8, relx = 0.1, rely = 0.1)

# label
label = tk.Label(frame, text="Command the System Following this Format:" + '\n' + "Capture + (a number) + image(s)/frame(s)/..." +
                                '\n' + '\n' + "For Example:" + '\n' + "Capture 200 images" + 
                                '\n' + '\n' + "Or Just Command:" + '\n' + "Capture" + '\n' "if You Don't Need The Automation. Use 's' to Take A Photo", fg='blue', bg='white', font='none 9')
label.pack()

label_folderName = tk.Label(frame, text="Input An Ouputted Folder Name If You Wish To", fg='black', font='none 10 bold')
label_folderName.place(x=cv_w - 480, y=cv_h / 2 + 25)

label2 = tk.Label(frame, text='\n' + '\n' + "Or Command: 'Open' to Open A Folder Directory" + '\n' "And Add Existing Images", fg='blue', bg='white', font='none 9')
label2.pack()

# user's input
# create an entry box
entry = tk.Entry(root)
canvas.create_window(cv_w / 2, cv_h / 1.25, window=entry)

# buttons 
# initCamBtn = tk.Button(root, text= 'Camera On',padx=20, pady=10, bg=colour, fg='white', command=initCamera)
# initCamBtn.pack()

speakBtn = tk.Button(root, text= 'Command',padx=20, pady=10, bg=colour, fg='white', command=speakCmd)
speakBtn.pack()

# openDirBtn = tk.Button(root, text= 'Open A Folder',padx=20, pady=10, bg=colour, fg='white', command=openFolder)
# openDirBtn.pack()

root.mainloop()

#############################