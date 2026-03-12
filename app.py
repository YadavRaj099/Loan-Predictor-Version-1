import streamlit as st
import numpy as np
import joblib
import math

model = joblib.load("loan_model.pkl")

st.set_page_config(page_title="AI Loan Analyzer", layout="wide")

st.sidebar.title("AI Finance Tools")

menu = st.sidebar.radio(
"Select Tool",
[
"Loan Eligibility Analyzer",
"EMI Calculator",
"Credit Score Simulator",
"Financial Advice",
"About"
]
)

# ---------------- LOAN ANALYZER ----------------

if menu == "Loan Eligibility Analyzer":

    st.title("AI Loan Eligibility Analyzer")
    st.write("Check your loan approval chances using machine learning.")

    gender = st.selectbox("Gender",["Male","Female"])
    married = st.selectbox("Married",["Yes","No"])
    dependents = st.number_input("Dependents",0)

    education = st.selectbox("Education",["Graduate","Not Graduate"])
    self_employed = st.selectbox("Self Employed",["Yes","No"])

    applicant_income = st.number_input("Applicant Income",value=5000)
    coapplicant_income = st.number_input("Coapplicant Income",value=0)

    loan_amount = st.number_input("Loan Amount",value=200)
    loan_term = st.number_input("Loan Term (months)",value=360)

    credit_history = st.selectbox("Credit History",["Good","Bad"])
    property_area = st.selectbox("Property Area",["Urban","Semiurban","Rural"])

    if st.button("Predict Loan Approval"):

        gender = 1 if gender=="Male" else 0
        married = 1 if married=="Yes" else 0
        education = 1 if education=="Graduate" else 0
        self_employed = 1 if self_employed=="Yes" else 0
        credit = 1 if credit_history=="Good" else 0

        if property_area=="Urban":
            area=2
        elif property_area=="Semiurban":
            area=1
        else:
            area=0

        data = np.array([[

        gender,
        married,
        dependents,
        education,
        self_employed,
        applicant_income,
        coapplicant_income,
        loan_amount,
        loan_term,
        credit,
        area,
        0,
        0

        ]])

        prediction = model.predict(data)
        probability = model.predict_proba(data)[0][1]

        st.subheader("Prediction Result")

        st.metric("Approval Probability", str(round(probability*100,2))+"%")

        meter=int(probability*100)

        if meter>70:
            color="green"
        elif meter>40:
            color="orange"
        else:
            color="red"

        st.markdown(f"""
        <div style='background:#222;padding:25px;border-radius:10px;text-align:center'>
        <h1 style='color:{color};'>{meter}%</h1>
        <p>Approval Likelihood</p>
        </div>
        """,unsafe_allow_html=True)

        if prediction[0]==1:
            st.success("Loan Likely Approved")
        else:
            st.error("Loan Likely Rejected")

# ---------------- EMI CALCULATOR ----------------

elif menu == "EMI Calculator":

    st.title("Loan EMI Calculator")

    loan = st.number_input("Loan Amount",value=100000)
    rate = st.number_input("Interest Rate (%)",value=8.0)
    tenure = st.number_input("Loan Tenure (months)",value=60)

    r = rate/(12*100)

    emi = loan*r*((1+r)**tenure)/(((1+r)**tenure)-1)

    st.metric("Monthly EMI",round(emi,2))

# ---------------- CREDIT SCORE ----------------

elif menu == "Credit Score Simulator":

    st.title("Credit Score Simulator")

    income = st.number_input("Monthly Income",value=5000)
    debts = st.number_input("Existing Monthly Debts",value=0)
    history = st.selectbox("Payment History",["Excellent","Good","Average","Poor"])

    score = 600

    if history=="Excellent":
        score +=150
    elif history=="Good":
        score +=100
    elif history=="Average":
        score +=50

    if debts>income*0.5:
        score -=100

    st.metric("Estimated Credit Score",score)

# ---------------- FINANCIAL ADVICE ----------------

elif menu == "Financial Advice":

    st.title("AI Financial Advice")

    income = st.number_input("Monthly Income",value=5000)
    expenses = st.number_input("Monthly Expenses",value=2000)

    savings = income-expenses

    st.metric("Monthly Savings",savings)

    if savings < income*0.2:
        st.warning("Try saving at least 20% of your income.")

    else:
        st.success("Your savings rate looks healthy.")

# ---------------- ABOUT ----------------

else:

    st.title("About This Tool")

    st.write("""
This platform provides financial analysis tools powered by AI.

Features included:

• Loan Eligibility Prediction  
• EMI Calculator  
• Credit Score Simulator  
• Financial Advice Engine  

Built using Machine Learning and Streamlit.
""")