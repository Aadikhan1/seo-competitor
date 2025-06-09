import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="SEO Backlink Filter Tool", layout="wide")
st.title("🔗 SEO Backlink Filter Tool")

uploaded_file = st.file_uploader("📤 Upload Excel file with backlinks", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ File uploaded successfully!")

        st.subheader("📊 Preview Data")
        st.dataframe(df.head())

        st.markdown("---")
        st.subheader("🎯 Apply SEO Filters")

        columns = df.columns.tolist()
        selected_columns = st.multiselect("Select columns to filter/search", columns, default=columns)

        filters = {}
        for col in selected_columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                min_val = float(df[col].min())
                max_val = float(df[col].max())
                if min_val == max_val:
                    min_val -= 1 if min_val > 0 else -1
                    max_val += 1 if max_val >= 0 else -1
                filters[col] = st.slider(f"{col} range",
                                         min_value=min_val,
                                         max_value=max_val,
                                         value=(min_val, max_val))
            else:
                unique_vals = df[col].dropna().unique().tolist()
                filters[col] = st.multiselect(f"Select {col}", unique_vals, default=unique_vals)

        filtered_df = df.copy()
        for col, val in filters.items():
            if pd.api.types.is_numeric_dtype(df[col]):
                filtered_df = filtered_df[(filtered_df[col] >= val[0]) & (filtered_df[col] <= val[1])]
            else:
                filtered_df = filtered_df[filtered_df[col].isin(val)]

        st.markdown("### 🔍 Search within Filtered Results")
        search_col = st.selectbox("Select column to search", selected_columns)
        search_term = st.text_input("Enter search term")
        if search_term:
            filtered_df = filtered_df[filtered_df[search_col].astype(str).str.contains(search_term, case=False)]

        st.markdown("### ✅ Filtered Data")
        st.dataframe(filtered_df)

        def convert_df_to_excel(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Filtered_Backlinks')
            return output.getvalue()

        st.download_button(
            label="📥 Download Filtered Data",
            data=convert_df_to_excel(filtered_df),
            file_name='filtered_backlinks.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

        if st.button("🔄 Reset Filters"):
            st.experimental_rerun()

    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")
else:
    st.info("📝 Please upload an Excel file to begin.")
