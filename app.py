import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go

st.set_page_config(page_title="AI Loan Analyzer", layout="wide")

# -------------------------
# UI POLISH
# -------------------------

st.markdown("""
<style>

.block-container{
padding-top:2rem;
max-width:1200px;
}

.stSidebar{
background-color:#1f2333;
}

.stSidebar button{
background-color:#2b2f45;
color:white;
border-radius:12px;
height:45px;
font-weight:600;
margin-bottom:10px;
border:1px solid #3c405c;
}

.stSidebar button:hover{
background-color:#40456a;
}

[data-testid="stMetricValue"]{
font-size:28px;
font-weight:700;
}

</style>
""", unsafe_allow_html=True)

model = joblib.load("loan_model.pkl")

# -------------------------
# HEADER
# -------------------------

st.title("AI Loan Eligibility Analyzer")
st.caption("Evaluate loan eligibility and financial risk using machine learning.")

st.info(
"This application is a machine learning demonstration tool and not financial advice."
)

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------

st.sidebar.title("Finance Tools")

if "menu" not in st.session_state:
    st.session_state.menu = "Loan Analyzer"

def nav_button(label):
    if st.sidebar.button(label, use_container_width=True):
        st.session_state.menu = label

nav_button("Loan Analyzer")
nav_button("EMI Calculator")
nav_button("About")

menu = st.session_state.menu

# -------------------------
# LOAN ANALYZER
# -------------------------

if menu == "Loan Analyzer":

    if "step" not in st.session_state:
        st.session_state.step = 1

    step = st.session_state.step
    st.progress(step/4)

# STEP 1
    if step == 1:

        st.subheader("Step 1 • Personal Information")

        gender = st.selectbox("Gender",["Male","Female"])
        married = st.selectbox("Marital Status",["Yes","No"])
        dependents = st.number_input("Dependents",0,10,0)

        if st.button("Next"):
            st.session_state.gender = gender
            st.session_state.married = married
            st.session_state.dependents = dependents
            st.session_state.step = 2
            st.rerun()

# STEP 2
    elif step == 2:

        st.subheader("Step 2 • Employment Details")

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

        st.subheader("Step 3 • Income Details")

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

        st.subheader("Step 4 • Loan Details")

        loan_amount = st.number_input("Loan Amount",0,10000000,200)
        loan_term = st.number_input("Loan Term (months)",1,600,360)
        credit = st.selectbox("Credit History",["Good","Bad"])

        col1,col2 = st.columns(2)

        with col1:
            if st.button("Previous"):
                st.session_state.step = 3
                st.rerun()

        with col2:
            analyze = st.button("Analyze Loan")

        if analyze:

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
                1,0,0
            ]])

            probability = model.predict_proba(data)[0][1]*100
            probability = round(probability,2)

# -------------------------
# EMI CALCULATION FIX
# -------------------------

            interest_rate = 8
            monthly_rate = interest_rate/(12*100)
            n = loan_term

            emi = (loan_amount*monthly_rate*(1+monthly_rate)**n)/((1+monthly_rate)**n-1)

            total_payment = emi*n
            total_interest = total_payment-loan_amount

# -------------------------
# RISK SCORE
# -------------------------

            if probability > 70:
                risk_label = "Low"
            elif probability > 40:
                risk_label = "Medium"
            else:
                risk_label = "High"

            income_total = st.session_state.income + st.session_state.co_income

            emi_ratio = (emi/income_total)*100 if income_total>0 else 0

# -------------------------
# SCORE CARDS
# -------------------------

            st.subheader("Financial Score Card")

            col1,col2,col3 = st.columns(3)

            col1.metric("Approval Probability", f"{probability}%")
            col2.metric("Estimated EMI", f"₹{int(emi)}")
            col3.metric("Risk Level", risk_label)

# -------------------------
# APPROVAL GAUGE
# -------------------------

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=probability,
                title={'text': "Approval Meter"},
                gauge={
                    'axis':{'range':[0,100]},
                    'bar':{'color':"white"},
                    'steps':[
                        {'range':[0,40],'color':"#ff4d4d"},
                        {'range':[40,70],'color':"#ffa500"},
                        {'range':[70,100],'color':"#4caf50"}
                    ],
                    'threshold':{
                        'line':{'color':"white",'width':4},
                        'thickness':0.75,
                        'value':probability
                    }
                }
            ))

            st.plotly_chart(fig,use_container_width=True)

# -------------------------
# EMI BURDEN GAUGE
# -------------------------

            fig2 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=emi_ratio,
                title={'text': "Income vs EMI Burden (%)"},
                gauge={
                    'axis':{'range':[0,100]},
                    'bar':{'color':"white"},
                    'steps':[
                        {'range':[0,25],'color':"#4caf50"},
                        {'range':[25,40],'color':"#ffa500"},
                        {'range':[40,100],'color':"#ff4d4d"}
                    ],
                    'threshold':{
                        'line':{'color':"white",'width':4},
                        'thickness':0.75,
                        'value':emi_ratio
                    }
                }
            ))

            st.plotly_chart(fig2,use_container_width=True)

# -------------------------
# LOAN COST ANALYSIS
# -------------------------

            st.subheader("Loan Cost Analysis")

            c1,c2 = st.columns(2)

            c1.metric("Total Repayment",f"₹{int(total_payment)}")
            c2.metric("Total Interest Paid",f"₹{int(total_interest)}")

# -------------------------
# RISK ANALYSIS
# -------------------------

            st.subheader("Risk Analysis")

            risks=[]

            if st.session_state.dependents > 3:
                risks.append("High number of dependents increases financial pressure.")

            if credit == "Bad":
                risks.append("Poor credit history reduces approval chances.")

            if st.session_state.income < loan_amount*5:
                risks.append("Loan amount is large relative to income.")

            if len(risks)==0:
                st.success("Financial profile appears stable.")
            else:
                for r in risks:
                    st.warning(r)

# -------------------------
# EMI CALCULATOR
# -------------------------

elif menu == "EMI Calculator":

    st.subheader("Loan EMI Calculator")

    loan = st.number_input("Loan Amount",0,100000000,100000)
    rate = st.number_input("Interest Rate (%)",0.0,50.0,8.0)
    years = st.number_input("Loan Tenure (years)",1,40,10)

    r = rate/(12*100)
    n = years*12

    emi = (loan*r*(1+r)**n)/((1+r)**n-1)

    st.metric("Monthly EMI",f"₹{int(emi)}")

# -------------------------
# ABOUT
# -------------------------

elif menu == "About":

    st.subheader("About This Tool")

    st.write("""
AI Loan Eligibility Analyzer demonstrates how machine learning
can estimate loan approval probability using financial inputs.

Built with Python, Streamlit and Scikit-Learn.
""")

# -------------------------
# FOOTER
# -------------------------

st.markdown("---")
st.caption("AI Loan Analyzer • Machine Learning Demonstration Tool")