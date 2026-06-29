import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import base64
from datetime import datetime

# Helper to get base64 image for embedding in markdown
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return ""

# Set page configuration with a premium icon and title
st.set_page_config(
    page_title="Churn Analyst Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for high-end UI design, glassmorphism, gradient buttons, and modern inputs
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-title {
        background: linear-gradient(135deg, #FF4B4B 0%, #902020 50%, #300C0C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #8E9AAF;
        font-size: 1.15rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, rgba(255, 75, 75, 0.1) 0%, rgba(30, 30, 47, 0.2) 100%);
        padding: 10px 15px;
        border-radius: 6px;
        margin-top: 1.8rem;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
    }
    .section-header h4 {
        margin: 0;
        color: #F8F9FA;
        font-size: 1.15rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
    }
    
    /* Premium Glassmorphism Cards */
    .result-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        color: #FF4B4B;
        text-shadow: 0 0 10px rgba(255, 75, 75, 0.3);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #8E9AAF;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    
    /* Glowing Churn Badge */
    .custom-badge {
        display: inline-block;
        padding: 0.5em 1em;
        font-size: 0.9em;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        border-radius: 8px;
        letter-spacing: 1px;
    }
    .badge-churn-glow {
        background: linear-gradient(135deg, #DC3545 0%, #901C27 100%);
        color: white;
        box-shadow: 0 0 15px rgba(220, 53, 69, 0.5);
    }
    .badge-active-glow {
        background: linear-gradient(135deg, #198754 0%, #0E4F31 100%);
        color: white;
        box-shadow: 0 0 15px rgba(25, 135, 84, 0.5);
    }
    
    /* Custom Styled Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #FF4B4B 0%, #B82525 100%) !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        box-shadow: 0 4px 20px rgba(255, 75, 75, 0.3) !important;
        width: 100% !important;
        margin-top: 1rem;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 75, 75, 0.5) !important;
        background: linear-gradient(90deg, #FF6B6B 0%, #D83535 100%) !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) !important;
    }
    
    /* Custom Styled Navigation Dropdown Button */
    .element-container:has(.nav-label-trigger) + .element-container div[data-baseweb="select"] {
        border-radius: 10px !important;
        border: none !important;
    }
    .element-container:has(.nav-label-trigger) + .element-container div[data-baseweb="select"] > div {
        background: linear-gradient(90deg, #FF4B4B 0%, #B82525 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        height: auto !important;
        min-height: 45px !important;
        display: flex !important;
        align-items: center !important;
    }
    .element-container:has(.nav-label-trigger) + .element-container div[data-baseweb="select"] > div:hover {
        background: linear-gradient(90deg, #FF6B6B 0%, #D83535 100%) !important;
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.5) !important;
        transform: translateY(-1px) !important;
    }
    .element-container:has(.nav-label-trigger) + .element-container div[data-baseweb="select"] span {
        color: white !important;
    }
    .element-container:has(.nav-label-trigger) + .element-container div[data-baseweb="select"] svg {
        fill: white !important;
        stroke: white !important;
    }
    
    /* Custom style for preset buttons */
    .preset-container {
        background: rgba(255, 255, 255, 0.02);
        border: 1px dashed rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load model
@st.cache_resource
def load_model():
    if os.path.exists("best_churn_pipeline.joblib"):
        return joblib.load("best_churn_pipeline.joblib")
    return None

model_data = load_model()

# Header Section
st.markdown("""
<div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
  <svg width="45" height="45" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 0 8px rgba(255,75,75,0.6)); margin-right: 12px;">
    <circle cx="12" cy="12" r="9" stroke="url(#title-grad)" stroke-width="2" />
    <circle cx="12" cy="12" r="4" fill="url(#title-grad)" />
    <path d="M12 2V5M12 19V22M2 12H5M19 12H22" stroke="url(#title-grad)" stroke-width="2" stroke-linecap="round"/>
    <defs>
      <linearGradient id="title-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#FF4B4B" />
        <stop offset="100%" stop-color="#852222" />
      </linearGradient>
    </defs>
  </svg>
  <span class="main-title" style="margin: 0; line-height: 1;">Churn Customer Predictor</span>
</div>
""", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Platform analisis cerdas untuk memprediksi potensi churn pelanggan dan mengoptimalkan retensi.</div>', unsafe_allow_html=True)

if model_data is None:
    st.warning("⚠️ Model belum dilatih! Silakan jalankan file `notebook_uas.py` terlebih dahulu untuk melatih model dan menghasilkan file `best_churn_pipeline.joblib`.")
else:
    pipeline = model_data['pipeline']
    numeric_features = model_data['numeric_features']
    categorical_features = model_data['categorical_features']
    cap_limits = model_data['cap_limits']
    
    # Initialize session state for inputs (for simulation presets)
    if 'gender' not in st.session_state:
        st.session_state.gender = "Male"
        st.session_state.age = 35
        st.session_state.country = "Germany"
        st.session_state.city = "Berlin"
        st.session_state.payment_method = "Card"
        st.session_state.subscription_type = "Annual"
        st.session_state.is_premium_user = "Ya"
        st.session_state.signup_date = datetime(2023, 5, 15).date()
        st.session_state.last_purchase_date = datetime(2024, 12, 1).date()
        st.session_state.total_spent = 850.0
        st.session_state.avg_order_value = 65.0
        st.session_state.lifetime_value = 1800.0
        st.session_state.total_visits = 14
        st.session_state.avg_session_time = 8.5
        st.session_state.pages_per_session = 3.5
        st.session_state.email_open_rate = 0.65
        st.session_state.email_click_rate = 0.25
        st.session_state.discount_used = "Ya"
        st.session_state.coupon_code = "SALE15"
        st.session_state.support_tickets = 1
        st.session_state.refund_requested = "Tidak"
        st.session_state.delivery_delay_days = 2
        st.session_state.satisfaction_score = 4.0
        st.session_state.nps_score = 8
        st.session_state.marketing_spend_per_user = 12.0
        st.session_state.last_3_month_purchase_freq = 6

    # Navigation Dropdown Selector
    st.markdown('<div class="nav-label-trigger" style="margin-top: 1.5rem; margin-bottom: 0.5rem;"><label style="font-size: 0.85rem; color: #8E9AAF; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase;">🧭 Navigasi Dashboard</label></div>', unsafe_allow_html=True)
    view = st.selectbox(
        "Pilih Menu Dashboard",
        [
            "🎯 Prediksi Churn Pelanggan", 
            "📈 Eksplorasi & Analisis Data", 
            "⚡ Performa Model & Evaluasi"
        ],
        label_visibility="collapsed"
    )
    st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)
    
    if view == "🎯 Prediksi Churn Pelanggan":
        # Simulation Preset Buttons
        st.markdown('<div class="preset-container">', unsafe_allow_html=True)
        st.write("💡 **Simulasi Instan**: Pilih salah satu profil pelanggan di bawah ini untuk mengisi formulir secara otomatis.")
        p_col1, p_col2 = st.columns(2)
        
        with p_col1:
            if st.button("✅ Load Profil: Pelanggan Setia (Low Risk)"):
                st.session_state.gender = "Female"
                st.session_state.age = 45
                st.session_state.country = "Germany"
                st.session_state.city = "Hamburg"
                st.session_state.payment_method = "Card"
                st.session_state.subscription_type = "Annual"
                st.session_state.is_premium_user = "Ya"
                st.session_state.signup_date = datetime(2022, 1, 15).date()
                st.session_state.last_purchase_date = datetime(2025, 2, 20).date()
                st.session_state.total_spent = 2800.0
                st.session_state.avg_order_value = 95.0
                st.session_state.lifetime_value = 4200.0
                st.session_state.total_visits = 28
                st.session_state.avg_session_time = 14.5
                st.session_state.pages_per_session = 6.8
                st.session_state.email_open_rate = 0.95
                st.session_state.email_click_rate = 0.70
                st.session_state.discount_used = "Ya"
                st.session_state.coupon_code = "SALE15"
                st.session_state.support_tickets = 0
                st.session_state.refund_requested = "Tidak"
                st.session_state.delivery_delay_days = 0
                st.session_state.satisfaction_score = 4.8
                st.session_state.nps_score = 10
                st.session_state.marketing_spend_per_user = 5.0
                st.session_state.last_3_month_purchase_freq = 15
                st.rerun()

        with p_col2:
            if st.button("🚨 Load Profil: Risiko Churn Tinggi (High Risk)"):
                st.session_state.gender = "Male"
                st.session_state.age = 22
                st.session_state.country = "USA"
                st.session_state.city = "New York"
                st.session_state.payment_method = "PayPal"
                st.session_state.subscription_type = "Monthly"
                st.session_state.is_premium_user = "Tidak"
                st.session_state.signup_date = datetime(2024, 9, 1).date()
                st.session_state.last_purchase_date = datetime(2024, 9, 15).date()
                st.session_state.total_spent = 45.0
                st.session_state.avg_order_value = 15.0
                st.session_state.lifetime_value = 45.0
                st.session_state.total_visits = 3
                st.session_state.avg_session_time = 1.5
                st.session_state.pages_per_session = 1.2
                st.session_state.email_open_rate = 0.05
                st.session_state.email_click_rate = 0.0
                st.session_state.discount_used = "Tidak"
                st.session_state.coupon_code = "None"
                st.session_state.support_tickets = 6
                st.session_state.refund_requested = "Ya"
                st.session_state.delivery_delay_days = 8
                st.session_state.satisfaction_score = 1.5
                st.session_state.nps_score = 2
                st.session_state.marketing_spend_per_user = 35.0
                st.session_state.last_3_month_purchase_freq = 0
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Main Input Form Divided by Categories
        st.markdown("""
        <div class="section-header" style="border-left: 5px solid #FF4B4B; background: linear-gradient(90deg, rgba(255, 75, 75, 0.1) 0%, rgba(30, 30, 47, 0.2) 100%);">
          <h4>
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 10px; filter: drop-shadow(0 0 4px rgba(255,75,75,0.4));">
              <path d="M17.5 21a5.5 5.5 0 0 0-11 0" stroke="url(#prof-grad)" stroke-width="2" stroke-linecap="round"/>
              <circle cx="12" cy="10" r="4" stroke="url(#prof-grad)" stroke-width="2"/>
              <defs>
                <linearGradient id="prof-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#FF4B4B" />
                  <stop offset="100%" stop-color="#FF8E8E" />
                </linearGradient>
              </defs>
            </svg>
            Profil & Informasi Akun
          </h4>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            gender = st.selectbox("Jenis Kelamin", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(st.session_state.gender))
            age = st.slider("Usia Pelanggan", 5, 100, int(st.session_state.age))
        with col2:
            country = st.selectbox("Negara", ["Germany", "India", "Bangladesh", "USA", "UK"], index=["Germany", "India", "Bangladesh", "USA", "UK"].index(st.session_state.country))
            city = st.selectbox("Kota Domisili", ["London", "Mumbai", "Dhaka", "New York", "Delhi", "Berlin", "Hamburg"], index=["London", "Mumbai", "Dhaka", "New York", "Delhi", "Berlin", "Hamburg"].index(st.session_state.city))
        with col3:
            subscription_type = st.selectbox("Jenis Langganan", ["Monthly", "Annual"], index=["Monthly", "Annual"].index(st.session_state.subscription_type))
            is_premium_user = st.selectbox("Akun Premium?", ["Tidak", "Ya"], index=["Tidak", "Ya"].index(st.session_state.is_premium_user))
            is_premium_val = 1 if is_premium_user == "Ya" else 0
        with col4:
            signup_date = st.date_input("Tanggal Mendaftar", st.session_state.signup_date)
            last_purchase_date = st.date_input("Transaksi Terakhir", st.session_state.last_purchase_date)

        img_base64_cat2 = get_base64_image("static/kategori_2.png")
        if img_base64_cat2:
            st.markdown(f"""
            <div class="section-header" style="border-left: 5px solid #00D4FF; background: linear-gradient(90deg, rgba(0, 212, 255, 0.1) 0%, rgba(30, 30, 47, 0.2) 100%);">
              <h4>
                <img src="data:image/png;base64,{img_base64_cat2}" width="24" height="24" style="vertical-align: middle; margin-right: 10px;" />
                Perilaku & Interaksi Sistem
              </h4>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="section-header" style="border-left: 5px solid #00D4FF; background: linear-gradient(90deg, rgba(0, 212, 255, 0.1) 0%, rgba(30, 30, 47, 0.2) 100%);">
              <h4>
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 10px; filter: drop-shadow(0 0 4px rgba(0,212,255,0.4));">
                  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke="url(#act-grad)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
                  <defs>
                    <linearGradient id="act-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stop-color="#00D4FF" />
                      <stop offset="100%" stop-color="#0072FF" />
                    </linearGradient>
                  </defs>
                </svg>
                Perilaku & Interaksi Sistem
              </h4>
            </div>
            """, unsafe_allow_html=True)
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            total_visits = st.number_input("Total Kunjungan", min_value=0, max_value=1000, value=int(st.session_state.total_visits))
            avg_session_time = st.number_input("Rata-rata Waktu Sesi (Menit)", min_value=0.0, max_value=1000.0, value=float(st.session_state.avg_session_time))
        with col6:
            pages_per_session = st.number_input("Rata-rata Halaman / Sesi", min_value=0.0, max_value=100.0, value=float(st.session_state.pages_per_session))
            delivery_delay_days = st.slider("Keterlambatan Pengiriman (Hari)", 0, 30, int(st.session_state.delivery_delay_days))
        with col7:
            email_open_rate = st.slider("Email Open Rate", 0.0, 1.0, float(st.session_state.email_open_rate))
            email_click_rate = st.slider("Email Click Rate", 0.0, 1.0, float(st.session_state.email_click_rate))
        with col8:
            support_tickets = st.number_input("Jumlah Tiket Komplain", min_value=0, max_value=50, value=int(st.session_state.support_tickets))
            refund_requested = st.selectbox("Pernah Mengajukan Refund?", ["Tidak", "Ya"], index=["Tidak", "Ya"].index(st.session_state.refund_requested))
            refund_val = 1 if refund_requested == "Ya" else 0

        img_base64_cat3 = get_base64_image("static/kategori_3.png")
        if img_base64_cat3:
            st.markdown(f"""
            <div class="section-header" style="border-left: 5px solid #28A745; background: linear-gradient(90deg, rgba(40, 167, 69, 0.1) 0%, rgba(30, 30, 47, 0.2) 100%);">
              <h4>
                <img src="data:image/png;base64,{img_base64_cat3}" width="24" height="24" style="vertical-align: middle; margin-right: 10px;" />
                Finansial, Promosi & Kepuasan
              </h4>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="section-header" style="border-left: 5px solid #28A745; background: linear-gradient(90deg, rgba(40, 167, 69, 0.1) 0%, rgba(30, 30, 47, 0.2) 100%);">
              <h4>
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 10px; filter: drop-shadow(0 0 4px rgba(40,167,69,0.4));">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" stroke="url(#fin-grad)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <defs>
                    <linearGradient id="fin-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stop-color="#28A745" />
                      <stop offset="100%" stop-color="#20C997" />
                    </linearGradient>
                  </defs>
                </svg>
                Finansial, Promosi & Kepuasan
              </h4>
            </div>
            """, unsafe_allow_html=True)
        col9, col10, col11, col12 = st.columns(4)
        with col9:
            total_spent = st.number_input("Total Pembelian ($)", min_value=0.0, max_value=100000.0, value=float(st.session_state.total_spent))
            avg_order_value = st.number_input("Rata-rata Nilai Order ($)", min_value=0.0, max_value=10000.0, value=float(st.session_state.avg_order_value))
        with col10:
            lifetime_value = st.number_input("Lifetime Value ($)", min_value=0.0, max_value=500000.0, value=float(st.session_state.lifetime_value))
            last_3_month_purchase_freq = st.number_input("Frekuensi Order (3 Bln Terakhir)", min_value=0, max_value=100, value=int(st.session_state.last_3_month_purchase_freq))
        with col11:
            discount_used = st.selectbox("Pernah Menggunakan Diskon?", ["Tidak", "Ya"], index=["Tidak", "Ya"].index(st.session_state.discount_used))
            discount_val = 1 if discount_used == "Ya" else 0
            coupon_code = st.selectbox("Kode Kupon Terakhir", ["None", "NEW20", "SALE15", "REF10"], index=["None", "NEW20", "SALE15", "REF10"].index(st.session_state.coupon_code))
            coupon_val = np.nan if coupon_code == "None" else coupon_code
        with col12:
            payment_method = st.selectbox("Metode Pembayaran Utama", ["UPI", "PayPal", "SEPA", "BKash", "Card"], index=["UPI", "PayPal", "SEPA", "BKash", "Card"].index(st.session_state.payment_method))
            marketing_spend_per_user = st.number_input("Biaya Pemasaran Akun ($)", min_value=0.0, max_value=2000.0, value=float(st.session_state.marketing_spend_per_user))

        col13, col14 = st.columns(2)
        with col13:
            satisfaction_score = st.slider("Tingkat Kepuasan Pelanggan (1-5)", 1.0, 5.0, float(st.session_state.satisfaction_score), step=0.1)
        with col14:
            nps_score = st.slider("Skor NPS (Net Promoter Score)", 0, 10, int(st.session_state.nps_score))

        # Predict Button
        if st.button("🔮 JALANKAN PREDIKSI RISIKO CHURN"):
            tenure_days = (last_purchase_date - signup_date).days
            if tenure_days < 0:
                tenure_days = 0
                
            input_dict = {
                'gender': gender,
                'age': age,
                'country': country,
                'city': city,
                'acquisition_channel': 'Organic',
                'device_type': 'Mobile',
                'subscription_type': subscription_type,
                'is_premium_user': is_premium_val,
                'total_visits': total_visits,
                'avg_session_time': avg_session_time,
                'pages_per_session': pages_per_session,
                'email_open_rate': email_open_rate,
                'email_click_rate': email_click_rate,
                'total_spent': total_spent,
                'avg_order_value': avg_order_value,
                'discount_used': discount_val,
                'coupon_code': coupon_val,
                'support_tickets': support_tickets,
                'refund_requested': refund_val,
                'delivery_delay_days': delivery_delay_days,
                'payment_method': payment_method,
                'satisfaction_score': satisfaction_score,
                'nps_score': nps_score,
                'marketing_spend_per_user': marketing_spend_per_user,
                'lifetime_value': lifetime_value,
                'last_3_month_purchase_freq': last_3_month_purchase_freq,
                'tenure_days': tenure_days
            }
            
            input_df = pd.DataFrame([input_dict])
            
            # Apply capping
            for col, limits in cap_limits.items():
                if col in input_df.columns:
                    input_df[col] = input_df[col].clip(lower=limits[0], upper=limits[1])
            
            try:
                pred_prob = pipeline.predict_proba(input_df)[0][1]
                pred_class = pipeline.predict(input_df)[0]
                
                st.markdown("### 📋 Hasil Prediksi & Rekomendasi")
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    if pred_class == 1:
                        st.markdown(f"""
                        <div class="result-card" style="border-left: 6px solid #DC3545;">
                            <div class="metric-label">Status Kelompok Pelanggan</div>
                            <div style="margin: 0.8rem 0;">
                                <span class="custom-badge badge-churn-glow">🚨 HIGH RISK OF CHURN (RISIKO TINGGI)</span>
                            </div>
                            <p style="color: #F8F9FA; font-size: 1rem; line-height: 1.5; margin-bottom: 0;">
                                Pelanggan terdeteksi memiliki probabilitas tinggi untuk berhenti berlangganan atau tidak aktif lagi. 
                                <br><br>
                                <b>Rekomendasi Tindakan:</b>
                                <ol style="margin-top: 5px; padding-left: 20px; color: #ADB5BD;">
                                    <li>Kirimkan kupon diskon loyalitas personal (e.g. kode SALE15).</li>
                                    <li>Lakukan follow-up aktif jika ada tiket keluhan yang belum terselesaikan.</li>
                                    <li>Tingkatkan kualitas onboarding jika pelanggan masih memiliki masa aktif singkat.</li>
                                </ol>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="result-card" style="border-left: 6px solid #198754;">
                            <div class="metric-label">Status Kelompok Pelanggan</div>
                            <div style="margin: 0.8rem 0;">
                                <span class="custom-badge badge-active-glow">✅ LOYAL / ACTIVE (RETENSI AMAN)</span>
                            </div>
                            <p style="color: #F8F9FA; font-size: 1rem; line-height: 1.5; margin-bottom: 0;">
                                Pelanggan ini diklasifikasikan sebagai pelanggan aktif dengan risiko churn yang sangat rendah. 
                                Hubungan mereka dengan sistem stabil.
                                <br><br>
                                <b>Rekomendasi Tindakan:</b>
                                <ol style="margin-top: 5px; padding-left: 20px; color: #ADB5BD;">
                                    <li>Masukkan mereka ke daftar kampanye promosi produk premium baru.</li>
                                    <li>Tawarkan program rujukan (referral program) untuk menarik pelanggan baru.</li>
                                    <li>Pertahankan layanan terbaik tanpa mengganggu mereka dengan email spam.</li>
                                </ol>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                with res_col2:
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="metric-label">Tingkat Risiko Churn</div>
                        <div class="metric-value">{pred_prob * 100:.2f}%</div>
                        <div style="margin-top: 1.5rem;">
                            <div style="height: 10px; width: 100%; background-color: rgba(255, 255, 255, 0.05); border-radius: 5px; overflow: hidden;">
                                <div style="height: 100%; width: {pred_prob * 100}%; background: linear-gradient(90deg, #FF4B4B 0%, #B82525 100%); border-radius: 5px;"></div>
                            </div>
                        </div>
                        <p style="margin-top: 1.5rem; color: #8E9AAF; font-size: 0.9rem;">
                            Persentase di atas menunjukkan keyakinan model terhadap potensi churn pelanggan berdasarkan kombinasi parameter demografis, finansial, dan interaksi yang diinputkan.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Gagal memprediksi churn: {e}")
                
    elif view == "📈 Eksplorasi & Analisis Data":
        img_base64_eda = get_base64_image("static/logo_eda.png")
        if img_base64_eda:
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-top: 1.5rem; margin-bottom: 1rem;">
              <img src="data:image/png;base64,{img_base64_eda}" width="32" height="32" style="vertical-align: middle; margin-right: 12px;" />
              <h3 style="margin: 0; color: #F8F9FA; font-size: 1.6rem; font-weight: 600;">Analisis Eksplorasi Data (EDA)</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("### Analisis Eksplorasi Data (EDA)")
        st.write("Berikut adalah beberapa visualisasi data historis pelanggan yang digunakan untuk membangun model ini.")
        
        img_col1, img_col2 = st.columns(2)
        with img_col1:
            if os.path.exists("static/images/churn_distribution.png"):
                st.image("static/images/churn_distribution.png", caption="Distribusi Churn Pelanggan historis")
            else:
                st.info("Visualisasi distribusi churn belum tersedia.")
                
            if os.path.exists("static/images/missing_values.png"):
                st.image("static/images/missing_values.png", caption="Kolom dengan Data Kosong (%)")
            else:
                st.info("Visualisasi data kosong tidak tersedia atau tidak ada data kosong.")
                
        with img_col2:
            if os.path.exists("static/images/correlation_heatmap.png"):
                st.image("static/images/correlation_heatmap.png", caption="Matriks Korelasi antar Fitur Numerik")
            else:
                st.info("Heatmap korelasi belum tersedia.")
                
            if os.path.exists("static/images/feature_importances.png"):
                st.image("static/images/feature_importances.png", caption="Tingkat Pengaruh Fitur (Feature Importance)")
            else:
                st.info("Visualisasi feature importance belum tersedia.")
                
    elif view == "⚡ Performa Model & Evaluasi":
        st.markdown("### Performa Model & Perbandingan Eksperimen")
        st.write("Halaman ini menyajikan metrik performa model-model yang telah dilatih pada dataset ini berdasarkan 3 skenario eksperimen.")
        
        if os.path.exists("static/model_comparison.csv"):
            comparison_df = pd.read_csv("static/model_comparison.csv")
            for col in ['Accuracy', 'Precision', 'Recall', 'F1-Score']:
                comparison_df[col] = comparison_df[col].map('{:.4f}'.format)
            
            st.dataframe(comparison_df[['Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score']], use_container_width=True)
            
            st.markdown("""
            > 💡 **Analisis Performa**:
            > * **Direct Modeling** melatih model secara langsung tanpa penskalaan (*scaling*) atau pembersihan mendalam.
            > * **Preprocessed Modeling** menerapkan normalisasi (*scaling*), penanganan nilai kosong (*imputation*), dan *feature engineering* (seperti menghitung durasi berlangganan / *tenure*). Hal ini biasanya meningkatkan akurasi dan stabilitas model secara signifikan.
            > * **Tuned Modeling** mengoptimalkan hyperparameter terbaik menggunakan metode *GridSearchCV* untuk mendapatkan performa F1-Score yang paling optimal.
            """)
        else:
            st.info("Tabel perbandingan performa model akan muncul di sini setelah Anda menjalankan skrip `notebook_uas.py`.")
