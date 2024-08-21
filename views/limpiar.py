import pandas as pd
import streamlit as st
from io import StringIO

class Upload:
    def __init__(self, file=None):
        self.file = file

    def load_data(self):
        if self.file and self.file.name.endswith('.csv'):
            st.session_state.data = pd.read_csv(self.file)
        else:
            st.error("Formato de archivo no soportado.")

    def datos_faltantes(self, column):
        if column and 'data' in st.session_state:
            mean_value = st.session_state.data[column].mean()
            mean_value_int = int(round(mean_value))
            st.session_state.data[column].fillna(mean_value_int, inplace=True)

    def cambiar_tipo(self, column, new_dtype):
        if column and 'data' in st.session_state:
            try:
                if new_dtype == 'datetime':
                    st.session_state.data[column] = pd.to_datetime(st.session_state.data[column], errors='coerce')
                    st.success(f"Tipo de dato de la columna '{column}' cambiado a {new_dtype}.")
                else:
                    st.session_state.data[column] = st.session_state.data[column].astype(new_dtype)
                    st.success(f"Tipo de dato de la columna '{column}' cambiado a {new_dtype}.")
            except ValueError as e:
                st.error(f"No se pudo cambiar el tipo de dato: {str(e)}")

    def convertir_moneda(self, column, conversion):
        tasa_cambio = 900.0
        if column and 'data' in st.session_state:
            try:
                if conversion == 'USD a CLP':
                    st.session_state.data[column] = st.session_state.data[column] * tasa_cambio
                elif conversion == 'CLP a USD':
                    st.session_state.data[column] = st.session_state.data[column] / tasa_cambio
                st.success(f"La columna '{column}' ha sido convertida ({conversion}).")
            except Exception as e:
                st.error(f"No se pudo realizar la conversión: {str(e)}")

    def limitar_edad(self, column, min_age=18, max_age=70):
        if column and 'data' in st.session_state:
            mean_value = st.session_state.data[column].mean() 
            mean_value_int = int(round(mean_value))
            st.session_state.data[column] = st.session_state.data[column].apply(lambda x: mean_value_int if x < min_age or x > max_age else x)
            st.success(f"Los valores de la columna '{column}' fuera del rango {min_age}-{max_age} han sido reemplazados por la media ({mean_value_int}).")

    def obtener_info_df(self):
        buffer = StringIO()
        st.session_state.data.info(buf=buffer)
        info_str = buffer.getvalue()
        buffer.close()
        return info_str

# Interfaz
st.title("Limpieza de Datos")

uploaded_file = st.file_uploader("Carga tu archivo CSV", type=["csv"])

if uploaded_file and 'data' not in st.session_state:
    analyzer = Upload(uploaded_file)
    analyzer.load_data()

if 'data' in st.session_state:
    analyzer = Upload(None) #para que no se actualice el archivo csv cada que modifico con alguna opcion :D
    with st.sidebar:
        st.header("Opciones")
        column_num = st.session_state.data.select_dtypes(include=['number']).columns
        column = st.selectbox("Reemplaza datos faltantes con su media", column_num)
        if st.button("Corregir Datos"):
            analyzer.datos_faltantes(column)
            st.success(f"Se reemplazaron los datos de la columna '{column}' por la media de sus datos.")

        st.divider()
        
        all_columns = st.session_state.data.columns
        column_to_change = st.selectbox("Selecciona una columna para cambiar su tipo de dato", all_columns)
        new_dtype = st.selectbox("Selecciona el nuevo tipo de dato", ['int64', 'float64', 'str', 'datetime'])
        if st.button("Cambiar Tipo de Dato"):
            analyzer.cambiar_tipo(column_to_change, new_dtype)

        st.divider()

        column_to_convert = st.selectbox("Selecciona una columna para convertir moneda", column_num)
        conversion_option = st.selectbox("Selecciona la conversión", ['USD a CLP', 'CLP a USD'])
        if st.button("Convertir Moneda"):
            analyzer.convertir_moneda(column_to_convert, conversion_option)

        st.divider()

        column_age = st.selectbox("Selecciona una columna para limitar la edad", column_num)
        min_age = st.number_input("Edad mínima", min_value=0, value=18)
        max_age = st.number_input("Edad máxima", min_value=0, value=70)
        if st.button("Aplicar Límite de Edad"):
            analyzer.limitar_edad(column_age, min_age, max_age)

    st.write("### DataFrame")
    st.dataframe(st.session_state.data)

    if st.session_state.data is not None:

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


        
        
        
        csv = st.session_state.data.to_csv(index=False)
        st.download_button(
            label="Descargar DataFrame modificado",
            data=csv,
            file_name='df_modificado.csv',
            mime='text/csv',
        )


