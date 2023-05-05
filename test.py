import streamlit as st
st.set_page_config(layout="wide")

import mysql.connector
from st_on_hover_tabs import on_hover_tabs
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from st_aggrid import AgGrid
import pandas as pd
import pymysql
import plotly.express as px
import ifcopenshell
from streamlit_option_menu import option_menu
from streamlit_tree_select import tree_select

st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

def callback_upload():
    session["file_name"] = session["uploaded_file"].name
    session["array_buffer"] = session["uploaded_file"].getvalue()
    session["ifc_file"] = ifcopenshell.file.from_string(session["array_buffer"].decode("utf-8"))
    session["is_file_loaded"] = True
    
    ### Empty Previous Model Data from Session State
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}

    ### Empty Previous DataFrame from Session State
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False
          ## Add File Name and Success Message
    if "is_file_loaded" in session and session["is_file_loaded"]:
        st.success(f'Projecto cargado exitosamente')
        st.write("🔃 Puede recargar un nuevo archivo  ")

# Create Streamlit App
# header {visibility: hidden;}
def main():
    # --- HIDE STREAMLIT STYLE ---
    hide_st_style = """
                        <style>               
                        #MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}
                        </style>
                    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Careperro1",
    database="winxa"
    )
    mycursor=mydb.cursor()
    print("Connection Established")

    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Gestion de Campus', 'Ver Modelo BIM'], 
                         iconName=['dashboard', 'money'], default_choice=0)

    if tabs =='Gestion de Campus':
        tab1, tab2 = st.tabs(["Ingresar Campus", "Campus actuales"])
        with tab1:
            
            mycursor=mydb.cursor()
            print("Connection Established")

            
            st.title("Universidad Santa Maria");

                # Display Options for CRUD Operations
            option=st.sidebar.selectbox("Select an Operation",("Create","Read","Update","Delete"))
                # Perform Selected CRUD Operations
            if option=="Create":

                    mycursor.execute("select nombre_pais from paises")
                    result_paises= mycursor.fetchall()

                    mycursor.execute("select nombre_region from regiones")
                    result_regiones= mycursor.fetchall()

                    mycursor.execute("select nombre_tipo from categoria_entidad")
                    result_categoria= mycursor.fetchall()
        
                    st.subheader("Ingresar nuevo Campus")
                    x = st.selectbox("Categoria",result_categoria,key = "hh")
                    name=st.text_input("Nombre desl Campus")
                    pais = st.selectbox("País",result_paises, key = "co_pais")
                    region = st.selectbox("Región",result_regiones, key = "co_reg")
                    ciudad = st.selectbox("Ciudad",(result_regiones), key = "co_ciu")
                    email=st.text_input("Direccion")
                    
                    if st.button("Crear"): 
                        sql= "insert into categoria_entidad(nombre_categoria) values(%s,%s)"
                        val= (name,email)
                        mycursor.execute(sql,val)
                        mydb.commit()
                        st.success("Record Created Successfully!!!")

        with tab2:
                df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')
                AgGrid(df)        

    elif tabs == 'Ver Modelo BIM':
   
        st.file_uploader("Seleccionar archivo", type=['ifc'], key="uploaded_file", on_change=callback_upload)
if __name__ == "__main__":
    session = st.session_state
    main()
