import streamlit as st
import pandas as pd
import time
from scholarly import scholarly

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="IIHR Research Performance Dashboard",
    layout="wide"
)

# ==============================
# LOAD DATA
# ==============================
DATA_FILE = "scholar_metrics_fetched.csv"
df = pd.read_csv(DATA_FILE)

# ==============================
# DATA CLEANING
# ==============================
df["Fetched H-index"] = pd.to_numeric(df["Fetched H-index"], errors="coerce")
df["Fetched Citations"] = pd.to_numeric(df["Fetched Citations"], errors="coerce")

# ==============================
# PERFORMANCE SCORE
# ==============================
df["norm_citations"] = df["Fetched Citations"] / df["Fetched Citations"].max()
df["norm_hindex"] = df["Fetched H-index"] / df["Fetched H-index"].max()

df["Performance Score"] = (
    0.6 * df["norm_citations"] +
    0.4 * df["norm_hindex"]
)

def classify_performance(score):
    if score >= 0.66:
        return "High"
    elif score >= 0.33:
        return "Medium"
    else:
        return "Low"

df["Performance Category"] = df["Performance Score"].apply(classify_performance)

# ==============================
# HEADER
# ==============================
st.title("📊 IIHR Research Performance Dashboard")
st.caption(
    "Semi-automated bibliometric analysis using Google Scholar profile links"
)

# ==============================
# KPI METRICS
# ==============================
total_scientists = len(df)
avg_hindex = df["Fetched H-index"].mean()
total_citations = df["Fetched Citations"].sum()
coverage = df["Fetched H-index"].notna().mean() * 100
iihr_score = df["Performance Score"].mean()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("👨‍🔬 Scientists", total_scientists)
col2.metric("📈 Avg H-Index", f"{avg_hindex:.2f}")
col3.metric("📚 Total Citations", f"{int(total_citations):,}")
col4.metric("✅ Profiles Fetched", f"{coverage:.1f}%")
col5.metric("🏛️ IIHR Score", f"{iihr_score:.3f}")

st.divider()

# ==============================
# TOP PERFORMERS
# ==============================
st.subheader("🏆 Top 10 Scientists by Performance Score")

top10 = df.sort_values("Performance Score", ascending=False).head(10)
st.dataframe(
    top10[
        [
            "Full Name of Scientist",
            "Fetched H-index",
            "Fetched Citations",
            "Performance Score",
            "Performance Category"
        ]
    ],
    use_container_width=True
)

st.divider()

# ==============================
# PERFORMANCE CATEGORY DISTRIBUTION
# ==============================
st.subheader("📊 Performance Category Distribution")
st.bar_chart(df["Performance Category"].value_counts())

st.divider()

# ==============================
# DATA QUALITY REPORT
# ==============================
st.subheader("🧪 Data Quality & Coverage Report")

missing_links = df["Google Scholar Profile Link"].isna().sum()
missing_metrics = df["Fetched H-index"].isna().sum()

col1, col2 = st.columns(2)
col1.metric("❌ Missing Scholar Links", missing_links)
col2.metric("⚠️ Profiles Without Metrics", missing_metrics)

st.divider()

# ==============================
# MANUAL SCHOLAR LINK UPDATE
# ==============================
st.subheader("🛠️ Update Missing Google Scholar Profiles")

missing_df = df[df["Fetched H-index"].isna()]

def extract_author_id(url):
    if isinstance(url, str) and "user=" in url:
        return url.split("user=")[1].split("&")[0]
    return None

if missing_df.empty:
    st.success("All scientist profiles are complete 🎉")
else:
    selected_name = st.selectbox(
        "Select Scientist",
        missing_df["Full Name of Scientist"].tolist()
    )

    new_link = st.text_input(
        "Paste Google Scholar Profile Link",
        placeholder="https://scholar.google.com/citations?user=XXXX"
    )

    if st.button("🔄 Fetch & Update Metrics"):
        if not new_link:
            st.error("Please enter a valid Google Scholar link.")
        else:
            with st.spinner("Fetching data from Google Scholar..."):
                try:
                    author_id = extract_author_id(new_link)
                    author = scholarly.search_author_id(author_id)
                    author = scholarly.fill(author)

                    hindex = author.get("hindex")
                    citations = author.get("citedby")

                    df.loc[
                        df["Full Name of Scientist"] == selected_name,
                        ["Google Scholar Profile Link", "Fetched H-index", "Fetched Citations"]
                    ] = [new_link, hindex, citations]

                    df.to_csv(DATA_FILE, index=False)

                    st.success(
                        f"Updated successfully ✅ | h-index: {hindex}, citations: {citations}"
                    )

                    time.sleep(1)
                    st.experimental_rerun()

                except Exception as e:
                    st.error(f"Failed to fetch data: {e}")

st.divider()

# ==============================
# FULL DATASET
# ==============================
st.subheader("📄 Complete Scientist Dataset")
st.dataframe(df, use_container_width=True)

# ==============================
# EXPORT
# ==============================
st.subheader("📤 Export Updated Data")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download IIHR Performance Dataset",
    data=csv_data,
    file_name="iihr_research_performance.csv",
    mime="text/csv"
)

st.caption("Last updated via Google Scholar semi-automated extraction")