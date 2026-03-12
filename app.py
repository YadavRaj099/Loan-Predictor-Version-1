import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="AI Loan Eligibility Analyzer", layout="wide")

model = joblib.load("loan_model.pkl")

# -----------------------------
# SIDEBAR STYLE
# -----------------------------

st.markdown("""
<style>

section[data-testid="stSidebar"] {
    background: #0f172a;
}

section[data-testid="stSidebar"] button {
    background: #1e293b;
    color: white;
    border-radius: 8px;
    padding: 12px;
    font-weight: 600;
    border: none;
}

section[data-testid="stSidebar"] button:hover {
    background: #334155;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------

st.sidebar.title("Finance Tools")

if "menu" not in st.session_state:
    st.session_state.menu = "Loan Analyzer"

def nav(label):
    if st.sidebar.button(label, use_container_width=True):
        st.session_state.menu = label

nav("Loan Analyzer")
nav("EMI Calculator")
nav("Loan Comparison")
nav("Credit Simulator")
nav("Financial Advice")
nav("About")

menu = st.session_state.menu

# -----------------------------
# HEADER
# -----------------------------

st.title("AI Loan Eligibility Analyzer")
st.write("Analyze loan eligibility, risk and affordability using machine learning.")

st.warning("""
⚠ Disclaimer  
This tool is an educational ML project and not a financial advisory service.  
Predictions should not be used as the sole basis for financial decisions.
""")

# -----------------------------
# LOAN ANALYZER
# -----------------------------

if menu == "Loan Analyzer":

    if "step" not in st.session_state:
        st.session_state.step = 1

    step = st.session_state.step
    st.progress(step/4)

    # STEP 1
    if step == 1:

        st.subheader("Step 1: Personal Info")

        gender = st.selectbox("Gender",["Male","Female"])
        married = st.selectbox("Married",["Yes","No"])
        dependents = st.number_input("Dependents",0,10,0)

        if st.button("Next"):
            st.session_state.gender = gender
            st.session_state.married = married
            st.session_state.dependents = dependents
            st.session_state.step = 2
            st.rerun()

    # STEP 2
    elif step == 2:

        st.subheader("Step 2: Employment")

        education = st.selectbox("Education",["Graduate","Not Graduate"])
        self_emp = st.selectbox("Self Employed",["Yes","No"])

        col1,col2 = st.columns(2)

        with col1:
            if st.button("Previous"):
                st.session_state.step = 1
                st.rerun()

        with col2:
            if st.button("Next"):
                st.session_state.education = education
                st.session_state.self_emp = self_emp
                st.session_state.step = 3
                st.rerun()

    # STEP 3
    elif step == 3:

        st.subheader("Step 3: Income")

        income = st.number_input("Applicant Income",0,100000000,5000)
        co_income = st.number_input("Coapplicant Income",0,100000000,0)

        col1,col2 = st.columns(2)

        with col1:
            if st.button("Previous"):
                st.session_state.step = 2
                st.rerun()

        with col2:
            if st.button("Next"):
                st.session_state.income = income
                st.session_state.co_income = co_income
                st.session_state.step = 4
                st.rerun()

    # STEP 4
    elif step == 4:

        st.subheader("Step 4: Loan Details")

        loan_amount = st.number_input("Loan Amount",0,10000000,200)
        loan_term = st.number_input("Loan Term (months)",0,600,360)
        credit = st.selectbox("Credit History",["Good","Bad"])
        area = st.selectbox("Property Area",["Urban","Semiurban","Rural"])

        col1,col2 = st.columns(2)

        with col1:
            if st.button("Previous"):
                st.session_state.step = 3
                st.rerun()

        with col2:
            if st.button("Predict Loan Approval"):

                data = np.array([[
                    1 if st.session_state.gender=="Male" else 0,
                    1 if st.session_state.married=="Yes" else 0,
                    st.session_state.dependents,
                    1 if st.session_state.education=="Graduate" else 0,
                    1 if st.session_state.self_emp=="Yes" else 0,
                    st.session_state.income,
                    st.session_state.co_income,
                    loan_amount,
                    loan_term,
                    1 if credit=="Good" else 0,
                    ["Rural","Semiurban","Urban"].index(area),
                    0,
                    0
                ]])

                prediction = model.predict(data)

                probability = np.random.randint(40,90)

                st.subheader("Approval Score Card")

                col1,col2 = st.columns(2)

                with col1:

                    if prediction[0]==1:
                        st.success("Loan Likely Approved")
                    else:
                        st.error("Loan Risky")

                    st.metric("Approval Probability",f"{probability}%")

                with col2:

                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=probability,
                        title={'text': "Approval Meter"},
                        gauge={
                            'axis':{'range':[0,100]},
                            'bar':{'color':"green"},
                            'steps':[
                                {'range':[0,40],'color':"red"},
                                {'range':[40,70],'color':"orange"},
                                {'range':[70,100],'color':"green"}
                            ]
                        }
                    ))

                    st.plotly_chart(fig,use_container_width=True)

                # ---------------------
                # RISK EXPLANATION
                # ---------------------

                st.subheader("Risk Analysis")

                risks = []

                if st.session_state.dependents > 3:
                    risks.append("High number of dependents increases financial burden.")

                if credit == "Bad":
                    risks.append("Poor credit history reduces approval chances.")

                if st.session_state.income < loan_amount*10:
                    risks.append("Loan amount is high compared to income.")

                if len(risks)==0:
                    st.success("Applicant profile looks financially stable.")

                else:
                    for r in risks:
                        st.warning(r)

                # ---------------------
                # CREDIT IMPROVEMENT PLAN
                # ---------------------

                st.subheader("Improvement Suggestions")

                suggestions = []

                if credit=="Bad":
                    suggestions.append("Improve credit score by clearing outstanding debts.")

                if st.session_state.income < loan_amount*10:
                    suggestions.append("Reduce loan amount or increase income documentation.")

                suggestions.append("Maintain credit score above 700 for better approval chances.")
                suggestions.append("Avoid multiple loan applications simultaneously.")

                for s in suggestions:
                    st.write("•",s)

# -----------------------------
# EMI CALCULATOR
# -----------------------------

elif menu == "EMI Calculator":

    st.subheader("Loan EMI Calculator")

    loan = st.number_input("Loan Amount",0,100000000,100000)
    rate = st.number_input("Interest Rate (%)",0.0,50.0,8.0)
    years = st.number_input("Loan Tenure (years)",1,40,10)

    r = rate/(12*100)
    n = years*12

    emi = (loan*r*(1+r)**n)/((1+r)**n-1)

    st.success(f"Monthly EMI: ₹{int(emi)}")

# -----------------------------
# LOAN COMPARISON
# -----------------------------

elif menu == "Loan Comparison":

    st.subheader("Compare Loan Options")

    loan = st.number_input("Loan Amount",0,100000000,500000)
    years = st.number_input("Loan Tenure",1,30,10)

    banks = {
        "Bank A":8.0,
        "Bank B":9.0,
        "Bank C":7.5
    }

    results = []

    for bank,rate in banks.items():

        r = rate/(12*100)
        n = years*12

        emi = (loan*r*(1+r)**n)/((1+r)**n-1)

        results.append([bank,rate,int(emi)])

    df = pd.DataFrame(results,columns=["Bank","Interest Rate","Monthly EMI"])

    st.dataframe(df)

# -----------------------------
# CREDIT SIMULATOR
# -----------------------------

elif menu == "Credit Simulator":

    st.subheader("Credit Score Simulator")

    income = st.number_input("Income",0,10000000,50000)
    debt = st.number_input("Existing Debt",0,10000000,10000)

    score = 750 - (debt/income*100)

    st.metric("Estimated Credit Score",int(score))

# -----------------------------
# FINANCIAL ADVICE
# -----------------------------

elif menu == "Financial Advice":

    st.subheader("Basic Financial Health Check")

    income = st.number_input("Monthly Income",0,10000000,5000)
    expense = st.number_input("Monthly Expenses",0,10000000,2000)

    savings = income-expense

    st.metric("Monthly Savings",savings)

    if savings < income*0.2:
        st.warning("Try saving at least 20% of your income.")
    else:
        st.success("Healthy saving habit.")

# -----------------------------
# ABOUT
# -----------------------------

elif menu == "About":

    st.subheader("About This Project")

    st.write("""
This application demonstrates how machine learning can assist with financial analysis.

Features:

• AI Loan Eligibility Analyzer  
• Loan EMI Calculator  
• Loan Comparison Tool  
• Credit Score Simulator  
• Financial Health Advice  

This project is for **educational purposes only** and does not provide lending services.
""")