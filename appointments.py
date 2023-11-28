
import streamlit as st
from datetime import datetime, timedelta, date
import csv
from csv import DictWriter
from streamlit_gsheets import GSheetsConnection


st.set_page_config(page_title="Healthcare Appointment", page_icon="👩‍⚕️", layout="centered", initial_sidebar_state="auto")

st.title("Healthcare Appointment Form")

conn = st.experimental_connection("gsheets", type =GSheetsConnection)

# Patient Information
with st.expander("Patient Information"):
    patient_name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=1, max_value=150, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

# Contact Information
with st.expander("Contact Information"):
    email = st.text_input("Email")
    phone_number = st.text_input("Phone Number")

# Appointment Details
with st.expander("Appointment Details"):
    today = datetime.today().date()
    max_date = today + timedelta(days=365 * 10)  # Maximum date is set to 10 years from today
    min_date = today + timedelta(days=1)  # Minimum date is set to tomorrow
    preferred_date = st.date_input("Preferred Date", min_value=today , format="DD/MM/YYYY")
    preferred_time = st.time_input("Preferred Time")
    department = st.selectbox("Department", ["Cardiology", "Dermatology", "Orthopedics", "Neurology", "Other"])

# Additional Information
additional_info = st.text_area("Additional Information or Questions")

# Submit Button
if st.button("Submit Appointment"):
    # Check if the selected date is in the past
    if preferred_date < today:
        st.warning("Please select a date in the future for your appointment.")
    else:
        # You can add your backend logic to process the appointment here
        st.success("Appointment submitted successfully! We will contact you shortly.")

#Saving the form data into a csv file
        column_names = ["Patient Name" , 	"Age","Gender",	"Email",	"Phone Number"	,"Appointment Date",	"Time",	"Department",	"Queries"]
        dict = {"Patient Name":patient_name , 	"Age":age,"Gender":gender,	"Email":email,	"Phone Number":phone_number	,"Appointment Date":preferred_date,	"Time":preferred_time,	"Department":department,	"Queries":additional_info}
        with open('extracted_data.csv' , 'a') as file:
            data = DictWriter(file, fieldnames=column_names)
            data.writerow(dict)
            file.close()
worksheet_name = "extracted_data"
conn.write("extracted_data.csv" , worksheet_name = worksheet_name)