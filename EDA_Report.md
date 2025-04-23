# 📝 Exploratory Data Analysis Report

## 📊 Dataset Overview
- **Rows:** 614
- **Columns:** 13

## 🔍 Dataset Summary
- **Shape:** (614, 13)
- **Columns:** ['Loan_ID', 'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area', 'Loan_Status']
- **Missing Values:** {'Loan_ID': 0, 'Gender': 13, 'Married': 3, 'Dependents': 15, 'Education': 0, 'Self_Employed': 32, 'ApplicantIncome': 0, 'CoapplicantIncome': 0, 'LoanAmount': 22, 'Loan_Amount_Term': 14, 'Credit_History': 50, 'Property_Area': 0, 'Loan_Status': 0}
- **Data Types:** {'Loan_ID': dtype('O'), 'Gender': dtype('O'), 'Married': dtype('O'), 'Dependents': dtype('O'), 'Education': dtype('O'), 'Self_Employed': dtype('O'), 'ApplicantIncome': dtype('int64'), 'CoapplicantIncome': dtype('float64'), 'LoanAmount': dtype('float64'), 'Loan_Amount_Term': dtype('float64'), 'Credit_History': dtype('float64'), 'Property_Area': dtype('O'), 'Loan_Status': dtype('O')}
- **Summary Statistics:** {'ApplicantIncome': {'count': 614.0, 'mean': 5403.459283387622, 'std': 6109.041673387178, 'min': 150.0, '25%': 2877.5, '50%': 3812.5, '75%': 5795.0, 'max': 81000.0}, 'CoapplicantIncome': {'count': 614.0, 'mean': 1621.2457980271008, 'std': 2926.2483692241885, 'min': 0.0, '25%': 0.0, '50%': 1188.5, '75%': 2297.25, 'max': 41667.0}, 'LoanAmount': {'count': 592.0, 'mean': 146.41216216216216, 'std': 85.58732523570545, 'min': 9.0, '25%': 100.0, '50%': 128.0, '75%': 168.0, 'max': 700.0}, 'Loan_Amount_Term': {'count': 600.0, 'mean': 342.0, 'std': 65.12040985461256, 'min': 12.0, '25%': 360.0, '50%': 360.0, '75%': 360.0, 'max': 480.0}, 'Credit_History': {'count': 564.0, 'mean': 0.8421985815602837, 'std': 0.3648783192364048, 'min': 0.0, '25%': 1.0, '50%': 1.0, '75%': 1.0, 'max': 1.0}}

## 📌 Missing Values
- Check missing values heatmap

## 🚨 Outlier Detection
- **ApplicantIncome:** 50 outliers
- **CoapplicantIncome:** 18 outliers
- **LoanAmount:** 39 outliers
- **Loan_Amount_Term:** 88 outliers
- **Credit_History:** 89 outliers
