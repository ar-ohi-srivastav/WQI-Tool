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





# STEP 1
def step_1(data_file_path):
    ## Load data
    # Place the input CSV file in the same directory of the code
    # NOTE: Already removed the NAN columns
    data = pd.read_csv(data_file_path)
    y = data["Inflow"].values
    X = data.drop(["Inflow"], axis=1).values
    ## Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)  # Size split can be changed
    ## Train the model
    rf = RandomForestRegressor()
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)

    ## Evaluating the Algorithm
    rf_rms = np.sqrt(metrics.mean_squared_error(y_test, y_pred_rf))
    print("Random Forest Metrics with test_size=", 0.2, "\n")
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred_rf))
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred_rf))
    print('Root Mean Squared Error:', rf_rms)

    ## Save the predicted inflows

    n = len(y_pred_rf) // 12
    DF = pd.DataFrame(y_pred_rf[:12 * n])
    date = "01/1960"
    ## save the dataframe as a csv file
    np.savetxt(r'C:\Users\SHAIK REHANA\Downloads\HMSD_Project\predict_inflow.txt', DF.values, fmt='%f')
    data = data2 = ""
    # Reading data from file2
    with open(r'C:\Users\SHAIK REHANA\Downloads\HMSD_Project\predict_inflow.txt') as fp:
        data2 = fp.read()

    date += "\n"
    date += data2

    with open(r'C:\Users\SHAIK REHANA\Downloads\HMSD_Project\predict_inflow.txt', 'w') as fp:
        fp.write(date)
    print("Done")

# step_1("input.csv")





# STEP 2
def step_2():

    ## path
    dir = os.getcwd()
    ##
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    ##
    ##
    program = "C:\Program Files (x86)\IWMI\EnvFlowCalculator\ENV_Flow_Calculator.exe"
    ##

    app = Application(backend="uia").start(program, timeout=8)

    Wnd_Main = app.window_(title_re="GLOBAL.*")
    # Wnd_Main.wait('ready', timeout=20)
    Wnd_Main.restore()
    # Wnd_Main.print_control_identifiers()
    # Wnd_Main.menu_select("Data->User Defined File")
    def upload():
        # print("xyz")
        Wnd_Main.menu_select("Data->User Defined File")
        # print("pqr")
    t = Thread(target=upload)
    t.start()
    time.sleep(2)
    pyautogui.typewrite(dir + "\predict_inflow.txt")
    time.sleep(1)
    pyautogui.press('enter')
    t.join()

    # data_select = app.window_(title_re="SELECT.*")
    # data_select.wait('ready', timeout=10)
    # data_select.print_control_identifiers()
    # data_select.edit1.set_text(r"C:\Users\singh\Downloads\data.txt")
    # print_dlg = app.Print
    # print_dlg.wait('ready')
    ini_output = app.window_(title_re="DISPLAY.*")
    ini_output.wait('ready', timeout=20)
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(dir + "\screenshot_1.png")
    ini_output.menu_select("Calculate EFR")
    final_output = app.window_(title_re="DURATION.*")
    final_output.wait('ready', timeout=20)
    myScreenshot1 = pyautogui.screenshot()
    myScreenshot1.save(dir + "\screenshot_2.png")

    ## for saving the table:
    # final_output.menu_select("Save->Save All")
    # save = app.window_(title_re="DURATION.*")
    def save():
        # print("xyz")
        final_output.menu_select("Save->Save All")
        # print("pqr")
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

    # OCR
    img = cv2.imread(dir + "\screenshot_2.png")
    x, y, z = img.shape
    
    # time.sleep(50)
    image = img[int(x * 0.48):int(x * 0.76), int(y * 0.55):int(y * 0.72)]
    # cv2.imshow('ss',image)
    # cv2.waitKey(0)
    # time.sleep(20)
    # crop = cv2.resize(crop, (450, 600))
    # gray_image = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    # ret, thresh1 = cv2.threshold(gray_image, 160, 255, cv2.THRESH_BINARY)
    # ret, thresh1 = cv2.threshold(thresh1, 0, 255, cv2.THRESH_OTSU)
    # kernel = np.ones((3,3),np.uint8)
    # thresh1 = cv2.erode(thresh1,kernel,iterations = 1)
    # thresh1 = cv2.cvtColor(thresh1, cv2.COLOR_GRAY2BGR)
    # cv2.imshow('cropped', thresh1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # image = cv2.imread('index.jpeg')
    image = cv2.fastNlMeansDenoising(image, None, 20, 7, 21)
    image = cv2.resize(image, None, fx=4, fy=4)
    # { cv2.imshow('cropped', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows() } arohi made these comments
    # image to digits using pytesseract
    # txt = pytesseract.image_to_string(image, lang='eng', config='-c tessedit_char_whitelist=0123456789. --psm 6')   
    # txt = pytesseract.image_to_string(thresh1)
    # print(txt)                                   arohi 
    # log = open(dir + "\efr.txt", "w")            aroh                 
    # print(txt, file=log)                          aroh
    # log.close()                                       aroh

    ##
    img2 = cv2.imread(dir + "\screenshot_1.png")
    x, y, z = img2.shape
    crop2 = img2[int(x * 0.64):int(x * 0.77), int(y * 0.55):int(y * 0.72)]
    cv2.imshow('show',crop2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    image = cv2.fastNlMeansDenoising(crop2, None, 20, 7, 21)
    image = cv2.resize(image, None, fx=4, fy=4)
    # cv2.imshow('cropped', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    txt = pytesseract.image_to_string(crop2, lang='eng', config='-c tessedit_char_whitelist=0123456789. --psm 6')
    print(txt)
    log = open(dir + "\stats.txt", "w")
    print(txt, file=log)
    log.close()
    Wnd_Main.close()

# step_2()





# STEP 3
def step_3(user_input):
    print(user_input)
    file1 = open("stats.txt", "r+")
    lines1 = file1.readlines()
    flow = float(lines1[0]) / 60
    flow = flow * float(lines1[1])
    file2 = open("efr.txt", "r+")
    lines2 = file2.readlines()
    # print("kljdskl",lines2[user_input])
    flow = flow * float(lines2[user_input]) / 100
    flow = flow / 15
    str_flow = str(flow)

    path = os.getcwd()
    # print()
    # print("Working Directory:", path)
    file = "\Q2KMasterv2_12b1.xls"
    file = path+file
    # print()
    # print("Excel File Path:", file)
    os.startfile(file)

    time.sleep(5)

    # print()
    # print("Screen Resolution:", pyautogui.size())

    pyautogui.moveTo(30, 980)
    time.sleep(0.25)
    pyautogui.keyDown("ctrl")
    pyautogui.click(30, 980)
    pyautogui.keyUp("ctrl")
    time.sleep(0.5)

    pyautogui.moveTo(150, 980)
    time.sleep(0.25)
    pyautogui.click(150, 980)
    time.sleep(0.5)

    pyautogui.moveTo(460, 510)
    time.sleep(0.25)
    pyautogui.click(460, 510)
    pyautogui.typewrite(path)
    time.sleep(0.5)

    pyautogui.moveTo(460, 690)
    time.sleep(0.25)
    pyautogui.click(460, 690)
    pyautogui.typewrite("3")
    time.sleep(0.5)

    pyautogui.moveTo(350, 980)
    time.sleep(0.25)
    pyautogui.click(350, 980)
    time.sleep(0.5)

    pyautogui.moveTo(400, 555)
    time.sleep(0.25)
    pyautogui.click(400, 555)
    pyautogui.typewrite(str_flow)
    time.sleep(0.5)

    pyautogui.moveTo(950, 350)
    time.sleep(0.25)
    pyautogui.click(950, 350)
    time.sleep(15)

    pyautogui.press("enter")
    time.sleep(0.25)
    pyautogui.moveTo(920, 600)
    time.sleep(0.5)
    pyautogui.click(920, 600)
    time.sleep(1)

    pyautogui.moveTo(1900, 10)
    time.sleep(0.25)
    pyautogui.click(1910, 10)
    time.sleep(0.25)
    pyautogui.press("enter")
    time.sleep(0.5)

    time.sleep(3)

    dict_df = pd.read_excel("Q2KMasterv2_12b1.xls", header=None, sheet_name=["WQ Output"])
    output_df = dict_df.get("WQ Output")
    # x_value = []
    WQI_value = []
    for i in range(0, 30):
        # x_value.append(output_df[2][646-(21*i)])
        DO = output_df[5][646-(21*i)]
        BOD = output_df[7][646-(21*i)]
        COD = output_df[7][646-(21*i)] + output_df[6][646-(21*i)]
        NH4 = output_df[9][646-(21*i)] / 100
        NO3 = output_df[10][646-(21*i)] * 4 / 100
        pH = output_df[22][646-(21*i)]
        TP = output_df[28][646-(21*i)] / 10
        WQI = ((DO * 0.097) + (BOD * 0.117) + (COD * 0.093) + (NH4 * 0.09) + (NO3 * 0.108) + (pH * 0.051) + (TP * 0.087))
        WQI = WQI / (0.097+0.117+0.093+0.09+0.108+0.051+0.087)
        WQI_value.append(100-WQI)

    # print(x_value)
    # print(WQI_value)
    wqi = pd.DataFrame(WQI_value)
    wqi.to_csv("wqi.csv", index=False, header=False)

# env_class = 0
# step_3(env_class)





# STEP 4
def step_4(image_path):
    # fig=plt.figure(figsize=(15,15))
    L_x=[]
    L_y=[]
    image = cv2.imread(image_path) ######### change the image name here
    img= cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # original img
    def click_event(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            L_x.append(x)
            L_y.append(y)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, str(x) + ',' +str(y), (x,y), font,1, (255, 0, 0), 2)
            cv2.imshow('image', img)

    cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    image = cv2.imread(image_path) ######### change the image name here
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # original img
    fig = plt.figure(figsize=(15,15))
    # fig.add_subplot(121)
    plt.imshow(img)

    # wq=[24,89,95] ######### change the WQI values here
    wq = np.genfromtxt('wqi.csv', delimiter=',')
    for i in range(min(len(L_x),len(wq))):
        print(L_x[i])
        if(wq[i]>=0 and wq[i]<=24):
            plt.plot(L_x[i],L_y[i], "or", markersize=10)
        if(wq[i]>=25 and wq[i]<49):
            plt.plot(L_x[i],L_y[i], "or", markersize=10)
        if(wq[i]>=50 and wq[i]<69):
            plt.plot(L_x[i],L_y[i], "or", markersize=10)
        if(wq[i]>=70 and wq[i]<=89):
            plt.plot(L_x[i],L_y[i], "ob", markersize=10)
        if(wq[i]>=90 and wq[i]<100):
            plt.plot(L_x[i],L_y[i], "og", markersize=10)
    plt.tight_layout()
    plt.savefig("WQI.png",format="png",bbox_inches='tight',pad_inches=0)
    # plt.show()
    return fig

# step_4("foxy.png")


def str_man(s1, s2, s3):
    f1 = open(s1, "r")
    f2 = open(s2, "r")
    l1 = f1.readlines()
    l2 = f2.readlines()

    if (len(l1) != len(l2) + 1):
        print("Files are not of desired size")
        return 0
    else:
        l = len(l1)
        ret = []
        for i in range(1, l):
            inflow = int(l1[i])
            storage = int(l2[i - 1])
            if (inflow < storage):
                ret.append(str(inflow) + "\n")
            else:
                ret.append(str(inflow - storage) + "\n")

        file1 = open(s3, 'w')
        file1.writelines(ret)
    return 1