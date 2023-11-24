import streamlit as st
import pickle
import pandas as pd
import os

# Load medicine data and similarity matrix
medicines_dict = pickle.load(open(os.path.join(base_path, 'medicine_dict.pkl'), 'rb'))
medicines = pd.DataFrame(medicines_dict)
similarity = pickle.load(open(os.path.join(base_path, 'similarity.pkl'), 'rb'))
l = pd.read_csv(os.path.join(base_path, 'medicine.csv'))


st.set_page_config(
    page_title='Medicine Recommender System',
    page_icon='🌡️',
)

def recommend(medicine):
    medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
    distances = similarity[medicine_index]
    medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_medicines = []
    for i in medicines_list:
        recommended_medicine = medicines.iloc[i[0]].Drug_Name
        recommended_medicines.append(recommended_medicine)

    return recommended_medicines

import pandas as pd

# Assuming your dataset is named 'df' and has columns 'Medicine_Name' and 'Indication'
# Replace 'Medicine_Name' and 'Indication' with your actual column names

def medication_chatbot(user_input):
    r=[]
    user_input_lower = user_input.lower()

    # Check if the user input matches any medication names in the dataset
    matching_medications = l[l['Reason'].str.lower().isin([user_input_lower])]

    # Check if there are any matching medications
    if not matching_medications.empty:
        # Display information about the matching medication(s)
        response = f"Here is information about the medication matching your input '{user_input}':\n"
        for index, row in matching_medications.iterrows():
            response += f"{row['Drug_Name']}: {row['Description']}\n"
            r.append(response)
        return r

    else:
        # If no direct match, provide a generic response or ask for more details
        return "I'm a simple medication chatbot. Please provide more details for personalized recommendations."




def home_page():
    st.header('Welcome to the Medicine Recommender System')
    st.write(
        "This system helps you discover alternative medicines based on similarity. "
        "Select a medicine from the sidebar and press enter"
    )
    user_question = st.text_input("Ask any medicion:")
    if user_question:
        chatbot_response = medication_chatbot(user_question)
        st.write("Chatbot:", chatbot_response)
    st.image('images/medicine-image.jpg', caption='Recommended Medicines')


st.sidebar.image('images/r.jpg', caption='Logo')
st.sidebar.title('Search Medicines')

selected_medicine_name = st.sidebar.selectbox(
    'Type your medicine name whose alternative is to be recommended',
    ['Search here'] + list(medicines['Drug_Name'].values)
)

if selected_medicine_name == 'Search here':
    home_page()
else:
    recommendations = recommend(selected_medicine_name)
    st.header(f"Top 5 Alternative Medicines for {selected_medicine_name}")
    for j, rec in enumerate(recommendations, start=1):
        st.write(f"{j}. {rec}")

    user_question = st.text_input("Ask a question:")
    if user_question:
        chatbot_response = medication_chatbot(user_question)
        st.write("Chatbot:", chatbot_response)
