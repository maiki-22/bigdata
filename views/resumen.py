import streamlit as st
import pandas as pd
from io import StringIO


class Upload:
    def __init__(self, file):
        self.file = file
        self.data = None

    def load_data(self):
        if self.file.name.endswith('.csv'):
            self.data = pd.read_csv(self.file)
        else:
            st.error("Formato de archivo no soportado.")
            return
        st.session_state.data = self.data
    
    def obtener_info_df(self):
        buffer = StringIO()
        self.data.info(buf=buffer)
        info_str = buffer.getvalue()
        buffer.close()
        return info_str
        
        

st.title('Resumen de los datos')

uploaded_file = st.file_uploader("Carga tu archivo CSV", type=["csv"])

if uploaded_file:
    analyzer = Upload(uploaded_file)
    analyzer.load_data()


    if st.session_state.data is not None:
        st.write("DataFrame")
        st.dataframe(st.session_state.data)

        st.write("Primeras Filas del DF")
        st.write(st.session_state.data.head())

        st.write('Ultimas Filas del DF')
        st.write(st.session_state.data.tail())

        st.write('Descripcion del DF')
        st.write(st.session_state.data.describe())

        st.write('Valores Nulos del DF')
        st.write(st.session_state.data.isnull().sum())

        st.write('Info del DF')
        st.text(analyzer.obtener_info_df())
