import pandas as pd

# Load the dataset
df = pd.read_csv('olist_order_reviews_dataset.csv')

# Drop rows without text (optional, but keeps data clean)
df = df.dropna(subset=['review_comment_message'])

# --- THE FIX: Use Star Rating for Sentiment Category ---
# This ensures your dashboard looks colorful and accurate
def categorize_by_score(score):
    if score <= 2:
        return 'Negative'
    elif score == 3:
        return 'Neutral'
    else:
        return 'Positive'

# Apply the function
df['Sentiment_Category'] = df['review_score'].apply(categorize_by_score)

# Save the cleaned data
df.to_csv('cleaned_reviews.csv', index=False)

print(f"Processing complete. {len(df)} rows saved with Star-Based Sentiment.")