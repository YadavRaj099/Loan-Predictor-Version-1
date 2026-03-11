import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="Loan Approval Predictor", page_icon="💰")

model = joblib.load("loan_model.pkl")

st.title("💰 Loan Approval Predictor")
st.write("Enter applicant details")

gender = st.selectbox("Gender", ["Male","Female"])
married = st.selectbox("Married", ["Yes","No"])
dependents = st.text_input("Dependents","0")
education = st.selectbox("Education", ["Graduate","Not Graduate"])
self_employed = st.selectbox("Self Employed", ["Yes","No"])

applicant_income = st.text_input("Applicant Income","5000")
coapplicant_income = st.text_input("Coapplicant Income","0")
loan_amount = st.text_input("Loan Amount","200")
loan_term = st.text_input("Loan Term","360")

credit_history = st.selectbox("Credit History", ["Good","Bad"])
property_area = st.selectbox("Property Area", ["Rural","Semiurban","Urban"])

gender = 1 if gender=="Male" else 0
married = 1 if married=="Yes" else 0
education = 1 if education=="Graduate" else 0
self_employed = 1 if self_employed=="Yes" else 0
credit_history = 1 if credit_history=="Good" else 0
property_area = 0 if property_area=="Rural" else 1 if property_area=="Semiurban" else 2

extra1 = 0
extra2 = 0

if st.button("Predict Loan Approval"):
    data = np.array([[gender,married,int(dependents),education,self_employed,int(applicant_income),int(coapplicant_income),int(loan_amount),int(loan_term),credit_history,property_area,extra1,extra2]])
    prediction = model.predict(data)
    probability = model.predict_proba(data)[0][1]

    if prediction[0] == 1:
          st.success("Loan Approved")
    else:
          st.error("Loan Rejected")

    st.write("Approval Probability:", round(probability*100,2), "%")
