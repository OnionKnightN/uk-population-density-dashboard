
import pandas as pd
import plotly.express as px
import streamlit as st
import json

# Setting the page layout
st.set_page_config(layout="wide")

###### Loading Data Start ######

# Loading the datasets for 2022 and 2011
df_uk_density_2022 = pd.read_csv("data/df_uk_population_density_2022.csv")
df_uk_density_2011 = pd.read_csv("data/df_uk_population_density_2011.csv")

# Loading the GeoJSON file for the UK boundaries
with open("data/Local_Authority_Districts_May_2024_Boundaries_UK.geojson", "r") as f:
    geojson = json.load(f)

###### Loading Data End ######


###### Streamlit Sidebar Controls Start ######

# Setting sidebar title
st.sidebar.title("Sidebar Options")

# Gender selection
gender_options = ['Both Genders', 'Male', 'Female']
selected_gender = st.sidebar.selectbox("Select Gender", gender_options)

# Age group label-to-key mapping
age_group_map = {
    'All Ages': 'All',
    'Early Childhood (0–5)': 'early_childhood',
    'Middle Childhood (6–12)': 'middle_childhood',
    'Teens (13–18)': 'teens',
    'Young Adults (19–39)': 'young_adults',
    'Middle Aged Adults (40–59)': 'middle_aged_adults',
    'Seniors/Elderly (60+)': 'seniors_elderly'
}

# Age group selection
age_group_option = st.sidebar.selectbox("Select Age Group", list(age_group_map.keys()))
selected_age_group = age_group_map[age_group_option]

######  Streamlit Sidebar Controls End ######

###### Helper Functions for Options Start ######

# Function to get the correct density column based on gender and age group
def get_density_column(gender, age_group):
    if gender == 'Both Genders':
        return 'person_per_sq_km'
    elif age_group == 'All':
        return f"{gender.lower()}_per_sq_km"
    else:
        return f"{gender.lower()}_{age_group.lower()}_per_sq_km"

# Function to get the correct population column based on gender, age group, and dataframe
def get_population_column(gender, age_group, df):
    if gender == 'Both Genders':
        if age_group == 'All':
            return 'population'
        else:
            male_col = f"male_{age_group}_population"
            female_col = f"female_{age_group}_population"
            df['combined_population'] = df[male_col] + df[female_col]
            return 'combined_population'
    else:
        if age_group == 'All':
            return f"{gender.lower()}_population"
        else:
            return f"{gender.lower()}_{age_group}_population"

###### Helper Functions for Options End ######

###### Data Selection Start ######

# Get the correct density and population columns for 2022
density_column_2022 = get_density_column(selected_gender, selected_age_group)
population_column_2022 = get_population_column(selected_gender, selected_age_group, df_uk_density_2022)

# Get the correct density and population columns for 2011
density_column_2011 = get_density_column(selected_gender, selected_age_group)
population_column_2011 = get_population_column(selected_gender, selected_age_group, df_uk_density_2011)

# Population label for the selected columns
if selected_gender == 'Both Genders' and selected_age_group != 'All':
    population_label = "Population"
else:
    population_label = population_column_2022.replace('_', ' ').title()


###### Create Choropleth Map for 2022 Start ######

# Create the choropleth map for 2022
fig_2022 = px.choropleth_map(
    df_uk_density_2022,
    geojson=geojson,
    locations='code',
    color=density_column_2022,
    featureidkey="properties.LAD24CD",
    color_continuous_scale=px.colors.sequential.Magma,
    center={"lat": 55.09, "lon": -4.03},
    custom_data=['name', 'code', 'area_sq_km', population_column_2022],
    labels={density_column_2022: 'Population<br>Density'},
    zoom=4.8
)

# Updating the hover template for the choropleth map for 2022
fig_2022.update_traces(
    hovertemplate=f"""
    <br><b>%{{customdata[0]}}</b><br>
    <br><b>Code: </b> %{{customdata[1]}}
    <br><b>Area per km²: </b> %{{customdata[2]:.0f}}
    <br><b>{population_label}: </b> %{{customdata[3]:.0f}}<br>
    """
)

# Updating layout for the choropleth map for 2022
fig_2022.update_layout(
    height=800,
    title={
        'text': f"UK Population Density by Local Authority District 2022 - {selected_gender} - {age_group_option}",
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
###### Create Choropleth Map for 2022 End ######

###### Create Choropleth Map for 2011 Start ######

# Create the choropleth map for 2011
fig_2011 = px.choropleth_map(
    df_uk_density_2011,
    geojson=geojson,
    locations='code',
    color=density_column_2011,
    featureidkey="properties.LAD24CD",
    color_continuous_scale=px.colors.sequential.Magma,
    center={"lat": 55.09, "lon": -4.03},
    custom_data=['name', 'code', 'area_sq_km', population_column_2011],
    labels={density_column_2011: 'Population<br>Density'},
    zoom=4.8
)

# Updating the hover template for the choropleth map for 2011
fig_2011.update_traces(
    hovertemplate=f"""
    <br><b>%{{customdata[0]}}</b><br>
    <br><b>Code: </b> %{{customdata[1]}}
    <br><b>Area per km²: </b> %{{customdata[2]:.0f}}
    <br><b>{population_label}: </b> %{{customdata[3]:.0f}}<br>
    """
)

# Updating layout for the choropleth map for 2011
fig_2011.update_layout(
    height=800,
    title={
        'text': f"UK Population Density by Local Authority District 2011 - {selected_gender} - {age_group_option}",
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
###### Create Choropleth Map for 2011 End ######

###### Display Both Maps Side by Side Start ######

col1, col2 = st.columns(2)

# Display the maps
with col1:
    st.plotly_chart(fig_2022, use_container_width=True)

with col2:
    st.plotly_chart(fig_2011, use_container_width=True)

###### Display Both Maps Side by Side End ######

