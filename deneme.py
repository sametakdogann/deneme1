import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import zscore
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

st.title("B2B Transaction Dashboard (Excel Upload)")

st.title("📊 B2B Intelligent Sales Dashboard")
st.write(
    "This dashboard is built with *Streamlit* using the B2B Transaction dataset. "
    "It includes KPIs, interactive visuals and an *ABC–XYZ stock classification* analysis."
)

# -----------------------------
# DATA LOADING
# -----------------------------
@st.cache_data
def load_data(uploaded_file):
    """Read Excel from uploader (or local file as fallback)."""
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
    else:
        # Fallback for running locally (teacher can keep the file in the same folder)
        df = pd.read_excel("B2B_Transaction_Data.xlsx")
    return df

st.sidebar.header("🔁 Data & Filters")

uploaded_file = st.sidebar.file_uploader(
    "Upload *B2B_Transaction_Data.xlsx*", type=["xlsx", "xls"]
)

if uploaded_file is None:
    st.sidebar.info(
        "You can upload the homework dataset here.\n\n"
        "If you are running this locally and the file is in the same folder "
        "as this script, the app will try to load it automatically."
    )

# Try loading data (will crash if file is really missing everywhere, which is okay for homework)
try:
    df = load_data(uploaded_file)
except Exception as e:
    st.error("❌ Data could not be loaded. Please upload the Excel file.")
    st.stop()
    
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
