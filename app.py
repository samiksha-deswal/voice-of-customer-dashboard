#!/usr/bin/env python3
"""
app.py

Streamlit + Plotly app for visualizing Olist cleaned review data.

Features:
- Page title: "Voice of Customer Intelligence Engine"
- Loads cleaned_reviews.csv (cached with st.cache_data)
- Sidebar multiselect for Sentiment_Category
- KPI row (Total, Positive, Negative reviews)
- Pie chart of sentiment distribution
- Bar chart of review_score distribution (top 5)
- AI Insight Search: filter reviews by keyword in comment text
- Handles missing values gracefully
"""

import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path


# ---- Page Config ----
st.set_page_config(
    page_title="Voice of Customer Intelligence Engine",
    layout="wide"
)

st.title("Voice of Customer Intelligence Engine")


# ---- Data Loading ----
@st.cache_data
def load_data(csv_path: str) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        st.error(f"Data file not found: {csv_path}")
        st.stop()

    df = pd.read_csv(path, encoding="utf-8")

    # Ensure we have a sentiment category column
    # Try to standardize to 'Sentiment_Category'
    if "Sentiment_Category" in df.columns:
        df["Sentiment_Category"] = df["Sentiment_Category"].fillna("Unknown")
    elif "sentiment_label" in df.columns:
        df["Sentiment_Category"] = df["sentiment_label"].fillna("Unknown")
    elif "sentiment_polarity" in df.columns:
        # Reconstruct categories from polarity if needed
        def categorize(p):
            try:
                if p > 0.1:
                    return "Positive"
                elif p < -0.1:
                    return "Negative"
                else:
                    return "Neutral"
            except Exception:
                return "Unknown"

        df["Sentiment_Category"] = df["sentiment_polarity"].apply(categorize)
    else:
        # Fallback: everything Unknown, but app still works
        df["Sentiment_Category"] = "Unknown"

    # Ensure review_score exists and is numeric
    if "review_score" in df.columns:
        df["review_score"] = pd.to_numeric(df["review_score"], errors="coerce")
    else:
        # Create a dummy column so charts don't break (will just be NaN)
        df["review_score"] = pd.Series([None] * len(df))

    # Ensure review_comment_message exists
    if "review_comment_message" not in df.columns:
        df["review_comment_message"] = ""

    # Clean up NaNs in comment for search/filtering
    df["review_comment_message"] = df["review_comment_message"].fillna("")

    return df


df = load_data("cleaned_reviews.csv")

if df.empty:
    st.warning("The dataset is empty after loading. Please check cleaned_reviews.csv.")
    st.stop()


# ---- Sidebar Filters ----
st.sidebar.header("Filters")

sentiment_options = sorted(df["Sentiment_Category"].dropna().unique().tolist())
selected_sentiments = st.sidebar.multiselect(
    "Sentiment Category",
    options=sentiment_options,
    default=sentiment_options
)

if selected_sentiments:
    filtered_df = df[df["Sentiment_Category"].isin(selected_sentiments)].copy()
else:
    # If user deselects all, show everything (or you could choose to show none)
    filtered_df = df.copy()


# ---- KPI Row ----
total_reviews = len(filtered_df)

positive_reviews = len(
    filtered_df[filtered_df["Sentiment_Category"] == "Positive"]
    if "Sentiment_Category" in filtered_df.columns
    else []
)

negative_reviews = len(
    filtered_df[filtered_df["Sentiment_Category"] == "Negative"]
    if "Sentiment_Category" in filtered_df.columns
    else []
)

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

kpi_col1.metric("Total Reviews", f"{total_reviews:,}")
kpi_col2.metric("Positive Reviews", f"{positive_reviews:,}")
kpi_col3.metric("Negative Reviews", f"{negative_reviews:,}")


# ---- Charts Row ----
chart_col1, chart_col2 = st.columns(2)

# Pie Chart - Sentiment distribution
with chart_col1:
    st.subheader("Sentiment Distribution")

    if not filtered_df.empty:
        sentiment_counts = (
            filtered_df.groupby("Sentiment_Category")
            .size()
            .reset_index(name="count")
        )

        if not sentiment_counts.empty:
            fig_pie = px.pie(
                sentiment_counts,
                names="Sentiment_Category",
                values="count",
                hole=0.3,
            )
            fig_pie.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No sentiment data available for the selected filters.")
    else:
        st.info("No data available for the selected filters.")

# Bar Chart - Review score distribution (top 5)
with chart_col2:
    st.subheader("Review Score Distribution (Top 5)")

    # Only consider non-null scores
    score_df = filtered_df.dropna(subset=["review_score"])
    if not score_df.empty:
        score_counts = (
            score_df.groupby("review_score")
            .size()
            .reset_index(name="count")
        )

        # Top 5 by count (for Olist this will usually be all scores 1-5)
        score_counts = score_counts.sort_values("count", ascending=False).head(5)
        score_counts = score_counts.sort_values("review_score")

        fig_bar = px.bar(
            score_counts,
            x="review_score",
            y="count",
            labels={"review_score": "Review Score", "count": "Number of Reviews"},
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No valid review_score data available for the selected filters.")


# ---- AI Insight Search ----
st.markdown("---")
st.subheader("AI Insight Search")

search_term = st.text_input(
    "Type a word or phrase (e.g., 'delivery', 'atraso', 'produto') "
    "to filter reviews containing that text:"
)

if search_term:
    # Case-insensitive contains search on the filtered_df
    insight_mask = filtered_df["review_comment_message"].fillna("").str.contains(
        search_term, case=False, na=False
    )
    insight_df = filtered_df[insight_mask].copy()

    st.write(f"Found **{len(insight_df)}** review(s) containing “{search_term}”.")

    if not insight_df.empty:
        # Show a subset of the most relevant columns if they exist
        columns_to_show = []
        for col in ["review_score", "Sentiment_Category", "review_comment_message"]:
            if col in insight_df.columns:
                columns_to_show.append(col)

        if columns_to_show:
            st.dataframe(
                insight_df[columns_to_show],
                use_container_width=True,
            )
        else:
            st.dataframe(insight_df, use_container_width=True)
    else:
        st.info("No reviews matched your search term.")
else:
    st.caption("Enter a keyword above to search within the selected reviews.")
