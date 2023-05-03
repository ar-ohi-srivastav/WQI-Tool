import os
import pyautogui
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



dir = os.getcwd()
dic={}
img = cv2.imread(dir + "\screenshot_2.png")
for i in range(6) :
    # print(i)
    x, y, z = img.shape
    # print(float(x * 0.27 +float(i) * 0.))
    image = img[int(x * 0.27 + i * 32):int(x * 0.29 + i * 32), int(y * 0.67):int(y * 0.70)]
    image = cv2.fastNlMeansDenoising(image, None, 20, 7, 21)
    image = cv2.resize(image, None, fx=4, fy=4)
    # cv2.imshow('cropped', image)
    # cv2.waitKey(0)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    txt = pytesseract.image_to_string(image, lang='eng', config='-c tessedit_char_whitelist=0123456789. --psm 6')   
    print(float(txt))
    dic[i]=float(txt)

print(dic)