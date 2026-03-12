# AI Loan Eligibility Analyzer

A machine learning web application that predicts the probability of loan approval based on applicant financial and personal details.

This project demonstrates how a trained machine learning model can be deployed as an interactive web application using Streamlit.

---

## Live Demo

Try the application here:

https://loan-predictor-version-1-n82w4wkr2fyejedd4bgei3.streamlit.app/

---

## Features

• Loan approval probability prediction using a trained ML model  
• Step-by-step loan application wizard  
• Approval probability meter visualization  
• Risk analysis based on financial inputs  
• EMI calculator for loan planning  
• Interactive dashboard built with Streamlit  

---

## How It Works

The model analyzes several applicant attributes including:

- Gender
- Marital status
- Number of dependents
- Education level
- Employment type
- Applicant income
- Co-applicant income
- Loan amount
- Loan term
- Credit history

Using these features, the trained machine learning model estimates the likelihood of loan approval.

---

## Tech Stack

- Python
- Streamlit
- Scikit-learn
- NumPy
- Plotly

---

## Project Structure

AI-Loan-Analyzer

app.py → Streamlit web application  
loan_model.pkl → Trained machine learning model  
requirements.txt → Python dependencies  
README.md → Project documentation  

---

## Installation (Run Locally)

1. Clone the repository

git clone https://github.com/YOUR-USERNAME/AI-Loan-Analyzer.git

2. Navigate to the project directory

cd AI-Loan-Analyzer

3. Install dependencies

pip install -r requirements.txt

4. Run the Streamlit app

streamlit run app.py

---

## Disclaimer

This application is a machine learning demonstration project and should not be used as financial advice or an actual loan approval system.

---

## Future Improvements

- Improved financial risk analysis
- Credit score simulator
- Better UI components
- Integration with financial APIs

---

## Author

Machine Learning Deployment Project