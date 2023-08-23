import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
   
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Balueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#List to pick the fruit that they want
selected_fruits = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[selected_fruits]

#display the table on the page
streamlit.dataframe(fruits_to_show)

#create the function
def getfruityvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalized

#Fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   #streamlit.write('The user entered ', fruit_choice)
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
   else:
      #import requests
      #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
      #Normalize the json response
      #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      #Show as a dataframe
      back_from_function= getfruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
except URLError as e:
   streamlit.error()


#streamlit.stop()


#streamlit.write('The user want to add ' , add_my_fruit)
#my_cur.execute("insert into fruit_load_list values ('from streamlit')")

#import snowflake.connector

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("insert into fruit_load_list values ('"+add_my_fruit +"')")

#my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
      with my_cnx.cursor() as my_cur:
           my_cur.execute("select * from fruit_load_list")
           return my_cur.fetchall()


if streamlit.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+new_fruit +"')")
        return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you want to add?')
if streamlit.button('Add a Fruit to the List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_function)



