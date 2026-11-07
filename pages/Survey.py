# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("What is your favorite NBA team?")
    value_input = st.text_input("How many NBA games do you watch per week?")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.

        if category_input.strip() == "":
            st.error("Please enter your favorite NBA team.")

        elif not value_input.isdigit():
            st.error("Please enter a valid number of games.")

        else:
            games = int(value_input)

            with open("data.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([category_input.strip().title(), games])

            st.success("Your response has been submitted!")
            st.write(f"Favorite Team: {category_input}")
            st.write(f"Games Watched Per Week: {games}")


       # DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Responses in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    if len(current_data_df) > 0:
        st.dataframe(current_data_df)
        st.write(f"Total responses: {len(current_data_df)}")
    else:
        st.info("No responses yet. Be the first to submit!")
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
