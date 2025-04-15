import streamlit as st
import pandas as pd
from utils import generate_code_from_columns
import io

st.set_page_config(page_title="Code Generator", layout="centered")

st.title("🔠 8 - Alpha Code Generator")

uploaded_file = st.file_uploader("Upload your base file (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")

        st.dataframe(df.head())

        st.markdown("---")

        st.subheader("📌 Select Columns for Code Generation")

        column_inputs = []
        num_cols = st.session_state.get("num_cols", 1)

        for i in range(num_cols):
            col_name = st.selectbox(f"Select Column #{i+1}", df.columns, key=f"col_{i}")
            column_inputs.append(col_name)

        if st.button("➕ Add Column"):
            st.session_state.num_cols = num_cols + 1
            st.rerun()

        st.subheader("📝 Output Column Name")
        target_column = st.text_input("Enter new column name to store generated code", value="CodeTRG")

        if st.button("🚀 Generate Code"):
            if column_inputs and target_column:
                df = generate_code_from_columns(df, column_inputs, target_column)
                st.success("Code generation completed!")

                st.dataframe(df.head())

                output = io.BytesIO()
                df.to_excel(output, index=False, engine='openpyxl')
                st.download_button("📥 Download File", output.getvalue(), file_name="output_with_code.xlsx")
            else:
                st.warning("Please select at least one column and enter a target column name.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
