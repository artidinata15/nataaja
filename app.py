import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Customer Churn Prediction")

st.title("Customer Churn Prediction")

try:
    model=joblib.load("model.pkl")
except Exception:
    st.warning("model.pkl belum tersedia. Jalankan train_model.py setelah dataset ditambahkan.")
    model=None

age=st.number_input("Age",18,100,30)
premium=st.selectbox("Premium User",[0,1])
visits=st.number_input("Total Visits",0,10000,100)

if st.button("Predict"):
    if model is None:
        st.error("Model belum tersedia.")
    else:
        X=pd.DataFrame([[age,premium,visits]],columns=["age","is_premium_user","total_visits"])
        pred=model.predict(X)[0]
        st.success("Churn" if pred==1 else "Tidak Churn")
