import streamlit as st
import pandas as pd
from backend import find_best_match, update_yaml, calculate_expenses


# Configurar la página
st.set_page_config(page_title="FamilyLedger Extractor", layout="wide")

st.title("FamilyLedger")

# Cargar archivos HTML
uploaded_file = st.file_uploader("Upload a file", type=["csv"], accept_multiple_files=False)

if uploaded_file:

    df = pd.read_csv(uploaded_file, encoding="utf-8")
    df = df.drop(columns=["Fecha valor", "Moneda", "Entidad", "Tipo de producto", "Nombre de producto"])
    df.columns = df.columns.str.replace("Fecha de operación", "Fecha")
    df.columns = df.columns.str.replace("Tipo de movimiento", "Tipo")

    df["Nota"] = df["Concepto"].apply(find_best_match)

    # Guardar datos en session_state para mantener ediciones
    if 'df' not in st.session_state:
        st.session_state.df = df

    st.header("CSV data table")
    edited_df = st.data_editor(st.session_state.df, num_rows="dynamic")

    if st.button("Update translations"):
        update_yaml(edited_df)

    if st.button("Export expenses"):
        st.header("Calculated expenses")
        exp = calculate_expenses(edited_df)
        st.dataframe(exp)

