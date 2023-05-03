import os
import time
import pandas as pd
from pywinauto.application import Application
import pytesseract
import cv2
import numpy as np
import shutil
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn import metrics
from threading import Thread
import csv
import math
from matplotlib import pyplot as plt
import pyautogui

path = os.getcwd()
file = "\Q2KMasterv2_12b1.xls"
file = path+file
os.startfile(file)
time.sleep(5)


pyautogui.moveTo(30, 1000)
time.sleep(0.25)
# pyautogui.keyDown("ctrl")
for i in range(30):
    pyautogui.click(30, 1000)

pyautogui.click(300, 1000)

pyautogui.click(112, 468,clicks=4)
pyautogui.typewrite("125")
# pyautogui.keyDown("ctrl")
# pyautogui.press('s')
# pyautogui.keyUp("ctrl")
# time.sleep(25)
pyautogui.click(540,300)
time.sleep(10)
for i in range(10):
    pyautogui.press('enter')

time.sleep(5)
for i in range(10):
    print("hi")
    pyautogui.press('enter')
time.sleep(5)
pyautogui.press('enter')
pyautogui.press('tab')
pyautogui.press('tab')
pyautogui.press('enter')

pyautogui.moveTo(1000, 1000)
pyautogui.click(800,500)

# pyautogui.keyUp("ctrl")
time.sleep(0.5)

# pyautogui.moveTo(150, 980)
# time.sleep(0.25)
# pyautogui.click(150, 980)
# time.sleep(0.5)

# pyautogui.moveTo(460, 510)
# time.sleep(0.25)
# pyautogui.click(460, 510)
# pyautogui.typewrite(path)
# time.sleep(0.5)

# pyautogui.moveTo(460, 690)
# time.sleep(0.25)
# pyautogui.click(460, 690)
# pyautogui.typewrite("3")
# time.sleep(0.5)

# pyautogui.moveTo(350, 980)
# time.sleep(0.25)
# pyautogui.click(350, 980)
# time.sleep(0.5)

# pyautogui.moveTo(400, 555)
# time.sleep(0.25)
# pyautogui.click(400, 555)
# pyautogui.typewrite(str_flow)
# time.sleep(0.5)

# pyautogui.moveTo(950, 350)
# time.sleep(0.25)
# pyautogui.click(950, 350)
# time.sleep(15)

# pyautogui.press("enter")
# time.sleep(0.25)
# pyautogui.moveTo(920, 600)
# time.sleep(0.5)
# pyautogui.click(920, 600)
# time.sleep(1)

# pyautogui.moveTo(1900, 10)
# time.sleep(0.25)
# pyautogui.click(1910, 10)
# time.sleep(0.25)
# pyautogui.press("enter")
# time.sleep(0.5)

# time.sleep(3)