import streamlit as st

# Paginas //

limpiar_page = st.Page(
    page="views/limpiar.py",
    title='Limpieza De Datos',
    icon=':material/cleaning_services:',
    default=True
)
analisis_page = st.Page(
    page="views/analisis.py",
    title='Analisis de datos',
    icon=':material/analytics:',
)
resumen_page = st.Page(
    page='views/resumen.py',
    title="Resumen de los datos",
    icon=':material/monitoring:',
)

# Navegador :) //

pg = st.navigation(pages=[limpiar_page,analisis_page,resumen_page])
pg.run()