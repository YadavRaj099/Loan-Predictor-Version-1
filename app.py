import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go
import math

st.set_page_config(page_title="AI Loan Eligibility Analyzer", layout="wide")

model = joblib.load("loan_model.pkl")

# -------------------------
# Premium Styling
# -------------------------

st.markdown("""
<style>

body {
background-color:#0e1117;
color:white;
}

.menu-card{
background:#1f2937;
padding:12px;
margin-bottom:10px;
border-radius:10px;
text-align:center;
font-weight:600;
cursor:pointer;
border:1px solid #374151;
}

.menu-card:hover{
background:#2563eb;
}

.result-card{
background:#1f2937;
padding:20px;
border-radius:12px;
margin-top:15px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Sidebar Card Navigation
# -------------------------

if "page" not in st.session_state:
    st.session_state.page = "Loan Analyzer"

st.sidebar.markdown("## Finance Tools")

if st.sidebar.button("Loan Analyzer"):
    st.session_state.page = "Loan Analyzer"

if st.sidebar.button("EMI Calculator"):
    st.session_state.page = "EMI Calculator"

if st.sidebar.button("About"):
    st.session_state.page = "About"

page = st.session_state.page

# =====================================================
# LOAN ANALYZER
# =====================================================

if page == "Loan Analyzer":

    st.title("AI Loan Eligibility Analyzer")

    st.write("Evaluate loan eligibility, affordability and financial risk using machine learning.")

    st.warning("This application is a machine learning demonstration tool and not financial advice.")

    if "step" not in st.session_state:
        st.session_state.step = 1

    step = st.session_state.step

# ---------------- STEP 1 ----------------

    if step == 1:

        st.header("Step 1 • Personal Information")

        gender = st.selectbox("Gender",["Male","Female"])
        married = st.selectbox("Married",["Yes","No"])
        dependents = st.number_input("Dependents",0,10)

        if st.button("Next"):
            st.session_state.gender = gender
            st.session_state.married = married
            st.session_state.dependents = dependents
            st.session_state.step = 2
            st.rerun()

# ---------------- STEP 2 ----------------

    elif step == 2:

        st.header("Step 2 • Education & Work")

        education = st.selectbox("Education",["Graduate","Not Graduate"])
        self_employed = st.selectbox("Self Employed",["Yes","No"])

        col1,col2 = st.columns(2)

        with col1:
            if st.button("Previous"):
                st.session_state.step = 1
                st.rerun()

        with col2:
            if st.button("Next"):
                st.session_state.education = education
                st.session_state.self_employed = self_employed
                st.session_state.step = 3
                st.rerun()

# ---------------- STEP 3 ----------------

    elif step == 3:

        st.header("Step 3 • Income")

        applicant_income = st.number_input("Applicant Monthly Income",0)
        coapplicant_income = st.number_input("Co Applicant Income",0)

        col1,col2 = st.columns(2)

        with col1:
            if st.button("Previous"):
                st.session_state.step = 2
                st.rerun()

        with col2:
            if st.button("Next"):
                st.session_state.applicant_income = applicant_income
                st.session_state.coapplicant_income = coapplicant_income
                st.session_state.step = 4
                st.rerun()

# ---------------- STEP 4 ----------------

    elif step == 4:

        st.header("Step 4 • Loan Details")

        loan_amount = st.number_input("Loan Amount",0)
        loan_term = st.number_input("Loan Term (months)",1)
        credit_history = st.selectbox("Credit History",["Good","Bad"])

        col1,col2 = st.columns(2)

        with col1:
            if st.button("Previous"):
                st.session_state.step = 3
                st.rerun()

        with col2:
            analyze = st.button("Analyze Loan")

        if analyze:

            gender = 1 if st.session_state.gender == "Male" else 0
            married = 1 if st.session_state.married == "Yes" else 0
            education = 1 if st.session_state.education == "Graduate" else 0
            self_employed = 1 if st.session_state.self_employed == "Yes" else 0
            credit = 1 if credit_history == "Good" else 0

            features = np.array([[gender,
                                  married,
                                  st.session_state.dependents,
                                  education,
                                  self_employed,
                                  st.session_state.applicant_income,
                                  st.session_state.coapplicant_income,
                                  loan_amount,
                                  loan_term,
                                  credit]])

            probability = model.predict_proba(features)[0][1]*100

            annual_rate = 0.10
            monthly_rate = annual_rate/12
            n = loan_term

            emi = loan_amount * monthly_rate * ((1 + monthly_rate) ** n) / ((1 + monthly_rate) ** n - 1)

            if probability >= 70:
                risk = "Low"
                message = "Strong financial profile."
            elif probability >= 40:
                risk = "Medium"
                message = "Moderate approval chance."
            else:
                risk = "High"
                message = "Loan approval unlikely."

            col1,col2 = st.columns(2)

            with col1:

                st.markdown('<div class="result-card">', unsafe_allow_html=True)

                st.subheader("Financial Score Card")

                st.metric("Approval Probability",f"{probability:.1f}%")
                st.metric("Estimated EMI",f"₹{emi:,.0f}")
                st.metric("Risk Level",risk)

                st.write(message)

                st.markdown('</div>', unsafe_allow_html=True)

            with col2:

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=probability,
                    gauge={
                        "axis":{"range":[0,100]},
                        "steps":[
                            {"range":[0,40],"color":"red"},
                            {"range":[40,70],"color":"orange"},
                            {"range":[70,100],"color":"green"}
                        ]
                    }
                ))

                st.plotly_chart(fig,use_container_width=True)

# =====================================================
# EMI CALCULATOR
# =====================================================

elif page == "EMI Calculator":

    st.title("Loan EMI Calculator")

    amount = st.number_input("Loan Amount",0)
    rate = st.number_input("Interest Rate (%)",1.0)
    years = st.number_input("Loan Duration (years)",1)

    if st.button("Calculate EMI"):

        r = rate/(12*100)
        n = years*12

        emi = amount*r*((1+r)**n)/((1+r)**n-1)

        st.success(f"Monthly EMI: ₹{emi:,.0f}")

# =====================================================
# ABOUT
# =====================================================

else:

    st.title("About")

    st.write("AI Loan Analyzer is a machine learning project demonstrating loan approval prediction and financial risk evaluation.")