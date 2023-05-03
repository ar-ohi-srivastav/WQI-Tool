import streamlit as st
from webapp import *
# give a title to our app
st.title('WQI Prediction Tool')
# Upload Inflow data File
input_file = st.file_uploader("Upload Input File (Inflow data)", type=["csv"])
# Upload Image File
# image_file = st.file_uploader("Upload Image File", type=["png", "jpg", "jpeg"])

if input_file:
    # print(input_file.name)
    with open("temp.csv", 'wb') as f: 
        f.write(input_file.getbuffer())
# if image_file:
#     # print(input_file.name)
#     with open("p"+image_file.name, 'wb') as f: 
#         f.write(image_file.getbuffer())

opt = st.radio(
    "Pick an Environmental Management Class",
    ('A','B','C','D','E','F'))

#If storage values available
# seg_status = st.checkbox('Have reservoir storage data?')

# compare status value
# if(seg_status):
#     # Upload Input File (Reservoir Storage) File in CSV format only 
#     seg_file = st.file_uploader("Upload Input File (Reservoir Storage)", type=["csv"])
#     if (seg_file):
#         with open("s" + seg_file.name, 'wb') as f:
#             f.write(seg_file.getbuffer())
#         errc = str_man("predict_inflow.txt", "s" + seg_file.name, "predict_inflow.txt")
#         if (errc == 0):
#             st.error("Mismatching Files")

# create a button to predict the WQI value 
if st.button('Predict'):
    errc = 1


    if errc != 0:
        class_val = ord(opt) - ord('A')          
        # class_val=0                     arohi made this comment
        st.warning('Wait for the prediction, do not move the cursor...')
        # st.progress(0)
        st.info('Step 1: Calculating Inflow')
        step_1("temp.csv")
        st.progress(30)
        st.info('Step 2: Calculating Environmental Flow Classes')
        step_2(opt)
        # st.progress(60)
        # st.info('Step 3: Calculating Water Quality Parameters')
        # step_3()
        # st.progress(90)
        # st.info('Step 4: Calculating WQI')
        # fig = step_4("foxy.png")
        # st.progress(100)
        # display the predicted value
        # display the figure
        # st.pyplot(fig)
        # st.text('WQI values are displayed on the map')
        # st.header("Legend:")
        # new_title = '<p style="font-family:sans-serif; color:Green; font-size: 22px;">Excellent (>90)</p>'
        # st.markdown(new_title, unsafe_allow_html=True)
        # new_title = '<p style="font-family:sans-serif; color:Blue; font-size: 22px;">Very Good (>70)</p>'
        # st.markdown(new_title, unsafe_allow_html=True)
        # new_title = '<p style="font-family:sans-serif; color:Yellow; font-size: 22px;">Fair (>60)</p>'
        # st.markdown(new_title, unsafe_allow_html=True)
        # new_title = '<p style="font-family:sans-serif; color:Grey; font-size: 22px;">Very Poor (<60)</p>'
        # st.markdown(new_title, unsafe_allow_html=True)
        # st.success('The predicted WQI value is 0.5')
        # st.snow()