import streamlit

streamlit.title('My Parents New Healthy Diner')
   
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Balueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#List to pick the fruit that they want
selected_fruits = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[selected_fruits]

#display the table on the page
streamlit.dataframe(fruits_to_show)

#Fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+"kiwi")

#Normalize the json response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#Show as a dataframe
streamlit.dataframe(fruityvice_normalized)


