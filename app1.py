import streamlit as st
import pandas as pd
import joblib
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns

# --- Custom CSS ---
st.markdown("""
    <style>
    body, .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #06b6d4);
        color: white;
        border-radius: 8px;
        font-size: 18px;
        padding: 8px 24px;
        margin-top: 10px;
        box-shadow: 0 2px 8px #6366f133;
        transition: 0.3s;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #06b6d4, #6366f1);
        color: #fff;
        letter-spacing: 2px;
        box-shadow: 0 4px 16px #6366f155;
    }
    .prediction-card {
        background: rgba(255,255,255,0.7);
        border-radius: 16px;
        box-shadow: 0 4px 24px #6366f133;
        padding: 32px;
        margin-top: 32px;
        text-align: center;
        font-size: 24px;
        color: #4338ca;
        backdrop-filter: blur(8px);
        border: 1px solid #e0e7ff;
        animation: fadeIn 1s;
    }
    .animated-header {
        font-size: 44px;
        font-weight: bold;
        background: linear-gradient(90deg, #6366f1, #06b6d4, #16a34a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientMove 2s infinite alternate;
        text-align: center;
        margin-bottom: 0px;
        margin-top: 16px;
        letter-spacing: 2px;
    }
    @keyframes gradientMove {
        0% { letter-spacing: 2px; }
        100% { letter-spacing: 8px; }
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px);}
        to { opacity: 1; transform: translateY(0);}
    }
    .section-divider {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #6366f1, #06b6d4, #16a34a);
        margin: 24px 0;
    }
    .footer {
        text-align: center;
        color: #6366f1;
        font-size: 16px;
        margin-top: 32px;
        margin-bottom: 8px;
        opacity: 0.8;
    }
    </style>
""", unsafe_allow_html=True)

# --- Animated Header ---
st.markdown('<div class="animated-header">💰 Salary Prediction App 🚀</div>', unsafe_allow_html=True)
st.markdown("""
    <div style="font-size:22px; color:#6366f1; text-align:center;">
        <span style="font-size:32px;">🧑‍💼</span>
        Enter the details below to get an <b>estimated salary prediction</b>.<br>
        This app uses a machine learning model trained on various professional attributes.
    </div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# --- Load the trained model ---
model_path = "best_model.pkl"
if not os.path.exists(model_path):
    st.error(f"Error: Model file '{model_path}' not found. Please make sure 'best_model.pkl' is in the same directory as this script.")
    st.stop()

try:
    model_pipeline = joblib.load(model_path)
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# --- Input Form for User Data ---
st.header("Employee Details 👤")

# Using st.form for better input management and a single submit button
with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        education = st.selectbox(
            "Education Level 🎓",
            ('High School', 'Bachelor', 'Master', 'PhD'),
            help="Select the highest education level."
        )
        experience = st.slider(
            "Years of Experience 🏆",
            min_value=0,
            max_value=60,
            value=5,
            step=1,
            help="Select the number of years of professional experience."
        )
        location = st.selectbox(
            "Location Type 📍",
            ('Urban', 'Suburban', 'Rural'),
            help="Select the type of location."
        )

    with col2:
        job_title = st.selectbox(
            "Job Title 💼",
            ('Software Engineer', 'Data Scientist', 'Manager', 'Analyst', 'Other'),
            help="Select your job title."
        )
        age = st.number_input(
            "Age 🎂",
            min_value=18,
            max_value=100,
            value=30,
            step=1,
            help="Enter the age of the employee."
        )
        gender = st.radio(
            "Gender ⚧️",
            ('Male', 'Female', 'Other'),
            horizontal=True,
            help="Select the gender."
        )

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    # Submit button for the form
    submitted = st.form_submit_button("Predict Salary 🚀")

# --- Prediction Logic ---
if submitted:
    # Create a DataFrame from the user input
    input_data = pd.DataFrame([[education, experience, location, job_title, age, gender]],
                              columns=['Education', 'Experience', 'Location', 'Job_Title', 'Age', 'Gender'])

    # Ensure correct dtypes for the input DataFrame columns
    input_data['Education'] = input_data['Education'].astype(str)
    input_data['Location'] = input_data['Location'].astype(str)
    input_data['Job_Title'] = input_data['Job_Title'].astype(str)
    input_data['Gender'] = input_data['Gender'].astype(str)
    input_data['Experience'] = pd.to_numeric(input_data['Experience'])
    input_data['Age'] = pd.to_numeric(input_data['Age'])

    # Animated progress bar
    progress_text = "⏳ Predicting salary, please wait..."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(0, 101, 10):
        time.sleep(0.07)
        my_bar.progress(percent_complete, text=progress_text)
    my_bar.empty()

    with st.spinner("Making prediction..."):
        time.sleep(0.5)
        try:
            predicted_salary = model_pipeline.predict(input_data)[0]

            # Show prediction in a styled card
            st.markdown(
                f'<div class="prediction-card">Predicted Salary: <span style="font-size:32px; color:#16a34a;">₹{predicted_salary:,.2f}</span><br><span style="font-size:28px;">🥳</span></div>',
                unsafe_allow_html=True
            )

            # Provide insights based on user input
            st.markdown("### Insights Based on Your Input")
            if job_title == 'Software Engineer':
                st.markdown("💡 **Career Insight**: Software engineers are in high demand. Consider learning new programming languages or frameworks to enhance your skills.")
            elif job_title == 'Data Scientist':
                st.markdown("💡 **Career Insight**: Data science is a rapidly growing field. Staying updated with the latest tools and techniques can give you an edge.")
            elif job_title == 'Manager':
                st.markdown("💡 **Career Insight**: Leadership skills are crucial for managers. Consider taking courses in management and communication.")
            elif job_title == 'Analyst':
                st.markdown("💡 **Career Insight**: Analysts should focus on data interpretation and visualization skills. Tools like Tableau or Power BI can be beneficial.")
            else:
                st.markdown("💡 **Career Insight**: Explore networking opportunities in your field to discover new career paths.")

            # Display potential salary range based on experience
            min_salary = predicted_salary * 0.8  # 20% less
            max_salary = predicted_salary * 1.2  # 20% more
            st.markdown(f"### Potential Salary Range: ₹{min_salary:,.2f} - ₹{max_salary:,.2f}")

            # Allow users to download their input data and prediction
            input_data['Predicted_Salary'] = predicted_salary
            csv = input_data.to_csv(index=False)
            st.download_button(
                label="⬇️ Download Prediction Report",
                data=csv,
                file_name='salary_prediction_report.csv',
                mime='text/csv'
            )

        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
            st.warning("Please ensure all input fields are filled correctly and the model is compatible with the provided inputs.")

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.info("Note: This prediction is an estimate based on the trained model and may not reflect actual market salaries precisely.")

# --- Sidebar with styled info ---
st.sidebar.image("https://avatars.githubusercontent.com/u/9919?s=200&v=4", width=80)
st.sidebar.header("About")
st.sidebar.markdown(
    """
    <div style="background:#6366f1; color:white; border-radius:8px; padding:16px; font-size:16px;">
    <b>This app demonstrates a simple salary prediction using a pre-trained machine learning model.</b><br>
    The model was trained using scikit-learn.<br>
    <span style="font-size:22px;">💡</span> Try different inputs and download your prediction!<br>
    <a href="https://github.com/" style="color:#fff; text-decoration:underline;" target="_blank">GitHub</a>
    </div>
    """, unsafe_allow_html=True
)

st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ using Streamlit")

# --- Footer ---
st.markdown('<div class="footer">© 2025 Salary Predictor | Powered by Streamlit & scikit-learn</div>', unsafe_allow_html=True)
