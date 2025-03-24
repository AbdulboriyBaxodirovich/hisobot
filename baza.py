import streamlit as st
import pandas as pd
import os

def get_saved_files():
    folder_path = "kirim_data"
    if not os.path.exists(folder_path):
        return []
    return [f for f in os.listdir(folder_path) if f.endswith(".csv")]

def load_data(file_name):
    file_path = os.path.join("kirim_data", file_name)
    return pd.read_csv(file_path) if os.path.exists(file_path) else pd.DataFrame()

def show_baza():
    st.header("Baza Bo‘limi")
    
    files = get_saved_files()
    if not files:
        st.write("Hali hech qanday ma'lumot saqlanmagan.")
        return
    
    selected_file = st.selectbox("Fayl tanlang", files, key="selected_file")
    
    if st.button("Ko‘rish"):
        data = load_data(selected_file)
        if not data.empty:
            st.write(f"### {selected_file} ma'lumotlari")
            st.dataframe(data, height=300, width=700)
        else:
            st.warning("Fayl bo‘sh yoki yuklab bo‘lmadi.")
    
    if st.button("Qayta yuklash"):
        data = load_data(selected_file)
        if not data.empty:
            st.session_state["kirim_data"] = data
            st.success("Ma'lumotlar qayta yuklandi va oynaga joylandi!")
        else:
            st.error("Faylni yuklashda xatolik yuz berdi!")
