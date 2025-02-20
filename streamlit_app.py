# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched
import requests

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be", name_on_order)


cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    my_dataframe,
    max_selections = 5
)
if ingredients_list:   
    ingredients_string = ''
    for i in ingredients_list:
        ingredients_string += i + ' '
        st.subheader(i + " Nutrition Information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+i)
        st_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
   

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
  #  st.stop()
    
    #st.write(my_insert_stmt)oopower
    time_to_insert = st.button('Submit Order')
    
    
    # Insert the Order into Snowflake
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order+'!', icon="✅")
        















