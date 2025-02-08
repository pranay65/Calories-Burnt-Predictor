import streamlit as st
from xgboost import XGBRegressor
import joblib

model = joblib.load('/Users/pranay/Documents/Python/CaloriesPredictor/caloriesModel.pkl') 

def predict_calories(gender, age, height, weight, duration, heart_rate, body_temp):
    features = [[gender, age, height, weight, duration, heart_rate, body_temp]]
    prediction = model.predict(features)
    return prediction[0]

def calculate_bmi(weight, height):
    height_m = height / 100 
    bmi = weight / (height_m ** 2)
    return bmi

def bmi_category_and_recommendation(bmi):
    if bmi < 18.5:
        category = "Underweight"
        recommendation = "Increase caloric intake and consider strength training."
    elif 18.5 <= bmi <= 24.9:
        category = "Normal weight"
        recommendation = "Maintain regular exercise, ideally 150-300 minutes of moderate exercise per week."
    elif 25 <= bmi <= 29.9:
        category = "Overweight"
        recommendation = "Engage in at least 300 minutes of moderate exercise per week."
    else:
        category = "Obese"
        recommendation = "Consult a healthcare provider for a personalized exercise and diet plan."

    return category, recommendation

st.title("Calories Burned Prediction")
st.write("Enter your details to predict the calories burned.")

gender = st.selectbox("Gender", options=[1, 0], format_func=lambda x: "Male" if x == 1 else "Female")
age = st.number_input("Age", min_value=1, max_value=100, value=25)
height = st.slider("Height (cm)", min_value=100, max_value=220, value=170)
weight = st.slider("Weight (kg)", min_value=30, max_value=200, value=70)
duration = st.slider("Duration (minutes)", min_value=1, max_value=250, value=30)
heart_rate = st.slider("Heart Rate (bpm)", min_value=50, max_value=200, value=120)
body_temp = st.slider("Body Temperature (°C)", min_value=35.0, max_value=42.0, value=38.7, step=0.1)

if st.button("Predict Calories Burned"):
    prediction = predict_calories(gender, age, height, weight, duration, heart_rate, body_temp)
    st.subheader("Calories Burned Prediction:")
    st.write(f"Estimated calories burned: **{prediction:.2f} kcal**")

    bmi = calculate_bmi(weight, height)
    category, recommendation = bmi_category_and_recommendation(bmi)

    st.subheader("BMI Analysis")
    st.write(f"Your BMI: **{bmi:.2f}** ({category})")
    st.write(f"Recommended Exercise: {recommendation}")
    
    if category == "Normal weight":
        st.success("Your BMI is in a healthy range for your age and gender.")
    else:
        st.warning("Your BMI is outside the healthy range for your age and gender. Consider consulting a healthcare provider.")