import streamlit as st
import numpy as np
import joblib

model = joblib.load("loan_model.pkl")

st.set_page_config(page_title="AI Loan Eligibility Analyzer")

st.title("AI Loan Eligibility Analyzer")
st.write("Check your loan approval chances step by step")

# initialize step
if "step" not in st.session_state:
    st.session_state.step = 1

# progress bar
progress = st.session_state.step / 4
st.progress(progress)

# STEP 1
if st.session_state.step == 1:

    st.subheader("Step 1: Basic Information")

    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Married", ["Yes", "No"])
    dependents = st.number_input("Dependents", 0, 5, 0)

    if st.button("Next"):
        st.session_state.gender = 1 if gender == "Male" else 0
        st.session_state.married = 1 if married == "Yes" else 0
        st.session_state.dependents = dependents
        st.session_state.step = 2
        st.rerun()

# STEP 2
elif st.session_state.step == 2:

    st.subheader("Step 2: Education & Employment")

    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    self_employed = st.selectbox("Self Employed", ["Yes", "No"])

    if st.button("Next"):
        st.session_state.education = 1 if education == "Graduate" else 0
        st.session_state.self_employed = 1 if self_employed == "Yes" else 0
        st.session_state.step = 3
        st.rerun()

# STEP 3
elif st.session_state.step == 3:

    st.subheader("Step 3: Income Details")

    applicant_income = st.number_input("Applicant Income", 0, 1000000, 5000)
    coapplicant_income = st.number_input("Coapplicant Income", 0, 1000000, 0)

    if st.button("Next"):
        st.session_state.applicant_income = applicant_income
        st.session_state.coapplicant_income = coapplicant_income
        st.session_state.step = 4
        st.rerun()

# STEP 4
elif st.session_state.step == 4:

    st.subheader("Step 4: Loan Details")

    loan_amount = st.number_input("Loan Amount", 0, 1000, 200)
    loan_term = st.number_input("Loan Term (months)", 12, 480, 360)

    credit_history = st.selectbox("Credit History", ["Good", "Bad"])
    property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

    if st.button("Predict Loan Approval"):

        credit = 1 if credit_history == "Good" else 0

        if property_area == "Urban":
            area = 2
        elif property_area == "Semiurban":
            area = 1
        else:
            area = 0

        data = np.array([[

            st.session_state.gender,
            st.session_state.married,
            st.session_state.dependents,
            st.session_state.education,
            st.session_state.self_employed,
            st.session_state.applicant_income,
            st.session_state.coapplicant_income,
            loan_amount,
            loan_term,
            credit,
            area,
            0,
            0

        ]])

        prediction = model.predict(data)

        if prediction[0] == 1:
            st.success("Loan Approved")
        else:
            st.error("Loan Rejected")