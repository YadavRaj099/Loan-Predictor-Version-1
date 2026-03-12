import streamlit as st
import numpy as np
import joblib
import math

model = joblib.load("loan_model.pkl")

st.set_page_config(page_title="AI Loan Analyzer", layout="wide")

# HEADER
st.markdown("""
<h1 style='color:#2E86C1;'>AI Loan Eligibility Analyzer</h1>
<p style='font-size:18px;'>Analyze loan eligibility, financial risk and EMI using AI.</p>
""", unsafe_allow_html=True)

st.markdown("---")

# DISCLAIMER
st.warning("""
⚠️ **Disclaimer:**  
This tool is an educational project and not a financial advisory service.  
Predictions are based on machine learning models and should not be used as the sole basis for financial decisions.
""")

# SIDEBAR
st.sidebar.title("Finance Tools")

menu = st.sidebar.radio(
"Navigation",
[
"Loan Analyzer",
"EMI Calculator",
"Credit Score Simulator",
"Financial Advice",
"About"
]
)

# ---------------- LOAN ANALYZER ----------------

if menu == "Loan Analyzer":

    if "step" not in st.session_state:
        st.session_state.step = 1

    progress = st.session_state.step / 4
    st.progress(progress)

# STEP 1
    if st.session_state.step == 1:

        st.subheader("Step 1: Personal Information")

        col1,col2 = st.columns(2)

        with col1:
            gender = st.radio("Gender",["Male","Female"], horizontal=True)

        with col2:
            married = st.radio("Marital Status",["Single","Married"], horizontal=True)

        dependents = st.number_input("Dependents",value=0)

        if st.button("Next"):

            st.session_state.gender = 1 if gender=="Male" else 0
            st.session_state.married = 1 if married=="Married" else 0
            st.session_state.dependents = dependents

            st.session_state.step = 2
            st.rerun()

# STEP 2
    elif st.session_state.step == 2:

        st.subheader("Step 2: Education & Employment")

        education = st.radio("Education",["Graduate","Not Graduate"], horizontal=True)

        employment = st.radio(
        "Employment Type",
        ["Salaried","Self Employed"],
        horizontal=True
        )

        if st.button("Next"):

            st.session_state.education = 1 if education=="Graduate" else 0
            st.session_state.self_employed = 1 if employment=="Self Employed" else 0

            st.session_state.step = 3
            st.rerun()

# STEP 3
    elif st.session_state.step == 3:

        st.subheader("Step 3: Income")

        applicant_income = st.number_input("Monthly Income",value=5000)
        coapplicant_income = st.number_input("Coapplicant Income",value=0)

        if st.button("Next"):

            st.session_state.applicant_income = applicant_income
            st.session_state.coapplicant_income = coapplicant_income

            st.session_state.step = 4
            st.rerun()

# STEP 4
    elif st.session_state.step == 4:

        st.subheader("Step 4: Loan Details")

        loan_amount = st.number_input("Loan Amount",value=200)
        loan_term = st.number_input("Loan Term (months)",value=360)
        interest_rate = st.number_input("Interest Rate (%)",value=8.0)

        credit_history = st.radio("Credit History",["Good","Bad"], horizontal=True)

        property_area = st.radio(
        "Property Area",
        ["Urban","Semiurban","Rural"],
        horizontal=True
        )

        if st.button("Analyze Loan"):

            credit = 1 if credit_history=="Good" else 0

            if property_area=="Urban":
                area=2
            elif property_area=="Semiurban":
                area=1
            else:
                area=0

            data=np.array([[

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

            prediction=model.predict(data)
            probability=model.predict_proba(data)[0][1]

            income_total = st.session_state.applicant_income + st.session_state.coapplicant_income
            loan_to_income = loan_amount/(income_total+1)

            risk_score=int((1-probability)*100)

# EMI
            r = interest_rate/(12*100)
            emi = loan_amount*r*((1+r)**loan_term)/(((1+r)**loan_term)-1)

            col1,col2 = st.columns([2,1])

            with col1:

                st.subheader("Loan Analysis")

                st.metric("Approval Probability",str(round(probability*100,2))+"%")
                st.metric("Risk Score",str(risk_score))
                st.metric("Loan to Income Ratio",round(loan_to_income,2))
                st.metric("Estimated EMI",round(emi,2))

                if prediction[0]==1:
                    st.success("Loan Likely Approved")
                else:
                    st.error("Loan Likely Rejected")

            with col2:

                st.subheader("Approval Meter")

                meter=int(probability*100)

                if meter>70:
                    color="green"
                elif meter>40:
                    color="orange"
                else:
                    color="red"

                st.markdown(f"""
                <div style='background:#222;padding:30px;border-radius:12px;text-align:center'>
                <h1 style='color:{color};'>{meter}%</h1>
                <p>Approval Likelihood</p>
                </div>
                """,unsafe_allow_html=True)

# ---------------- EMI TOOL ----------------

elif menu == "EMI Calculator":

    st.title("EMI Calculator")

    loan = st.number_input("Loan Amount",value=100000)
    rate = st.number_input("Interest Rate (%)",value=8.0)
    tenure = st.number_input("Loan Tenure (months)",value=60)

    r = rate/(12*100)
    emi = loan*r*((1+r)**tenure)/(((1+r)**tenure)-1)

    st.metric("Monthly EMI",round(emi,2))

# ---------------- CREDIT TOOL ----------------

elif menu == "Credit Score Simulator":

    st.title("Credit Score Simulator")

    income = st.number_input("Monthly Income",value=5000)
    debt = st.number_input("Existing Monthly Debt",value=0)

    score = 650

    if debt > income*0.5:
        score -=100

    elif debt < income*0.2:
        score +=50

    st.metric("Estimated Credit Score",score)

# ---------------- ADVICE ----------------

elif menu == "Financial Advice":

    st.title("Financial Advice")

    income = st.number_input("Monthly Income",value=5000)
    expenses = st.number_input("Monthly Expenses",value=2000)

    savings = income-expenses

    st.metric("Monthly Savings",savings)

    if savings < income*0.2:
        st.warning("Try saving at least 20% of income.")

    else:
        st.success("Savings level looks healthy.")

# ---------------- ABOUT ----------------

else:

    st.title("About This Tool")

    st.write("""
AI Loan Eligibility Analyzer is a demonstration project built using machine learning.

Features include:

• Loan approval prediction  
• EMI calculation  
• Credit score simulation  
• Financial advice  

This project demonstrates how AI can assist with financial analysis.
""")