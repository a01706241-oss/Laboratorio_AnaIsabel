import streamlit as st 
import plotly.express as px
import geopandas as gpd
import pandas as pd

def load_data(data):
    return pd.read_csv(data)

def main():

    st.title("Teams Map")
    menu = ["Home","Advanced","Teams","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Plot")
        us_cities = pd.read_csv("us_cities.csv")
        world = pd.read_csv("worldcities.csv")
      
        st.dataframe(world)
        fig = px.scatter_map(world, lat="lat", lon="lng", hover_name="city", hover_data=["country", "population"],
                                color_discrete_sequence=["fuchsia"], zoom=1,height=700)
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig)
       
    
    elif choice == "Advanced":
        st.subheader("Plot")
        world = load_data("worldcities.csv")
       
        countries_list = world["country"].unique().tolist()
        selected_country = st.multiselect("country",countries_list,default=["Ghana"])
        gdf = world[world["country"].isin(selected_country)]
        st.dataframe(gdf)

        fig = px.scatter_map(gdf, lat="lat", lon="lng", hover_name="city", hover_data=["country", "population"],
                                color_discrete_sequence=["fuchsia"], zoom=2,height=700)
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig)

    elif choice == "Teams":
        st.subheader("Plot")
        world = load_data("worldcities.csv")
       
        cities_list = world["city"].unique().tolist()
        selected_cities = st.multiselect("city",cities_list,default=["Bremen"])
        gdf = world[world["city"].isin(selected_cities)]
        st.dataframe(gdf)

        fig = px.scatter_map(gdf, lat="lat", lon="lng", hover_name="city", hover_data=["country", "population"],
                                color_discrete_sequence=["fuchsia"], zoom=2,height=700)
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig)
    

    else:
        st.subheader("About")



if __name__ == '__main__':
    main()