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

txt=''
def step_1(data_file_path):
    data = pd.read_csv(data_file_path)
    y = data["Inflow"].values
    X = data.drop(["Inflow"], axis=1).values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2) 
    rf = RandomForestRegressor()
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    n = len(y_pred_rf) // 12
    DF = pd.DataFrame(y_pred_rf[:12 * n])
    date = "01/1960"
    np.savetxt(r'C:\Users\SHAIK REHANA\Downloads\Webapp\predict_inflow.txt', DF.values, fmt='%f')
    data = data2 = ""
    with open(r'C:\Users\SHAIK REHANA\Downloads\Webapp\predict_inflow.txt') as fp:
        data2 = fp.read()
    date += "\n"
    date += data2
    with open(r'C:\Users\SHAIK REHANA\Downloads\Webapp\predict_inflow.txt', 'w') as fp:
        fp.write(date)
    print("Done")


def step_2(opt):
    print(opt)
    dir = os.getcwd()
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    program = "C:\Program Files (x86)\IWMI\EnvFlowCalculator\ENV_Flow_Calculator.exe"
    app = Application(backend="uia").start(program, timeout=8)
    Wnd_Main = app.window_(title_re="GLOBAL.*")
    Wnd_Main.restore()
    def upload():
        Wnd_Main.menu_select("Data->User Defined File")
    t = Thread(target=upload)
    t.start()
    time.sleep(2)
    pyautogui.typewrite(dir + "\predict_inflow.txt")
    time.sleep(1)
    pyautogui.press('enter')
    t.join()
    ini_output = app.window_(title_re="DISPLAY.*")
    ini_output.wait('ready', timeout=20)
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(dir + "\screenshot_1.png")
    ini_output.menu_select("Calculate EFR")
    final_output = app.window_(title_re="DURATION.*")
    final_output.wait('ready', timeout=20)
    myScreenshot1 = pyautogui.screenshot()
    myScreenshot1.save(dir + "\screenshot_2.png")
   
    def save():
        final_output.menu_select("Save->Save All")
    t1 = Thread(target=save)
    t1.start()
    time.sleep(2)
    pyautogui.typewrite(dir + "\output.txt")
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(.5)
    pyautogui.press('left')
    pyautogui.press('enter')
    t1.join()

    img = cv2.imread(dir + "\screenshot_2.png")
    x, y, z = img.shape
    
    
    
    image = img[int(x * 0.48):int(x * 0.76), int(y * 0.55):int(y * 0.72)]
    image = cv2.fastNlMeansDenoising(image, None, 20, 7, 21)
    image = cv2.resize(image, None, fx=4, fy=4)

    img2 = cv2.imread(dir + "\screenshot_1.png")
    x, y, z = img2.shape
    crop2 = img2[int(x * 0.64):int(x * 0.77), int(y * 0.55):int(y * 0.72)]
    # cv2.imshow('show',crop2)
    cv2.destroyAllWindows()
    image = cv2.fastNlMeansDenoising(crop2, None, 20, 7, 21)
    image = cv2.resize(image, None, fx=4, fy=4)
    txt = pytesseract.image_to_string(crop2, lang='eng', config='-c tessedit_char_whitelist=0123456789. --psm 6')
    txt=txt.splitlines()[0]
    mar=txt[:-1]
    # print(mar)  mar is the value of Mean Average Rainfall


# getting the selected class value in a dictionart
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
        class_per = pytesseract.image_to_string(image, lang='eng', config='-c tessedit_char_whitelist=0123456789. --psm 6')   
        # print(float(class_per))
        print(class_per)
        dic[i]=float(class_per)

    print(dic)

    if(opt=='A'):
        txt=dic[0]
    if(opt=='B'):
        txt=dic[1]
    if(opt=='C'):
        txt=dic[2]
    if(opt=='D'):
        txt=dic[3]
    if(opt=='E'):
        txt=dic[4]
    if(opt=='F'):
        txt=dic[5]

    
    final_value=float(mar) * float(txt)/100 * 0.031709792
    print(str(final_value))

    path = os.getcwd()
    # print(path)
    file = "\Q2KMasterv2_12b1.xls"
    file = path+file
    os.startfile(file)
    time.sleep(5)
    pyautogui.moveTo(30, 1000)           # required sheet
    time.sleep(0.25)
    for i in range(30):
        pyautogui.click(30, 1000)       # required sheet
    pyautogui.click(300, 1000)           #click on the first worksheet


    pyautogui.click(112, 468,clicks=4)       # fill in the value 
    pyautogui.typewrite(str(math.trunc(final_value)))
    print(txt)
    time.sleep(5)
    pyautogui.click(540,300,clicks=1)                 #run fortan
    time.sleep(8)
    print("done")
    for i in range(10):
        pyautogui.press('enter')                # ok
    time.sleep(5)
    for i in range(10):
        pyautogui.press('enter')
    time.sleep(5)
    pyautogui.press('enter')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')


    dict_df = pd.read_excel("Q2KMasterv2_12b1.xls", header=None, sheet_name=["WQ Output"])
    output_df = dict_df.get("WQ Output")
    print(output_df)