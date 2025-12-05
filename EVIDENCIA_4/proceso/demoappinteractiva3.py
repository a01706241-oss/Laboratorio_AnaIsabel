import streamlit as st
import pandas as pd
import pydeck as pdk

# Configuración inicial
MAPBOX_TOKEN = "pk.eyJ1IjoiZ3VzdGF2b3JvbWVybyIsImEiOiJjbWlqZDR2a3cxNGRiM2Rwc2dyNGN5N283In0.oxknwdyT9GQ8UAt4jH85bA"
st.set_page_config(page_title="Trazado de Ruta entre Ciudades", layout="wide")

# Sidebar
st.sidebar.title("Menú")
page = st.sidebar.radio("Selecciona una vista:", ["Ruta entre ciudades"])

# Datos base de ciudades y coordenadas
ciudades = {
    "Ciudad de México": {"lat": 19.4326, "lon": -99.1332},
    "Monterrey": {"lat": 25.6866, "lon": -100.3161},
    "Guadalajara": {"lat": 20.6597, "lon": -103.3496},
    "Querétaro": {"lat": 20.5888, "lon": -100.3899},
    "Puebla": {"lat": 19.0414, "lon": -98.2063},
    "León": {"lat": 21.1222, "lon": -101.6841}
}

if page == "Ruta entre ciudades":
    st.title("Trazar Ruta entre Ciudades")

    seleccionadas = st.multiselect(
        "Selecciona dos o más ciudades para trazar la ruta:",
        list(ciudades.keys()),
        default=["Querétaro", "Ciudad de México"]
    )

    if len(seleccionadas) < 2:
        st.warning("Selecciona al menos dos ciudades.")
    else:
        # Crear DataFrame con puntos
        df_puntos = pd.DataFrame([{
            "city": ciudad,
            "lat": ciudades[ciudad]["lat"],
            "lon": ciudades[ciudad]["lon"]
        } for ciudad in seleccionadas])

        # Crear líneas (rutas) entre puntos consecutivos
        rutas = []
        for i in range(len(df_puntos) - 1):
            rutas.append({
                "from_lon": df_puntos.iloc[i]["lon"],
                "from_lat": df_puntos.iloc[i]["lat"],
                "to_lon": df_puntos.iloc[i+1]["lon"],
                "to_lat": df_puntos.iloc[i+1]["lat"]
            })
        df_rutas = pd.DataFrame(rutas)

        # Visualizar puntos y líneas en el mapa
        st.pydeck_chart(pdk.Deck(
            api_keys={"mapbox": MAPBOX_TOKEN},
            map_style="mapbox://styles/mapbox/streets-v12",
            initial_view_state=pdk.ViewState(
                latitude=df_puntos["lat"].mean(),
                longitude=df_puntos["lon"].mean(),
                zoom=5,
                pitch=30,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df_puntos,
                    get_position="[lon, lat]",
                    get_color="[0, 100, 255, 160]",
                    get_radius=10000,
                    pickable=True,
                ),
                pdk.Layer(
                    "LineLayer",
                    data=df_rutas,
                    get_source_position='[from_lon, from_lat]',
                    get_target_position='[to_lon, to_lat]',
                    get_color='[255, 0, 0]',
                    get_width=5
                ),
            ]
        ))

        st.markdown("### Ruta:")
        for i, ciudad in enumerate(seleccionadas):
            st.markdown(f"{i+1}. {ciudad}")
