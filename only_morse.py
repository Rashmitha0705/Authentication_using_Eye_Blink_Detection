#import modules
from tkinter import *
import os
from tkinter import ttk

import tkinter as tk
from tkinter import Message ,Text
from PIL import Image, ImageTk
import tkinter.ttk as ttk
import tkinter.font as font
import os
from tkinter import *
import tkinter as ttk
import sys
#from morse_converter import MorseConverter as mc
import os 
import pathlib
global  username1
global username12
import cv2
import numpy as np
import dlib
from math import hypot
##import pyglet
import time
import telepot
import random

def Morse(password):
    # Counters
    frames = 0
    letter_index = 0
    blinking_frames = 0
    frames_to_blink = 6
    frames_active_letter = 9

    # Text and keyboard settings
    text = ""
    text1=[]
    keyboard_selected = "left"
    last_keyboard_selected = "left"
    select_keyboard_menu = True
    keyboard_selection_frames = 0
    count=0
    pf =[]
    scanned=0

    ######################Mousse clcking ################################################

    from PyQt5.QtCore import Qt, QTimer, pyqtSignal
    from PyQt5 import QtGui
    from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QDesktopWidget, QPushButton, QGridLayout
    # import sys
    from morse_converter import MorseConverter as mc


    class MouseClicksMorse(QWidget):
        global username1
        global username12
        

        def __init__(self):
            super().__init__()
            self.inputArea = InputArea()
            self.initUI()

        def initUI(self):
            self.center()
            self.resize(700, 500)
            self.setWindowTitle('Mouse Clicks - Morse Code Conversion')

            self.inputArea.update_labels.connect(self.updateLabels)
            self.inputArea.clear_labels.connect(self.clearLabels)

            inst = QLabel()
            inst.setText('Instructions:\n Dot (.)\t\t:  Left Click\n Dash (-)\t\t:  Double Left Click\n Next Letter\t:  Right Click\n Next Word\t:  Double Right Click')
            font = QtGui.QFont("MoolBoran", 18)
            font.setStyleHint(QtGui.QFont.TypeWriter)
            inst.setFont(font)

            grid = QGridLayout()
            grid.setSpacing(5)
            grid.addWidget(inst, 1, 3)
            grid.addWidget(self.inputArea, 1, 0, 5, 1)
            grid.addWidget(self.inputArea.outputMorse, 3, 3)
            grid.addWidget(self.inputArea.outputConverted, 4, 3)
            grid.addWidget(self.inputArea.clearButton, 5, 3)

            self.setLayout(grid)

            self.setGeometry(300, 300, 550, 300)
            self.setWindowTitle('Mouse Clicks - Morse Code Conversion')

            self.show()

        def keyPressEvent(self, event):
            if event.key() == Qt.Key_Escape:
                self.close()

        def center(self):
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())

        def updateLabels(self):
            self.inputArea.outputMorse.setText('Morse Code: <b>' + self.inputArea.message.replace('*', ' ').replace('.', '·'))
            if self.inputArea.message[-1] == '*':
                self.inputArea.outputConverted.setText('Conv. Text: <b>' + mc._morseToText(self.inputArea.message))    ##outputConvclearLabelserted

        def clearLabels(self):
            self.inputArea.outputMorse.setText('Morse Code: ')
            self.inputArea.outputConverted.setText('Conv. Text: ')
            test1=mc._morseToText(self.inputArea.message).strip('\n').strip('\t').strip(' ')
            print('dffdfddddddddddddddddd')
            print('username ,type {},{}'.format(username1,type(username1)))
            username12=username1 + '.txt'
            print((username12))
            file2 = open(username12, "a")
            
            print(file2)        
            file2.write(username1+ ',' + str(test1))
            
            file2.close()
            self.inputArea.message = ''
            exit()


    class InputArea(QWidget):
        update_labels = pyqtSignal()
        clear_labels = pyqtSignal()

        def __init__(self):
            super().__init__()
            self.timer = QTimer()
            self.timer.setInterval(250)
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.timeout)
            self.click_count = 0
            self.message = ''
            self.temp = ''

            self.setAutoFillBackground(True)
            p = self.palette()
            p.setColor(self.backgroundRole(), Qt.lightGray)
            self.setPalette(p)

            self.outputMorse = QLabel()
            self.outputMorse.setText('Morse Code: ')
            self.outputConverted = QLabel()
            self.outputConverted.setText('Conv. Text: ')
            font = QtGui.QFont("Consolas", 10)
            font.setStyleHint(QtGui.QFont.TypeWriter)
            self.outputMorse.setFont(font)
            self.outputConverted.setFont(font)

            self.clearButton = QPushButton('Clear All')
            self.clearButton.clicked.connect(self.sendClearSignal)

        def mousePressEvent(self, event):
            self.click_count += 1
            if event.button() == Qt.LeftButton:
                self.temp = '.'
            if event.button() == Qt.RightButton:
                self.temp = '*'
            if not self.timer.isActive():
                self.timer.start()

        def timeout(self):
            if self.click_count > 1:
                if self.temp == '*':
                    self.message += '**'
                else:
                    self.message += '-'
            else:
                self.message += self.temp
            self.click_count = 0
            self.update_labels.emit()

        def sendClearSignal(self):
            self.clear_labels.emit()

        def getMessage(self):
            return self.message

        def printMessage(self):
            print(self.message)
            


    # Implementing event on register button
    def listToString(s):  
        # initialize an empty string 
        str1 = "" 
        # return string   
        return (str1.join(s))

    def listToString1(s):  
        # initialize an empty string 
        str2 = "" 
        # return string   
        return (''.join(str(e) for e in list))

    def Convert(string): 
        li = list(string.split("")) 
        return li         

    cap = cv2.VideoCapture(0)
    board = np.zeros((300, 700), np.uint8)
    board[:] = 255

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    pf =[]
    ######################
    keyboard = np.zeros((300, 600, 3), np.uint8)


    keys_set_1 = {0: "-", 1: ".", 2: "<",3:'D'}

    def draw_letters(letter_index, text, letter_light):
    # Keys
        if letter_index == 0:
            x = 0
            y = 0
        elif letter_index == 1:
            x = 200
            y = 0
        elif letter_index == 2:
            x = 400
            y = 0
        elif letter_index == 3:
            x = 600
            y = 0
       
        width = 200
        height = 200
        th = 3 # thickness

        # Text settings
        font_letter = cv2.FONT_HERSHEY_PLAIN
        font_scale = 9
        font_th = 4
        text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
        width_text, height_text = text_size[0], text_size[1]
        text_x = int((width - width_text) / 2) + x
        text_y = int((height + height_text) / 2) + y

        if letter_light is True:
            cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
            cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
        else:
            cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (51, 51, 51), -1)
            cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (255, 255, 255), font_th)

    def draw_menu():
        rows, cols, _ = keyboard.shape
        th_lines = 4 # thickness lines


    def midpoint(p1 ,p2):
        return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

    font = cv2.FONT_HERSHEY_PLAIN

    def get_blinking_ratio(eye_points, facial_landmarks):
        left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
        right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
        center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
        center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

        hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

        ratio = hor_line_lenght / ver_line_lenght
        return ratio

    def eyes_contour_points(facial_landmarks):
        left_eye = []
        right_eye = []
        for n in range(36, 42):
            x = facial_landmarks.part(n).x
            y = facial_landmarks.part(n).y
            left_eye.append([x, y])
        for n in range(42, 48):
            x = facial_landmarks.part(n).x
            y = facial_landmarks.part(n).y
            right_eye.append([x, y])
        left_eye = np.array(left_eye, np.int32)
        right_eye = np.array(right_eye, np.int32)
        return left_eye, right_eye

    def get_gaze_ratio(eye_points, facial_landmarks):
            left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                        (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                        (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                        (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                        (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                        (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)

            height, width, _ = frame.shape
            mask = np.zeros((height, width), np.uint8)
            cv2.polylines(mask, [left_eye_region], True, 255, 2)
            cv2.fillPoly(mask, [left_eye_region], 255)
            eye = cv2.bitwise_and(gray, gray, mask=mask)

            min_x = np.min(left_eye_region[:, 0])
            max_x = np.max(left_eye_region[:, 0])
            min_y = np.min(left_eye_region[:, 1])
            max_y = np.max(left_eye_region[:, 1])

            gray_eye = eye[min_y: max_y, min_x: max_x]
            _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
            height, width = threshold_eye.shape
            left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
            left_side_white = cv2.countNonZero(left_side_threshold)

            right_side_threshold = threshold_eye[0: height, int(width / 2): width]
            right_side_white = cv2.countNonZero(right_side_threshold)

            if left_side_white == 0:
                gaze_ratio = 1
            elif right_side_white == 0:
                gaze_ratio = 5
            else:
                gaze_ratio = left_side_white / right_side_white
            return gaze_ratio

    ###################
    scanned=0
    once=1
    scanned =1
    # pf =['1','5']
    one=['.','-','-','-','-']
    two=['.','.','-','-','-']
    thrid=['.','.','.','-','-']
    four=['.','.','.','.','-']

    five=['.','.','.','.','.']
    six=['-','.','.','.','.']
    seven=['-','-','.','.','.']
    eight=['-','-','-','.','.']

    nine=['-','-','-','-','.']
    zero=['-','-','-','-','-']

    paswword =[0,0,0]
    char=[]

    while True:
        
        ret, frame = cap.read()
        rows, cols, _ = frame.shape
        keyboard[:] = (26, 26, 26)
        frames += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Draw a white space for loading bar
        frame[rows - 50: rows, 0: cols] = (255, 255, 255)

        if select_keyboard_menu is True:
            draw_menu()

        # Keyboard selected
        if keyboard_selected == "left":
            keys_set = keys_set_1

        active_letter = keys_set[letter_index]

        # Face detection
        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)

            left_eye, right_eye = eyes_contour_points(landmarks)

            # Detect blinking
            left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
            right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
            blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

            # Eyes color
            cv2.polylines(frame, [left_eye], True, (0, 0, 255), 2)
            cv2.polylines(frame, [right_eye], True, (0, 0, 255), 2)


            if select_keyboard_menu is True:
                # Detecting gaze to select Left or Right keybaord
                gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
                gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
                gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
                print(gaze_ratio)

                if gaze_ratio <= 5:
                    keyboard_selected = "right"
                    keyboard_selection_frames += 1
                    # If Kept gaze on one side more than 15 frames, move to keyboard
                    if keyboard_selection_frames == 15:
                        select_keyboard_menu = False
    ##                    right_sound.play()
                        # Set frames count to 0 when keyboard selected
                        frames = 0
                        keyboard_selection_frames = 0
                    if keyboard_selected != last_keyboard_selected:
                        last_keyboard_selected = keyboard_selected
                        keyboard_selection_frames = 0

            else:
                # Detect the blinking to select the key that is lighting up
                if blinking_ratio > 5:
                    # cv2.putText(frame, "BLINKING", (50, 150), font, 4, (255, 0, 0), thickness=3)
                    blinking_frames += 1
                    frames -= 1

                    # Show green eyes when closed
                    cv2.polylines(frame, [left_eye], True, (0, 255, 0), 2)
                    cv2.polylines(frame, [right_eye], True, (0, 255, 0), 2)

                    # Typing letter
                    if blinking_frames == frames_to_blink:
                        if active_letter != "E" and active_letter != "C":
                            count=count+1
                            text += active_letter
                            text1.append(active_letter)
                            print('text1 {}'.format(text1))
                        if active_letter == "<" or active_letter == "D" :
                            text += " "
                            count=count-1
                            text1.pop(count)
                            count=count-1
                            text1.pop(count)                        
                            print('del {}'.format(text1))
                        text += " "
                        #print("text {}".format(text))
                        ###############################3
                        cv2.putText(frame,str(text1) , (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA)
                        time.sleep(1)
                        ##################################3
                        if len(text1) == 5 :
                            print('Selection of Single no is completd ')
                            print(type(str(text1)))
                            
                            

                            if text1 == one:
                                print('Selected no {}'.format(one))
                                text1=[]
                                count=0
                                once =1
                                char.append('1')
                                

                            if text1 == two:
                                print('Selected no {}'.format(two))
                                text1=[]
                                count=0
                                once =1
                                char.append('2')

                            if text1 == thrid:
                                print('Selected no {}'.format(thrid))
                                text1=[]
                                count=0
                                once =1
                                char.append('3')

                            if text1 == four:
                                print('Selected no {}'.format(four))
                                text1=[]
                                count=0
                                once =1
                                char.append('4')
                            if text1 == five:
                                print('Selected no {}'.format(five))
                                text1=[]
                                count=0
                                once =1
                                char.append('5')
                            if text1 == six:
                                print('Selected no {}'.format(six))
                                text1=[]
                                count=0
                                once =1
                                char.append('6')

                            if text1 == seven:
                                print('Selected no {}'.format(seven))
                                text1=[]
                                count=0
                                once =1
                                char.append('7')

                            if text1 == eight:
                                print('Selected no {}'.format(eight))
                                text1=[]
                                count=0
                                once =1
                                char.append('8')

                            if text1 == nine:
                                print('Selected no {}'.format(nine))
                                text1=[]
                                count=0
                                once =1
                                char.append('9')
                            if text1 == zero:
                                print('Selected no {}'.format(zero))
                                text1=[]
                                count=0
                                once =1
                                char.append('0')

                            else:
                                #print('not ,matched ')
                                text1=[]
                                count=0
                                #print('Not MAtched char {}'.format(str(char)))
                            print('paswword {}'.format(str(char)))
                        select_keyboard_menu = True
                        # time.sleep(1)

                else:
                    blinking_frames = 0


        # Display letters on the keyboard
        if select_keyboard_menu is False:
            if frames == frames_active_letter:
                time.sleep(0.45)
                letter_index += 1
                frames = 0
            if letter_index == 3:
                letter_index = 0
            for i in range(3):
                if i == letter_index:
                    light = True
                else:
                    light = False
                draw_letters(i, keys_set[i], light)

        # Show the text we're writing on the board
        cv2.putText(board, str(text1), (80, 100), font, 9, 0, 3)

        # Blinking loading bar
        percentage_blinking = blinking_frames / frames_to_blink
        loading_x = int(cols * percentage_blinking)
        cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (51, 51, 51), -1)
        pwd=''
        ''
        if len(char) > 1 :
            break
        cv2.imshow("Frame", frame)
        cv2.imshow("Virtual keyboard", keyboard)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

    pwd=listToString(char)
    print ('Got the password and i  {} ,{}'.format(pwd,password))
    print ('Type the xhar password and i  {} ,{}'.format(type(pwd),type(password)))

    start=0
    if str(pwd) == str(password) :
        print('Password matches')
        return 'match'
    else:
        print('Failed')
        return 'mismatch'

