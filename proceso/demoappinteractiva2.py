#pip install streamlit pandas matplotlib pydeck
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk

# Configuración general
MAPBOX_TOKEN = "pk.eyJ1IjoiZ3VzdGF2b3JvbWVybyIsImEiOiJjbWlqZDR2a3cxNGRiM2Rwc2dyNGN5N283In0.oxknwdyT9GQ8UAt4jH85bA"
st.set_page_config(page_title="Gráficos Interactivos", layout="wide")

# Menú lateral
st.sidebar.title("Menú de Navegación")
page = st.sidebar.radio("Selecciona una vista:", ["Gráfico Tipo Dona", "Mapa Interactivo"])

# Página: Gráfico Tipo Dona
if page == "Gráfico Tipo Dona":
    st.title("Gráfico de Dona Interactivo")

    # Dataset de ejemplo
    categorias = ['Ventas', 'Marketing', 'Producción', 'Soporte', 'IT']
    valores = [35, 20, 25, 10, 10]
    data = dict(zip(categorias, valores))

    st.write("Selecciona las categorías que deseas mostrar:")
    seleccionadas = [cat for cat in categorias if st.checkbox(cat, value=True)]

    if seleccionadas:
        valores_filtrados = [data[cat] for cat in seleccionadas]

        fig, ax = plt.subplots()
        ax.pie(valores_filtrados, labels=seleccionadas, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4))
        ax.axis('equal')  # Donut
        st.pyplot(fig)
    else:
        st.warning("Selecciona al menos una categoría para visualizar el gráfico.")

# Página: Mapa Interactivo
elif page == "Mapa Interactivo":
    st.title("Mapa con Selección de Ciudad")

    # Dataset de ciudades con coordenadas
    ciudades = {
        "Ciudad de México": {"lat": 19.4326, "lon": -99.1332},
        "Monterrey": {"lat": 25.6866, "lon": -100.3161},
        "Guadalajara": {"lat": 20.6597, "lon": -103.3496},
        "Querétaro": {"lat": 20.5888, "lon": -100.3899}
    }

    ciudad = st.selectbox("Selecciona una ciudad:", list(ciudades.keys()))
    coordenadas = ciudades[ciudad]

    # Mostrar mapa con marcador
    st.write(f"Mostrando ubicación de **{ciudad}**")
    df_map = pd.DataFrame([{
        "lat": coordenadas["lat"],
        "lon": coordenadas["lon"]
    }])

    st.pydeck_chart(pdk.Deck(
        api_keys={"mapbox": MAPBOX_TOKEN},
        map_style='mapbox://styles/mapbox/streets-v12',
        initial_view_state=pdk.ViewState(
            latitude=coordenadas["lat"],
            longitude=coordenadas["lon"],
            zoom=10,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df_map,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=10000,
            ),
        ],
    ))
