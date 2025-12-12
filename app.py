import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Voice of Customer Intelligence Engine")
st.title("Voice of Customer Intelligence Engine")

# 2. Load Data
@st.cache_data
def load_data():
    return pd.read_csv('cleaned_reviews.csv')

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filters")
sentiment_filter = st.sidebar.multiselect(
    "Sentiment Category",
    options=df['Sentiment_Category'].unique(),
    default=df['Sentiment_Category'].unique()
)

filtered_df = df[df['Sentiment_Category'].isin(sentiment_filter)]

# 4. KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Reviews", len(filtered_df))
col2.metric("Positive Reviews", len(filtered_df[filtered_df['Sentiment_Category'] == 'Positive']))
col3.metric("Negative Reviews", len(filtered_df[filtered_df['Sentiment_Category'] == 'Negative']))

# 5. Visualizations
col_chart1, col_chart2 = st.columns(2)
with col_chart1:
    st.subheader("Sentiment Distribution")
    fig_pie = px.pie(filtered_df, names='Sentiment_Category', 
                     color='Sentiment_Category',
                     color_discrete_map={'Positive':'#636EFA', 'Negative':'#EF553B', 'Neutral':'#FECB52'})
    st.plotly_chart(fig_pie, use_container_width=True)

with col_chart2:
    st.subheader("Review Score Distribution")
    fig_bar = px.histogram(filtered_df, x='review_score', nbins=5, text_auto=True)
    st.plotly_chart(fig_bar, use_container_width=True)

# --- 6. FREE LLAMA 3 INTEGRATION (GROQ) ---
st.markdown("---")
st.subheader("🤖 AI Strategic Advisor (Powered by Llama 3)")

# Initialize Groq Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

user_question = st.text_input("Ask the AI about your data (e.g., 'What are the top complaints?')")

if st.button("Generate Insight"):
    if user_question:
        with st.spinner("Consulting Llama 3..."):
            # Sample data to save tokens
            sample_reviews = filtered_df['review_comment_message'].dropna().sample(min(50, len(filtered_df))).tolist()
            reviews_text = "\n".join(sample_reviews)
            
            prompt = f"""
            You are a Senior Business Analyst. 
            Analyze the following customer reviews and answer the user's question: "{user_question}"
            
            Focus on actionable business insights.
            
            Reviews:
            {reviews_text}
            """
            
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="llama-3.3-70b-versatile", # Free, Fast, Open Source Model
                )
                
                insight = chat_completion.choices[0].message.content
                st.success("Analysis Complete")
                st.markdown(insight)
            except Exception as e:
                st.error(f"Error communicating with AI: {e}")
    else:
        st.warning("Please enter a question first.")