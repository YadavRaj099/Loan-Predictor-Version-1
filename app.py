import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go

model = joblib.load("loan_model.pkl")

st.set_page_config(page_title="AI Loan Analyzer", layout="wide")

# HEADER
st.markdown("""
<div style="background:linear-gradient(90deg,#0f2027,#203a43,#2c5364);
padding:30px;border-radius:12px;margin-bottom:25px">
<h1 style="color:white;">AI Loan Eligibility Analyzer</h1>
<p style="color:#dce3ea;font-size:18px">
Explore loan eligibility, EMI planning and financial insights using AI.
</p>
</div>
""", unsafe_allow_html=True)

# DISCLAIMER
st.warning(
"⚠ Disclaimer: This tool is a demonstration project and not financial advice."
)

# SIDEBAR
st.sidebar.title("Finance Tools")

menu = st.sidebar.radio(
"",
["Home","Loan Analyzer","EMI Calculator","Credit Simulator","Financial Advice","About"]
)

# ---------------- HOME ----------------

if menu == "Home":

    st.subheader("Explore Tools")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.info("AI Loan Eligibility Analyzer\nPredict approval probability.")

    with col2:
        st.info("Loan EMI Calculator\nEstimate monthly payments.")

    with col3:
        st.info("Credit Score Simulator\nExplore credit health.")

# ---------------- LOAN ANALYZER ----------------

elif menu == "Loan Analyzer":

    if "step" not in st.session_state:
        st.session_state.step = 1

    st.progress(st.session_state.step/4)

# STEP 1

    if st.session_state.step == 1:

        st.subheader("Step 1 — Personal Information")

        gender = st.radio("Gender",["Male","Female"],horizontal=True)
        married = st.radio("Married",["Yes","No"],horizontal=True)

        dependents = st.number_input("Dependents",value=0)

        col1,col2 = st.columns(2)

        with col1:
            if st.button("Next"):
                st.session_state.gender = 1 if gender=="Male" else 0
                st.session_state.married = 1 if married=="Yes" else 0
                st.session_state.dependents = dependents
                st.session_state.step = 2
                st.rerun()

# STEP 2

    elif st.session_state.step == 2:

        st.subheader("Step 2 — Education & Employment")

        education = st.radio("Education",["Graduate","Not Graduate"],horizontal=True)

        employment = st.radio(
            "Employment",
            ["Salaried","Self Employed"],
            horizontal=True
        )

        col1,col2 = st.columns(2)

        with col1:
            if st.button("Previous"):
                st.session_state.step = 1
                st.rerun()

        with col2:
            if st.button("Next"):
                st.session_state.education = 1 if education=="Graduate" else 0
                st.session_state.self_employed = 1 if employment=="Self Employed" else 0
                st.session_state.step = 3
                st.rerun()

# STEP 3

    elif st.session_state.step == 3:

        st.subheader("Step 3 — Income")

        applicant_income = st.number_input("Applicant Income",value=5000)
        coapplicant_income = st.number_input("Coapplicant Income",value=0)

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

# STEP 4

    elif st.session_state.step == 4:

        st.subheader("Step 4 — Loan Details")

        loan_amount = st.number_input("Loan Amount",value=200)
        loan_term = st.number_input("Loan Term (months)",value=360)
        interest_rate = st.number_input("Interest Rate (%)",value=8.0)

        credit_history = st.radio("Credit History",["Good","Bad"],horizontal=True)

        property_area = st.radio(
            "Property Area",
            ["Urban","Semiurban","Rural"],
            horizontal=True
        )

        col1,col2,col3 = st.columns(3)

        with col1:
            if st.button("Previous"):
                st.session_state.step = 3
                st.rerun()

        with col2:
            if st.button("Analyze Loan"):

                credit = 1 if credit_history=="Good" else 0
                area = {"Urban":2,"Semiurban":1,"Rural":0}[property_area]

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

                r = interest_rate/(12*100)
                emi = loan_amount*r*((1+r)**loan_term)/(((1+r)**loan_term)-1)

                colA,colB = st.columns([2,1])

                with colA:

                    st.subheader("Loan Analysis")

                    st.metric("Approval Probability",f"{round(probability*100,2)}%")
                    st.metric("Estimated EMI",round(emi,2))

                    if prediction[0]==1:
                        st.success("Loan Likely Approved")
                    else:
                        st.error("Loan Likely Rejected")

                    # PROBABILITY CHART
                    st.subheader("Approval Probability Breakdown")

                    chart = go.Figure(data=[
                        go.Bar(
                            x=["Approval","Rejection"],
                            y=[probability,1-probability],
                            marker_color=["green","red"]
                        )
                    ])

                    chart.update_layout(height=300)

                    st.plotly_chart(chart,use_container_width=True)

                with colB:

                    # GAUGE
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=probability*100,
                        title={'text':"Approval Score"},
                        gauge={
                            'axis':{'range':[0,100]},
                            'bar':{'color':"darkblue"},
                            'steps':[
                                {'range':[0,40],'color':"red"},
                                {'range':[40,70],'color':"orange"},
                                {'range':[70,100],'color':"green"}
                            ]
                        }
                    ))

                    fig.update_layout(height=350)

                    st.plotly_chart(fig,use_container_width=True)

# ---------------- EMI ----------------

elif menu == "EMI Calculator":

    st.title("EMI Calculator")

    loan=st.number_input("Loan Amount",value=100000)
    rate=st.number_input("Interest Rate (%)",value=8.0)
    tenure=st.number_input("Tenure (months)",value=60)

    r=rate/(12*100)
    emi=loan*r*((1+r)**tenure)/(((1+r)**tenure)-1)

    st.metric("Monthly EMI",round(emi,2))

# ---------------- CREDIT ----------------

elif menu == "Credit Simulator":

    st.title("Credit Score Simulator")

    income=st.number_input("Monthly Income",value=5000)
    debt=st.number_input("Monthly Debt",value=0)

    score=650

    if debt>income*0.5:
        score-=100
    elif debt<income*0.2:
        score+=50

    st.metric("Estimated Credit Score",score)

# ---------------- FINANCIAL ADVICE ----------------

elif menu == "Financial Advice":

    st.title("Financial Advice")

    income=st.number_input("Income",value=5000)
    expenses=st.number_input("Expenses",value=2000)

    savings=income-expenses

    st.metric("Monthly Savings",savings)

    if savings<income*0.2:
        st.warning("Try saving at least 20% of income")
    else:
        st.success("Savings look healthy")

# ---------------- ABOUT ----------------

else:

    st.title("About")

    st.write("""
AI Loan Eligibility Analyzer is a machine learning demonstration project.

Features:
• Loan approval prediction
• EMI calculator
• Credit score simulation
• Financial insights
""")