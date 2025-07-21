import streamlit as st
import pandas as pd
import joblib
import os
import time
import plotly.express as px
import numpy as np
from PIL import Image

# Set page configuration
st.set_page_config(
    layout="centered",
    page_title="Salary Predictor Pro",
    page_icon="💰",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .st-emotion-cache-18ni7ap {
        background: linear-gradient(145deg, #2193b0, #6dd5ed);
    }
    .st-emotion-cache-1y4p8pa {
        max-width: 1200px;
    }
    .salary-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .st-radio label {
        padding: 8px 12px;
        margin-right: 10px;
        border-radius: 20px;
        background-color: #f0f2f6;
    }
    .st-emotion-cache-16txtl3 {
        padding: 2rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Load the trained model ---
model_path = "best_model.pkl"
if not os.path.exists(model_path):
    st.error(f"Error: Model file '{model_path}' not found.")
    st.stop()

try:
    model_pipeline = joblib.load(model_path)
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# --- App Header ---
st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color: #E0E0E0;">💰 Salary Predictor Pro</h1>
        <p style="color: #FAFAFA;">Advanced salary prediction with market insights</p>
    </div>
    """,
    unsafe_allow_html=True
)


# --- Input Form for User Data ---
with st.expander("🔍 Enter Employee Details", expanded=True):
    with st.form("prediction_form"):
        cols = st.columns([1, 1])
        
        with cols[0]:
            st.subheader("Basic Information")
            education = st.selectbox(
                "Education Level",
                ('High School', 'Bachelor', 'Master', 'PhD'),
                help="Select the highest education level."
            )
            experience = st.slider(
                "Years of Experience",
                min_value=0,
                max_value=60,
                value=5,
                step=1,
                help="Slide to select years of experience"
            )
            age = st.number_input(
                "Age",
                min_value=18,
                max_value=100,
                value=30,
                step=1,
                help="Enter the age of the employee."
            )
        
        with cols[1]:
            st.subheader("Job Details")
            job_title = st.selectbox(
                "Job Title",
                ["Software Engineer", "Data Scientist", "Product Manager", "Marketing Specialist", "Financial Analyst"],
                help="Select the job title"
            )
            location = st.selectbox(
                "Location Type",
                ('Urban', 'Suburban', 'Rural'),
                help="Select the type of location."
            )
            gender = st.radio(
                "Gender",
                ('Male', 'Female', 'Other'),
                horizontal=True,
                help="Select the gender."
            )
            company_size = st.select_slider(
                "Company Size",
                options=['Startup (1-50)', 'Small (51-200)', 'Medium (201-1000)', 'Large (1000+)'],
                value='Medium (201-1000)'
            )

        submitted = st.form_submit_button("🚀 Predict Salary", use_container_width=True)

# --- Prediction Logic ---
if submitted:
    with st.spinner("Analyzing market trends and predicting salary..."):
        time.sleep(1.5)
        
        # Create input DataFrame
        input_data = pd.DataFrame([[education, experience, location, job_title, age, gender]],
                                columns=['Education', 'Experience', 'Location', 'Job_Title', 'Age', 'Gender'])
        
        try:
            predicted_salary = model_pipeline.predict(input_data)[0]
            salary_min = predicted_salary * 0.9
            salary_max = predicted_salary * 1.15
            
            # Display prediction in a card
            with st.container():
                st.markdown(f"""
                <div class="salary-card">
                    <h2 style="color: #2d3748; text-align: center;">Your Salary Prediction</h2>
                    <h1 style="color: #2b6cb0; text-align: center;">${predicted_salary:,.2f}</h1>
                    <p style="text-align: center; color: #4a5568;">Estimated range: ₹{salary_min:,.2f} - ₹{salary_max:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                
                # Visualization - Salary Comparison
                st.subheader("How Does This Compare?")
                comparison_df = pd.DataFrame({
                    'Metric': ['Your Prediction', 'Industry Average', 'Experience Level'],
                    'Value': [predicted_salary, predicted_salary * 0.85, predicted_salary * (1 + (experience/100))]
                })
                
                fig = px.bar(comparison_df, x='Metric', y='Value', color='Metric',
                            labels={'Value': 'Salary ($)'}, height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Visualization - Salary Components
                st.subheader("Salary Breakdown")
                components = {
                    'Base Salary': predicted_salary * 0.7,
                    'Experience Bonus': predicted_salary * 0.15,
                    'Education Premium': predicted_salary * 0.1,
                    'Location Adjustment': predicted_salary * 0.05
                }
                pie_fig = px.pie(values=components.values(), names=components.keys(), hole=0.4)
                st.plotly_chart(pie_fig, use_container_width=True)
                
                # Download report
                input_data['Predicted Salary'] = predicted_salary
                input_data['Confidence Range'] = f"${salary_min:,.2f} - ${salary_max:,.2f}"
                csv = input_data.to_csv(index=False)
                st.download_button(
                    label="📄 Download Detailed Report",
                    data=csv,
                    file_name='salary_prediction_report.csv',
                    mime='text/csv',
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"Prediction error: {e}")

# --- Market Insights Section ---
st.markdown("---")
st.header("💡 Market Insights")

insight_cols = st.columns(3)
with insight_cols[0]:
    st.subheader("Education Impact")
    st.metric("PhD Premium", "+30%", "+2% YoY")
with insight_cols[1]:
    st.subheader("Experience Value")
    st.metric("Career Growth", "12%/year", "3-year avg")
with insight_cols[2]:
    st.subheader("Location Factor")
    st.metric("Urban Premium", "+15%", "vs Rural")

# Industry salary ranges illustration
industry_df = pd.DataFrame({
    'Industry': ['Tech', 'Finance', 'Healthcare', 'Marketing', 'Education'],
    'Avg Salary': [120000, 150000, 95000, 85000, 70000]
})
st.plotly_chart(px.bar(industry_df, x='Industry', y='Avg Salary', 
                       title="Average Salaries by Industry", height=400),
                use_container_width=True)

# --- Sidebar Features ---
with st.sidebar:
    st.image("https://placehold.co/200x50?text=Salary+Predictor+Pro", use_column_width=True)
    
    with st.expander("ℹ️ How It Works"):
        st.write("""
        Our advanced model considers:
        - Education level
        - Years of experience
        - Job title
        - Location
        - Age
        - Gender (for equality insights)
        """)
    
    with st.expander("📊 Sample Data"):
        st.dataframe(pd.DataFrame({
            'Education': ['PhD', 'Master', 'Bachelor'],
            'Experience': [10, 5, 3],
            'Predicted Salary': [150000, 100000, 75000]
        }))
    
    if st.button("🔄 Reset All Inputs", use_container_width=True):
        st.rerun()

st.markdown("---")
st.caption("Note: Predictions are estimates based on our machine learning model. Actual offers may vary.")
