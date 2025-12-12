# Voice of Customer Intelligence Engine (AI & NLP)

### [ Launch Live App](https://voice-of-customer-dashboard-bhyyzfltanzvbqr6ihhtgj.streamlit.app/)

![Dashboard Screenshot](https://via.placeholder.com/800x400?text=Upload+Your+Actual+Screenshot+Here)
*(Tip: Replace this link with a screenshot of your colorful dashboard)*

## THE BUSINESS PROBLEM 
E-commerce companies collect thousands of reviews, but 90% of this data is unstructured text. Analyzing it manually is impossible, leading to **missed revenue opportunities** and **unresolved churn drivers**.

## THE SOLUTION
I built an end-to-end intelligence engine that:
1.  **Ingests** raw customer data (CSV).
2.  **Cleans & Classifies** sentiment using proxy-labeling logic.
3.  **Visualizes** trends interactively via a Streamlit web app.
4.  **Prescribes** strategy using **Meta Llama 3.3 (70B)** to answer business questions automatically.

## TECH STACK
* **Core:** Python 3.10+
* **Data Processing:** Pandas
* **App Framework:** Streamlit
* **AI/LLM:** Groq API (Meta Llama 3.3)
* **Visualization:** Plotly Express

## AI ITEGRATION
This project integrates the **Groq API** to leverage the **Llama 3.3-70b** model.
* **Architecture:** It samples live filtered data, constructs a prompt context, and retrieves strategic insights in <2 seconds.
* **Use Case:** Stakeholders can ask *"Why are customers returning items?"* and receive a summarized, evidence-based answer.

## HOW TO RUN LOCALLY
1. Clone the repo:
   ```bash
   git clone [https://github.com/samiksha-deswal/voice-of-customer-dashboard.git](https://github.com/samiksha-deswal/voice-of-customer-dashboard.git)

2. Install dependencies:
   pip install -r requirements.txt

3. Run the app:
   streamlit run app.py

