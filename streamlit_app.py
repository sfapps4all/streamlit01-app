import streamlit as lit
import pandas as pd
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

lit.header('Breakfast Menu ')
lit.text('🥣 Omega 3 & Blueberry Oatmeal')
lit.text('🥗 Kale, Spinach & Rocket Smoothie')
lit.text('🐔 Hard-Boiled Free-Range Egg')
lit.text('🥑🍞 Avacado toast')

lit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
lit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberry'])

# Display the table on the page.
lit.dataframe(my_fruit_list)
