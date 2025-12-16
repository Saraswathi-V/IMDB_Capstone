# streamlit_app.py: Streamlit dashboard for IMDb Big Data Analytics
import streamlit as st
import pandas as pd
from pymongo import MongoClient

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="IMDb Big Data Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #f5c518;
    }
    .kpi-box {
        background: linear-gradient(135deg, #1f2937, #111827);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    }
    .kpi-title {
        font-size: 18px;
        color: #9ca3af;
    }
    .kpi-value {
        font-size: 36px;
        font-weight: bold;
        color: #f5c518;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- DATABASE ----------------
client = MongoClient("mongodb://localhost:27017")
db = client["imdb_capstone"]


@st.cache_data
def load_collection(name: str) -> pd.DataFrame:
    data = list(db[name].find({}, {"_id": 0}))
    return pd.DataFrame(data)


# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;'>
        🎬 IMDb Big Data Analytics Dashboard
    </h1>
    <p style='text-align:center; color:#9ca3af;'>
        Powered by MongoDB • Pandas • Streamlit
    </p>
    """,
    unsafe_allow_html=True,
)

# ---------------- LOAD DATA ----------------
genre_df = load_collection("movies_by_genre")
year_df = load_collection("movies_by_year")
top_df = load_collection("top_movies")

# ---------------- VALIDATION ----------------
if genre_df.empty or "genres" not in genre_df.columns:
    st.error("❌ movies_by_genre data not available. Run aggregation.")
    st.stop()

if year_df.empty:
    st.error("❌ movies_by_year data not available.")
    st.stop()

if top_df.empty:
    st.error("❌ top_movies data not available.")
    st.stop()

# ---------------- KPI METRICS ----------------
st.markdown("## 📊 Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="kpi-title">🎞️ Total Movies</div>
            <div class="kpi-value">{top_df.shape[0]:,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="kpi-title">🎭 Genres</div>
            <div class="kpi-value">{genre_df['genres'].nunique()}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-box">
            <div class="kpi-title">📅 Years Covered</div>
            <div class="kpi-value">{year_df['startYear'].nunique()}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ---------------- GENRE BAR CHART ----------------
st.subheader("🎭 Top 10 Genres by Movie Count")

top_genres = genre_df.head(10).set_index("genres")

st.bar_chart(
    top_genres["movie_count"],
    height=400
)

st.divider()

# ---------------- YEAR LINE CHART ----------------
st.subheader("📈 Movies Released Per Year")

year_df_clean = year_df[year_df["startYear"] >= 1900]

st.line_chart(
    year_df_clean.set_index("startYear")["movie_count"],
    height=400
)

st.divider()

# ---------------- TOP MOVIES TABLE ----------------
st.subheader("⭐ Top Rated Movies (Min 10k Votes)")

st.dataframe(
    top_df[["primaryTitle", "averageRating", "numVotes"]]
        .rename(
            columns={
                "primaryTitle": "Movie Title",
                "averageRating": "IMDb Rating",
                "numVotes": "Votes",
            }
        )
        .head(15),
    use_container_width=True,
)

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style='text-align:center; color:#6b7280;'>
        📽️ IMDb Capstone Project • Big Data Engineering
    </p>
    """,
    unsafe_allow_html=True,
)
