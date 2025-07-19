# 💰 Employee Salary Prediction

This project aims to build a machine learning model that predicts employee salaries based on a variety of features, including education, experience, job title, age, gender, and location. The model is trained using Linear Regression on a dataset sourced from Kaggle and deployed through Streamlit web applications, offering three unique user interfaces.

## 📊 Project Overview

* **Predictive Power:** Utilizes user-provided inputs to estimate potential employee salaries.
* **Core Model:** Trained with a Linear Regression model built using the `scikit-learn` library.
* **Diverse UIs:** Includes three distinct Streamlit web applications (`app.py`, `app1.py`, `app2.py`) showcasing different UI designs for varied user experiences.
* **Insights & Reporting:** Provides estimated salary ranges and personalized career insights based on the prediction.
* **Data Export:** Allows users to download a comprehensive prediction report as a CSV file.

## 🗂️ Repository Structure

employee-salary-prediction/


**├── app.py**                      # Streamlit App - Simplified form interface

**├── app1.py**                     # Streamlit App - Alternative UI design

**├── app2.py**                     # Streamlit App - Modern, animated interface

**├── best_model.pkl**              # Trained Linear Regression model (serialized)

**├── SalaryPredictionModel.ipynb** # Jupyter notebook for model training and evaluation

**├── requirements.txt**            # Project dependencies

**└── README.md**                   # Project documentation (this file)

## 🌐 Web App Features

Each Streamlit application offers an interactive user input form for:

* **Education Level**
* **Years of Experience**
* **Job Title**
* **Age**
* **Gender**
* **Location Type**

Beyond the input, the apps provide:

* **Predicted Salary Display:** Visually appealing display of the estimated salary, often with animations and clear formatting.
* **Estimated Salary Range:** A realistic range around the predicted value to provide better context.
* **Personalized Career Insights:** Tailored advice or information based on the input parameters.
* **Downloadable Report:** An option to download the prediction details in CSV format.

## 📒 Model Training

The Linear Regression model is meticulously trained using a dataset obtained from Kaggle. The training process, thoroughly documented in the `SalaryPredictionModel.ipynb` Jupyter notebook, involves the following key steps:

1.  **Data Cleaning and Preprocessing:** Handling missing values, outliers, and preparing data for model consumption.
2.  **Feature Encoding and Transformation:** Converting categorical features into numerical representations suitable for machine learning algorithms.
3.  **Model Training:** Utilizing `scikit-learn`'s `LinearRegression` to fit the preprocessed data.
4.  **Model Serialization:** Saving the trained model using `joblib` as `best_model.pkl` for later deployment.

## 🚀 Running the Application

To get the application up and running on your local machine, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/yourusername/employee-salary-prediction.git](https://github.com/yourusername/employee-salary-prediction.git)
    cd employee-salary-prediction
    ```
    *(Remember to replace `yourusername` with the actual GitHub username where the repository is hosted.)*

2.  **Install Dependencies:**
    Ensure you have Python installed (version 3.9+ is recommended). Then, install all required libraries using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Launch a Streamlit App:**
    Choose which Streamlit application you'd like to run. For example, to launch `app1.py`:
    ```bash
    streamlit run app1.py
    ```
    You can replace `app1.py` with `app.py` or `app2.py` to experience the different UIs.

---

### 📌 Notes

* **Disclaimer:** The prediction provided by this model is an estimate and may not perfectly represent actual market salaries due to various unmodeled factors and market fluctuations.
* **Model Dependency:** All Streamlit applications (`app.py`, `app1.py`, `app2.py`) assume the presence of the `best_model.pkl` file in the root directory. Ensure it is available before running the apps.
* **Python Compatibility:** The project is compatible with Python 3.9 and newer versions.

---

## 🙌 Acknowledgements

* **Kaggle:** For providing the dataset that made this project possible.
* **scikit-learn:** The robust machine learning framework used for model development.
* **Streamlit:** The fantastic open-source framework that enabled rapid development and deployment of the interactive web applications.
