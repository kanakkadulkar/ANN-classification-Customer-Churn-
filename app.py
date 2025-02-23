import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pickle

# Load trained model
model = tf.keras.models.load_model('model.h5')

# Load encoders
with open('label_encoder_gender.pkl', 'rb') as file:
    label_encoder_gender = pickle.load(file)

with open('onehot_encoder_geo.pkl', 'rb') as file:
    onehot_encoder_geo = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

# Streamlit app
st.title('Customer Churn Prediction')

# Create a form to take input from the user
geography = st.selectbox('Select Geography', onehot_encoder_geo.categories_[0])
gender = st.selectbox('Gender', label_encoder_gender.classes_)
age = st.slider('Enter Age', 18, 92)
balance = st.number_input('Enter Balance')
credit_score = st.number_input('Enter Credit Score')
estimated_salary = st.number_input('Enter Estimated Salary')
tenure = st.slider('Enter Tenure', 0, 10)
num_of_products = st.slider('Enter Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])

# Prepare input data
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label_encoder_gender.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary],
    'Geography': [geography]  # Add the 'Geography' column here
})

# One-hot encode 'Geography'
geo_encoded = onehot_encoder_geo.transform(input_data[['Geography']]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded, columns=onehot_encoder_geo.get_feature_names_out(['Geography']))

# Combine one-hot encoded data with input data
input_data = input_data.drop('Geography', axis=1)  # Drop the original 'Geography' column
input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1)

# Scale data
input_data_scaled = scaler.transform(input_data)

# Predict
prediction = model.predict(input_data_scaled)
prediction_proba = prediction[0][0]

st.write(f'Churn Probability: {prediction_proba:.2f}')

if prediction_proba > 0.5:
    st.write('The customer will leave the bank')
else:
    st.write('The customer will stay with the bank')