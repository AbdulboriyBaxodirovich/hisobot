import streamlit as st
import kirim
import chiqim
import baza

# Sahifa konfiguratsiyasi
st.set_page_config(page_title="Hisobot", layout="wide")

# Yon paneldagi menyu
with st.sidebar:
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #003366 !important;
        }
        .sidebar .stButton>button {
            background-color: #003366 !important;
            color: white !important;
            border: none !important;
            width: 100% !important;
            padding: 10px !important;
            font-size: 18px !important;
        }
        .sidebar .stButton>button:hover {
            opacity: 0.8 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    menu_options = ["Asosiy", "Kirim", "Chiqim", "Baza"]
    if "selected_menu" not in st.session_state:
        st.session_state["selected_menu"] = "Asosiy"
    
    for menu_name in menu_options:
        if st.button(menu_name, key=menu_name):
            st.session_state["selected_menu"] = menu_name

# Asosiy sahifa tarkibi
st.title("Hisobot")

if st.session_state["selected_menu"] == "Asosiy":
    st.header("Asosiy Bo'lim")
    st.write("Bu yerda umumiy hisobotlar ko'rsatiladi.")

elif st.session_state["selected_menu"] == "Kirim":
    kirim.show_kirim()

elif st.session_state["selected_menu"] == "Chiqim":
    chiqim.show_chiqim()

elif st.session_state["selected_menu"] == "Baza":
    baza.show_baza()