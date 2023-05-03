# HMSD Team 1 Course Project
This project requires a tool that returns Water Qaulity Index for a given water body through the water quality parameters.
## Main Idea
We have automated the intermediate tools requrired for computing the WQI. These tools include ```Qual2k``` and ```GEFC```. The ```Qual2k``` tool is used to compute the water quality parameters from the water quality data. The ```GEFC``` tool is used to compute the Environmental flow classes for a given water body.
This project essesntially includes 5 steps:
1. Feeding the reservoir inflow values to train a ML model.
2. Feeding the predicted reservoir inflow values to estimate envrionmental flow classes using GEFC.
3. Feeding envrionmental flow classes and Mean Annual Runoff (MAR) to estimate the water quality parameters using Qual2k.
4. Feeding the water quality parameters to estimate the WQI.
5. Visualising the WQI for a given water body.

## Installation
- Clone the repository
- Install the additional packages:
```
    - Matplotlib
    - Numpy
    - Pandas
    - Scikit-learn
    - pyautogui
    - pywinauto
    - streamlit
    - pytesseract
    - cv2
```
- Run the ```frontend.py``` file to start the web app. Use the following command: ```streamlit run frontend.py```
- The web app will be hosted on ```localhost:8501```
- The web app will make necessary calls to ```hmsd.py``` file to perform the required tasks.
- Input the requried data and click on the ```Predict``` button to get the WQI. User will be asked to select data station locations on a given river map after which the final results are displayed.
- Several data files are stored on the go which can be viewed in the cloned folder itself.

## Contributors 
- Aishwarya 
- Viswanadh 
- Akash
- Rishabh
- Meghashyam
- Naveen
- Tushar Asopa
