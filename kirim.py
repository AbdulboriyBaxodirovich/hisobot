import streamlit as st
import pandas as pd
import os
from datetime import datetime

def is_month_end():
    if not st.session_state["kirim_data"].empty:
        last_date = st.session_state["kirim_data"].iloc[-1]["Sana"]
        try:
            date_obj = datetime.strptime(last_date, "%d.%m.%Y")
            next_day = date_obj.replace(day=28) + pd.DateOffset(days=4)
            month_end = next_day - pd.DateOffset(days=next_day.day)
            return date_obj.date() == month_end.date()
        except ValueError:
            return False
    return False

def save_monthly_data():
    if not st.session_state["kirim_data"].empty and is_month_end():
        last_date = st.session_state["kirim_data"].iloc[-1]["Sana"]
        try:
            date_obj = datetime.strptime(last_date, "%d.%m.%Y")
            month_year = date_obj.strftime("%m.%Y")
            file_name = f"kirim_{month_year}.csv"
            folder_path = "kirim_data"
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, file_name)
            
            st.session_state["kirim_data"].to_csv(file_path, index=False)
            st.session_state["kirim_data"] = pd.DataFrame(columns=["Sana", "Kategoriya", "Summa"])
            st.success(f"{month_year} oyning ma'lumotlari saqlandi va oynaga qaytildi!")
        except ValueError:
            st.error("Sanani noto'g'ri formatda kiritdingiz!")

def show_kirim():
    st.header("Kirim Bo'limi")
    st.write("Bu yerda kirim ma'lumotlari kiritiladi va hisoblanadi.")

    if "kirim_data" not in st.session_state:
        st.session_state["kirim_data"] = pd.DataFrame(columns=["Sana", "Kategoriya", "Summa"])

    kategoriyalar = ["Do'kon1", "Do'kon2", "Do'kon3"]

    sana = st.text_input("Sana (01.01.2025 formatida)", key="sana")
    if st.session_state["sana"].endswith("\n"):
        st.session_state["kategoriya_focus"] = True
    
    kategoriya = st.selectbox("Kategoriya", kategoriyalar, key="kategoriya")
    if "kategoriya_focus" in st.session_state and st.session_state["kategoriya_focus"]:
        st.session_state["kategoriya_focus"] = False
        st.session_state["summa_focus"] = True
    
    summa = st.text_input("Summa", key="summa", value="", placeholder="0")
    if "summa_focus" in st.session_state and st.session_state["summa_focus"]:
        st.session_state["summa_focus"] = False
        st.session_state["submit_kirim"] = True
    
    if "submit_kirim" in st.session_state and st.session_state["submit_kirim"]:
        st.session_state["submit_kirim"] = False
        if summa.strip():
            yangi_qator = pd.DataFrame([[sana.strip(), kategoriya, float(summa)]], columns=["Sana", "Kategoriya", "Summa"])
            st.session_state["kirim_data"] = pd.concat([st.session_state["kirim_data"], yangi_qator], ignore_index=True)
    
    if st.button("Qo'shish"):
        if summa.strip():
            yangi_qator = pd.DataFrame([[sana, kategoriya, float(summa)]], columns=["Sana", "Kategoriya", "Summa"])
            st.session_state["kirim_data"] = pd.concat([st.session_state["kirim_data"], yangi_qator], ignore_index=True)
    
    st.write("### Kirim Jadvali")
    st.dataframe(st.session_state["kirim_data"], height=300, width=700)
    
    st.write("### Kategoriya bo'yicha filtrlash")
    selected_kategoriya = st.selectbox("Kategoriya tanlang", ["Hammasi"] + kategoriyalar, key="filter_kategoriya")
    if selected_kategoriya == "Hammasi":
        umumiy_summa = st.session_state["kirim_data"]["Summa"].sum() if not st.session_state["kirim_data"].empty else 0
        umumiy_kategoriya = "Umumiy"
    else:
        filtered_data = st.session_state["kirim_data"][st.session_state["kirim_data"]["Kategoriya"] == selected_kategoriya]
        umumiy_summa = filtered_data["Summa"].sum() if not filtered_data.empty else 0
        umumiy_kategoriya = selected_kategoriya
    
    umumiy_df = pd.DataFrame([["", umumiy_kategoriya, umumiy_summa]], columns=["Sana", "Kategoriya", "Summa"])
    
    st.write("### Umumiy")
    st.table(umumiy_df)
    
    if is_month_end():
        save_monthly_data()
