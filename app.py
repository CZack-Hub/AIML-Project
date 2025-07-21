import streamlit as st
import pandas as pd
import joblib
import os

# Set page configuration for a wider layout and a nice title
st.set_page_config(layout="centered", page_title="Salary Predictor", page_icon="💰")

# --- Load the trained model ---
# Check if the model file exists
model_path = "best_model.pkl"
if not os.path.exists(model_path):
    st.error(f"Error: Model file '{model_path}' not found. Please make sure 'best_model.pkl' is in the same directory as this script.")
    st.stop() # Stop the app if the model is not found

try:
    # Load the pipeline from the .pkl file
    model_pipeline = joblib.load(model_path)
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# --- App Title and Description ---
st.title("💰 Salary Prediction App")
st.markdown("""
    Enter the details below to get an estimated salary prediction.
    This app uses a machine learning model trained on various professional attributes.
""")

st.write("---")

# --- Input Form for User Data ---
st.header("Employee Details")

# Using st.form for better input management and a single submit button
with st.form("prediction_form"):
    # Input fields for features
    col1, col2 = st.columns(2)

    with col1:
        education = st.selectbox(
            "Education Level",
            ('High School', 'Bachelor', 'Master', 'PhD'),
            help="Select the highest education level."
        )
        experience = st.number_input(
            "Years of Experience",
            min_value=0,
            max_value=60,
            value=5,
            step=1,
            help="Enter the number of years of professional experience."
        )
        location = st.selectbox(
            "Location Type",
            ('Urban', 'Suburban', 'Rural'),
            help="Select the type of location."
        )

    with col2:
        job_title = st.text_input(
            "Job Title",
            "Software Engineer",
            help="Enter the job title (e.g., Manager, Analyst, Engineer)."
        )
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30,
            step=1,
            help="Enter the age of the employee."
        )
        gender = st.radio(
            "Gender",
            ('Male', 'Female', 'Other'),
            horizontal=True,
            help="Select the gender."
        )

    st.markdown("---")
    # Submit button for the form
    submitted = st.form_submit_button("Predict Salary 🚀")

# --- Prediction Logic ---
if submitted:
    # Create a DataFrame from the user input
    input_data = pd.DataFrame([[education, experience, location, job_title, age, gender]],
                              columns=['Education', 'Experience', 'Location', 'Job_Title', 'Age', 'Gender'])

    # Explicitly ensure correct dtypes for the input DataFrame columns
    # This is a defensive step to match the dtypes the model pipeline expects
    # based on the original training data's structure.
    input_data['Education'] = input_data['Education'].astype(str)
    input_data['Location'] = input_data['Location'].astype(str)
    input_data['Job_Title'] = input_data['Job_Title'].astype(str)
    input_data['Gender'] = input_data['Gender'].astype(str)
    input_data['Experience'] = pd.to_numeric(input_data['Experience'])
    input_data['Age'] = pd.to_numeric(input_data['Age'])

    try:
        # Make prediction using the loaded pipeline
        predicted_salary = model_pipeline.predict(input_data)[0]

        st.success(f"### Predicted Salary: ${predicted_salary:,.2f}")
        st.balloons() # A little celebratory animation!

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
        st.warning("Please ensure all input fields are filled correctly and the model is compatible with the provided inputs.")

st.write("---")
st.info("Note: This prediction is an estimate based on the trained model and may not reflect actual market salaries precisely.")

# Optional: Add a sidebar for more information or settings
st.sidebar.header("About")
st.sidebar.info(
    "This app demonstrates a simple salary prediction using a pre-trained machine learning model. "
    "The model was trained using scikit-learn and saved as a `.pkl` file."
)
