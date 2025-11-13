import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import zscore
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

st.title("B2B Transaction Dashboard (Excel Upload)")

# Kullanıcıdan Excel dosyası yüklemesini iste
uploaded_file = st.file_uploader("Lütfen Excel dosyanızı yükleyin", type=["xlsx"])

if uploaded_file is not None:
    # Excel dosyasını oku
    df = pd.read_excel(uploaded_file)

    st.success("Dosya başarıyla yüklendi!")
    
    # Veri tablosunu göster
    st.subheader("Veri Tablosu")
    st.dataframe(df)
    
    # Örnek: Plotly grafiği
    if 'Amount' in df.columns and 'Quantity' in df.columns:
        st.subheader("Miktar vs Tutar Grafiği")
        fig = px.scatter(df, x='Quantity', y='Amount', title="Miktar vs Tutar")
        st.plotly_chart(fig)
    
    # Örnek: Z-score hesapla ve göster
    if 'Amount' in df.columns:
        df['Amount_zscore'] = zscore(df['Amount'])
        st.subheader("Amount Z-Score")
        st.dataframe(df[['Amount', 'Amount_zscore']])
    
    # Örnek: Basit regresyon (Quantity -> Amount)
    if 'Quantity' in df.columns and 'Amount' in df.columns:
        X = df[['Quantity']].values
        y = df['Amount'].values
        model = LinearRegression()
        model.fit(X, y)
        df['Predicted_Amount'] = model.predict(X)
        st.subheader("Regresyon Tahminleri")
        st.dataframe(df[['Quantity', 'Amount', 'Predicted_Amount']])
else:
    st.info("Lütfen bir Excel dosyası yükleyin.")
