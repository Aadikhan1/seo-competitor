import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Advanced Website Category Filter Tool", layout="wide")
st.title("🕵️ Advanced Website Category Filter Tool")

uploaded_file = st.file_uploader("📤 Upload your website data file (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")
        st.dataframe(df.head())

        st.markdown("---")
        st.subheader("🧠 Apply Filters")

        st.markdown("### 📈 Traffic Filter")
        if 'Traffic' in df.columns:
            min_traffic, max_traffic = st.slider("Select Traffic Range",
                                                 float(df['Traffic'].min()),
                                                 float(df['Traffic'].max()),
                                                 (float(df['Traffic'].min()), float(df['Traffic'].max())))
        else:
            st.warning("No 'Traffic' column found for filtering.")

        st.markdown("### 📂 Category Filters")

        categories = {
            "WorkGine Focus": ["💻 Software & SaaS", "📈 Digital Marketing & SEO", "🏢 Business & Finance"],
            "Website Purpose": ["📝 Blog / Guest Posting", "🛠️ Service-Based", "🛒 E-commerce"],
            "General": ["💼 Business", "⚙️ Tech", "👗 Fashion", "⚽ Sports", "✈️ Travel", "₿ Crypto",
                        "💰 Finance", "📚 Education", "🏥 Health", "⚖️ Law", "🌟 Lifestyle", "💒 Wedding",
                        "🐕 Pets", "📸 Photography", "🎬 Entertainment", "🍕 Food"],
            "Geography": ["Argentina", "Australia", "Austria", "Belgium", "Brazil", "Canada", "China",
                          "Denmark", "Dubai (UAE)", "Estonia", "France", "Germany", "India", "Ireland",
                          "Italy", "Japan", "Mexico", "Netherlands", "New Zealand", "Norway", "Pakistan",
                          "Philippines", "Russia", "Singapore", "South Africa", "Spain", "Sweden",
                          "Switzerland", "UAE", "UK", "USA", "Other"],
            "TLD": [".ae", ".ai", ".app", ".at", ".au", ".be", ".br", ".ca", ".ch", ".cn", ".co", ".co.in",
                    ".co.jp", ".co.nz", ".co.uk", ".co.za", ".com", ".com.ar", ".com.au", ".com.br",
                    ".com.cn", ".com.es", ".com.mx", ".com.ph", ".com.pk", ".com.sg", ".de", ".dev", ".dk",
                    ".ee", ".es", ".fr", ".ie", ".in", ".io", ".it", ".jp", ".mx", ".net", ".nl", ".no",
                    ".online", ".org", ".ph", ".pk", ".ru", ".se", ".sg", ".site", ".store", ".tech",
                    ".us", ".xyz", ".za", "Other"]
        }

        selected_filters = {}
        for group, options in categories.items():
            selected_filters[group] = st.multiselect(f"{group}", options)

        filtered_df = df.copy()

        if 'Traffic' in df.columns:
            filtered_df = filtered_df[(filtered_df['Traffic'] >= min_traffic) & (filtered_df['Traffic'] <= max_traffic)]

        for key, values in selected_filters.items():
            if values:
                combined = '|'.join([str(v).replace("(", "\\(").replace(")", "\\)") for v in values])
                filtered_df = filtered_df[filtered_df.astype(str).apply(lambda row: row.str.contains(combined, case=False).any(), axis=1)]

        st.markdown("### 🔍 Search")
        search_column = st.selectbox("Search in column", df.columns)
        search_term = st.text_input("Search term")
        if search_term:
            filtered_df = filtered_df[filtered_df[search_column].astype(str).str.contains(search_term, case=False)]

        st.markdown("### ✅ Filtered Results")
        st.dataframe(filtered_df)

        def convert_df(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()

        st.download_button(
            "📥 Download Filtered Data",
            data=convert_df(filtered_df),
            file_name="filtered_competitor_websites.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        if st.button("🔄 Reset All"):
            st.experimental_rerun()

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("📂 Please upload a CSV or Excel file to begin.")
