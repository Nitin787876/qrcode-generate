# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 09:49:37 2022

@author: Nitin
"""


import streamlit as st
import pandas as pd
import numpy as np
#mport matplotlib.pyplot as plt
from ameydata3 import create_table,add_data,view_all_persons,delete,get_department,view_update,update
import qrcode
import os
import time
import cv2
#from pyzbar.pyzbar import decode
from PIL import Image
timestrf1=time.strftime("%Y%m%d-%H%M%S")
qr=qrcode.QRCode(version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,border=14)
#load image
def load_image(img):
    im=Image.open(img)
    return im
def main():
    st.title("QR GENERATION AND AUTHETICATION with Streamlite")
    menu=['Create','Read','Update','Delete','DecoderQR','About']
    choice=st.sidebar.selectbox("Menu",menu)
    create_table()
    if choice=='Create':
        st.subheader("Add Person records")
        col1,col2=st.columns(2)
        with col1:
            person_id=st.number_input("Person ID",1,100,1)
            person_name=st.text_input("Person Name")
        with col2:
            
            person_no=st.text_input("Person Phone No.",max_chars=10)
            #st.warning("Phone no.should be 10 digits")
            person_dept=st.selectbox("Department",['PYTHON','SQL','DATA SCIENCE'])
            person_record_date=st.date_input("Generator Date")
        if st.button("Add Record of Person"):
            add_data(person_id,person_name,person_no,person_dept,person_record_date)
            st.success("Successfully added record:{}{}{}{}{}".format(person_id,person_name,person_no,person_dept,person_record_date))                
            st.subheader("QR Generator")
                  
            
        #with st.form(key='myqr_form'):
        raw_text={'pd':person_id,'per_name':person_name,'person_no':person_no}              
        submit_button=st.button("Generate")
         #layout
        if submit_button:
             col1,col2=st.columns(2)
             with col1:
                qr.add_data(raw_text)
                qr.make(fit=True)
                img=qr.make_image(fill_color='black',back_color='white')
                #filename
                img_filename='generate_image_{}{}.png'.format(person_name,timestrf1)
                path_for_images=os.path.join('image',img_filename)
                img.save(path_for_images)
                final_image=load_image(path_for_images)
                st.image(final_image)
             with col2:
                st.info("Original Text")
                st.write(raw_text)
    elif choice=='Read':
        st.subheader("View Records")
        result=view_all_persons()
        st.write(result)
        df=pd.DataFrame(result,columns=['person_id','person_name','person_no','Department','Date'])
        with st.expander("View all records"):
            st.dataframe(df)
        with st.expander("No.of Department"):
            counts=df['Department'].value_counts().to_frame()
            counts=counts.reset_index()
            st.dataframe(counts)
    else:
             st.subheader('About')
                
if __name__=='__main__':
                main()