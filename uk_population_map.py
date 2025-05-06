
# Importing Library for uk_population_map.py
import pandas as pd
import plotly.express as px
import streamlit as st
import json

# Loading the dataset based on the uk density for 2022 and 2011
df_uk_density_2022 = pd.read_csv("data/df_uk_population_density_2022.csv")
df_uk_density_2011 = pd.read_csv("data/df_uk_population_density_2011.csv")

# Loading the GeoJSON file for the UK boundaries
with open("data/Local_Authority_Districts_May_2024_Boundaries_UK.geojson", "r") as f:
    geojson = json.load(f)

# Streamlit user input options
st.sidebar.title('Options')
year = st.sidebar.selectbox("Select Year:", [2011, 2022])

# Load the appropriate DataFrame based on the selected year
if year == 2011:
    df_selected = df_uk_density_2011
else:
    df_selected = df_uk_density_2022

# Create the choropleth map
fig = px.choropleth_map(
    df_selected,
    geojson=geojson,
    locations='code',
    color='person_per_sq_km',
    featureidkey="properties.LAD24CD",
    color_continuous_scale=px.colors.sequential.Plasma,
    center={"lat": 55.09, "lon": -4.03},
    custom_data=['name','code','population', 'area_sq_km', 'person_per_sq_km'],
    labels={'person_per_sq_km': 'Population<br>Density'},
    zoom=4
)

# Updating the hover template for the choropleth map. 
fig.update_traces(
    hovertemplate="""
    <br><b>%{customdata[0]}</b><br>
    <br><b>Code: </b> %{customdata[1]}
    <br><b>Population: </b> %{customdata[2]}
    <br><b>Area per km²: </b> %{customdata[3]:.0f}
    <br><b>Person per km²: </b> %{customdata[4]:.0f}<br>
    """
)

# Updating layout for the choropleth map. 
fig.update_layout(
     title={
        'text': f"UK Population by Local Authority District - {year}",
        'y': 0.95,  # Slightly lower than default
        'x': 0.0,
        'xanchor': 'left',
        'yanchor': 'top'
    },
    hoverlabel=dict(
        bgcolor="white",     
        font_size=14,
        font_color="grey", 
    ),
    margin={"r": 150, "t": 50, "l": 0, "b": 0}
)

# Display the choropleth map
st.plotly_chart(fig, use_container_width=True)

# Execute 'streamlit run uk_population_map.py' on the terminal
