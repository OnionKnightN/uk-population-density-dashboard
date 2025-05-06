# Importing Library for dashboard_interactive_visualisation.py
import pandas as pd
import plotly.express as px
import streamlit as st
import json

# Setting the page layout
st.set_page_config(layout="wide")

# Setting sidebar title
st.title("Interactive Dashboard - UK Population Density")

###### Loading Data for Choropleth Map Start ######

# Loading the datasets for 2022 and 2011
df_uk_density_2022 = pd.read_csv("data/df_uk_population_density_2022.csv")
df_uk_density_2011 = pd.read_csv("data/df_uk_population_density_2011.csv")

# Loading the GeoJSON file for the UK boundaries
with open("data/Local_Authority_Districts_May_2024_Boundaries_UK.geojson", "r") as f:
    geojson = json.load(f)

###### Loading Data for Choropleth Map Start ######

######  Streamlit Sidebar Controls Start ######

# Setting sidebar title
st.sidebar.title("Control Panel")

# Year selection (2022 or 2011)
year_options = [2022, 2011]
selected_year = st.sidebar.selectbox("Select Year", year_options)

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

# Function to get the correct population column based on gender, age group and dataframe
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

# Select the correct dataframe based on the selected year
if selected_year == 2022:
    df_selected = df_uk_density_2022
else:
    df_selected = df_uk_density_2011

# Get the correct density and population columns
density_column = get_density_column(selected_gender, selected_age_group)
population_column = get_population_column(selected_gender, selected_age_group, df_selected)

# Population label for the selected columns
if selected_gender == 'Both Genders' and selected_age_group != 'All':
    population_label = "Population"
else:
    population_label = population_column.replace('_', ' ').title()

if selected_gender == 'Female':
    colour = px.colors.sequential.Magma
elif selected_gender == 'Male':
    colour = px.colors.sequential.BuPu[2:]
else:
    colour = px.colors.sequential.Greys[2:]

# Adjust custom_data based on the population_column 
custom_data = ['name', 'code', 'area_sq_km', population_column]

###### Data Selection Start ######

###### Create Choropleth Map Start ######

# Create the choropleth map
fig = px.choropleth_map(
    df_selected,
    geojson=geojson,
    locations='code',
    color=density_column,
    featureidkey="properties.LAD24CD",
    color_continuous_scale=colour,
    center={"lat": 55.09, "lon": -4.03},
    custom_data=custom_data,
    labels={density_column:'Population<br>Density'},
    zoom=4.6
)

# Updating the hover template for the choropleth map
fig.update_traces(
    hovertemplate=f"""
    <br><b>%{{customdata[0]}}</b><br>
    <br><b>Code: </b> %{{customdata[1]}}
    <br><b>Area per km²: </b> %{{customdata[2]:.0f}}
    <br><b>{population_label}: </b> %{{customdata[3]:.0f}}<br>
    """
)

# Updating layout for the choropleth map
fig.update_layout(
    height=650,
    title={
        'text': f"UK Population Density {selected_year} - {selected_gender} - {age_group_option}",
        'y': 0.98,
        'font': dict(size=24),
        'xanchor': 'left',
        'yanchor': 'top'
    },
    coloraxis_colorbar=dict(
        title_font=dict(size=18),
        tickfont=dict(size=16),
    ),
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_color="grey", 
    ),
    margin={"r": 150, "t": 50, "l": 0, "b": 0}
)

###### Create Choropleth Map End ######


###### Loading Data for Bar Chart Start ######

# Loading the datasets for population for bar chart 
df_uk_population = pd.read_csv("data/df_uk_population.csv")
# Convert selected_year to string for column access
year_str = str(selected_year)
# Select appropriate population column based on year
df_uk_population["population"] = df_uk_population[f"population_{year_str}"]

###### Loading Data for Bar Chart End ######

###### Gender Title and Filtering Start ######

# Dynamoc gender title based on selected gender
gender_title = selected_gender if selected_gender != "Both Genders" else "Both Genders"

# Mapping the gender names to their respective abbreviations for filtering
gender_filter_map = {
    "Male": "M",
    "Female": "F"
}

# Filter the dataframe for the selected gender
if selected_gender in gender_filter_map:
    df_uk_population = df_uk_population[df_uk_population["sex"] == gender_filter_map[selected_gender]]

###### Gender Title and Filtering End ######

###### Grouping Population Data by Age Start ######

# Group by age
df_age_grouped = df_uk_population.groupby("age")["population"].sum().reset_index()

###### Grouping Population Data by Age End ######

###### Create Bar Chart Start ######

# Create bar chart
bar_fig = px.bar(
    df_age_grouped,
    x="age",
    y="population",
    labels={"age": "Age", "population": "Population"},
    hover_data={"age": True, "population": True}
)

# Updating layout for the bar chart 
bar_fig.update_layout(
    title={
        'text': f"UK Population by Age {year_str} - {gender_title}",
        'font': dict(size=24),
        'xanchor': 'left',
        'yanchor': 'top'
    },
    yaxis=dict(
        title_font=dict(size=18),  
        tickfont=dict(size=16)  
    ),
    xaxis=dict(
        title_font=dict(size=18), 
        tickfont=dict(size=16) 
    ),
    bargap=0.2
)

###### Create Bar Chart End ######

###### Bar Color Customization Start ######

# Gender to color mapping
gender_color_map = {
    "Male": "#9ebcda",   
    "Female": "#000004",
    "Both Genders": "#bdbdbd"
}

# Defining the bar color based on selected gender
bar_color = gender_color_map.get(selected_gender, "#7f7f7f")

# Applying the selected bar color to the chart
bar_fig.update_traces(marker_color=bar_color)

###### Bar Color Customization End ######

###### Main Visualization Container Start ######

# Main visualization container
with st.container():

    # Display the bar chart  
    st.plotly_chart(bar_fig, use_container_width=True)

    # Display the choropleth map
    st.plotly_chart(fig, use_container_width=True)

###### Main Visualization Container End ######

# Execute 'streamlit run dashboard_interactive_visualisation.py' on the terminal
