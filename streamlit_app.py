import streamlit as lit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

lit.header('Breakfast Menu ')
lit.text('🥣 Omega 3 & Blueberry Oatmeal')
lit.text('🥗 Kale, Spinach & Rocket Smoothie')
lit.text('🐔 Hard-Boiled Free-Range Egg')
lit.text('🥑🍞 Avacado toast')

lit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = lit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.
lit.dataframe(fruits_to_show)

# New Section
lit.header('Fruityvice fruit advice')

def get_fruitvice_data(fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    #lit.text(fruityvice_response.json())
    # write your own comment -what does the next line do? 
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
    

try:
  fruit_choice = lit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    lit.error("Please select a fruit to get information.")
  else:    
    fruityvice_response = get_fruitvice_data(fruit_choice)
    lit.dataframe(fruityvice_response)
except URLError as e:
  lit.error()
    
lit.write('The user entered ', fruit_choice)



lit.header("The fruit load list contains:")
my_cnx = snowflake.connector.connect(**lit.secrets["snowflake"])

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall() 

if lit.button("Get Fruit Load List"):
    my_data_rows = get_fruit_load_list()
    lit.dataframe(my_data_rows)


def insert_row_snowflake(add_fruit_choice):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list value ('from streamlit')")
    return 'Thanks for adding ', add_fruit_choice
    
add_fruit_choice = lit.text_input('What fruit would you like to add?')
if lit.button("Add a Fruit to List"):
    my_data_rows = insert_row_snowflake(add_fruit_choice)
    lit.text(my_data_rows)

