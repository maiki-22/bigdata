import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from scipy.stats import mode, pearsonr, spearmanr
import pandas as pd

class DataAnalysis:
    def __init__(self, data):
        self.data = data

    def calcular_tendencia_central(self):
        numeric_data = self.data.select_dtypes(include=[np.number])
        medidas = {
            'media': numeric_data.mean(),
            'mediana': numeric_data.median(),
            'moda': numeric_data.mode().iloc[0]
        }
        return medidas

    def calcular_dispersion(self):
        numeric_data = self.data.select_dtypes(include=[np.number])
        dispersion = {
            'desviación estándar': numeric_data["Salary"].std(),
            'varianza': numeric_data["Salary"].var(),
            'rango': numeric_data["Salary"].max() - numeric_data["Salary"].min()
        }
        return dispersion

    def crear_histogramas(self, columnas):
        if len(columnas) > 0:
            fig, axes = plt.subplots(nrows=1, ncols=len(columnas), figsize=(14, 6))
            fig.suptitle('Histogramas de las Variables Numéricas')

            for i, col in enumerate(columnas):
                sns.histplot(self.data[col], ax=axes[i], kde=True)
                axes[i].set_title(f'Histograma de {col}')
            
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("Por favor, selecciona al menos una columna para crear histogramas.")

    def identificar_outliers(self, factor=1.5):
        salario = self.data['Salary'].astype(float)
        Q1 = salario.quantile(0.25)
        Q3 = salario.quantile(0.75)
        IQR = Q3 - Q1
        outliers = salario[(salario < (Q1 - factor * IQR)) | (salario > (Q3 + factor * IQR))]
        return outliers

    def generar_boxplot(self):
        salario = self.data['Salary'].astype(float)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.boxplot(salario, vert=False)
        ax.set_title('Boxplot de Salarios')
        ax.set_xlabel('Salario')
        st.pyplot(fig)

    def calcular_matriz_correlacion(self):
        numeric_data = self.data.select_dtypes(include=[np.number])
        correlacion = numeric_data.corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlacion, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
        return correlacion

    def graficos_dispersion(self):
        fig = sns.pairplot(self.data)
        st.pyplot(fig.fig) 

    def pruebas_correlacion(self, metodo='pearson'):
        numeric_data = self.data.select_dtypes(include=[np.number])
        if metodo == 'pearson':
            correlaciones = numeric_data.corr(method='pearson')
        elif metodo == 'spearman':
            correlaciones = numeric_data.corr(method='spearman')
        else:
            st.error("Método no soportado: usa 'pearson' o 'spearman'")
            return None
        return correlaciones



# Interfaz
st.title("Análisis de Datos")

uploaded_file = st.file_uploader("Carga tu archivo CSV", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    analysis = DataAnalysis(data)

    st.write("### DataFrame Cargado")
    st.dataframe(data)

    # Opciones de análisis
    if st.sidebar.checkbox("Mostrar Medidas de Tendencia Central"):
        st.write("### Medidas de Tendencia Central")
        st.write(analysis.calcular_tendencia_central())

    if st.sidebar.checkbox("Mostrar Medidas de Dispersión"):
        st.write("### Medidas de Dispersión")
        st.write(analysis.calcular_dispersion())

    if st.sidebar.checkbox("Mostrar Histogramas"):
        columnas = st.sidebar.multiselect("Selecciona las columnas para los histogramas", data.select_dtypes(include=[np.number]).columns.tolist())
        st.write("### Histogramas")
        analysis.crear_histogramas(columnas)

    if st.sidebar.checkbox("Identificar Outliers"):
        st.write("### Outliers")
        st.write(analysis.identificar_outliers())

    if st.sidebar.checkbox("Generar Boxplot"):
        st.write("### Boxplot de Salarios")
        analysis.generar_boxplot()

    if st.sidebar.checkbox("Mostrar Matriz de Correlación"):
        st.write("### Matriz de Correlación")
        st.write(analysis.calcular_matriz_correlacion())

    if st.sidebar.checkbox("Mostrar Gráficos de Dispersión"):
        st.write("### Gráficos de Dispersión")
        analysis.graficos_dispersion()

    if st.sidebar.checkbox("Pruebas de Correlación"):
        metodo = st.sidebar.selectbox("Método de Correlación", ["pearson", "spearman"])
        st.write(f"### Pruebas de Correlación ({metodo.capitalize()})")
        st.write(analysis.pruebas_correlacion(metodo))


