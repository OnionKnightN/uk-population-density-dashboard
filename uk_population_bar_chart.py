
# Importing Library for uk_population_bar_chart.py
import pandas as pd
import plotly.express as px
import streamlit as st

# Loading the dataset based on the uk population
df_uk_population = pd.read_csv("data/df_uk_population.csv")

# Streamlit user input options
st.sidebar.title('Options')
selected_year = st.sidebar.selectbox("Select Year", options=["2011", "2022"], index=1)
selected_gender = st.sidebar.radio("Select Gender", options=["All", "M", "F"], index=0)

# Selecting appropriate population column based on year
if selected_year == "2022":
    df_uk_population["population"] = df_uk_population["population_2022"]
else:
    df_uk_population["population"] = df_uk_population["population_2011"]

# Selecting appropriate filter based on gender if its a Male or Female
if selected_gender in ["M", "F"]:
    df_uk_population = df_uk_population[df_uk_population["sex"] == selected_gender]

# Grouping the sum values based on age 
df_selected = df_uk_population.groupby("age")["population"].sum().reset_index()

# df_selected = df_selected.sort_values("age")

# Colour mapping based on gender
gender_color_map = {
    "M": "#1f77b4",   # blue
    "F": "#e377c2",   # pink
    "All": "#7f7f7f"  # grey
}
# Setting the the bar colour based on the gender
bar_color = gender_color_map.get(selected_gender)

# string mapping based on gender
gender_map = {"M": "Male", "F": "Female"} 
# Setting the the title based on the gender
gender_title = gender_map.get(selected_gender, "All Genders")


# Creating the bar chart
fig = px.bar(
    df_selected,
    x="age",
    y="population",
    labels={"age": "Age", "population": "Population"},
    title=f"UK Population by Age - {gender_title} ({selected_year})",
    hover_data={"age": True, "population": True}
)

# Updating layout for the bar chart map 
fig.update_layout(bargap=0.2)

# Updating colour for bar chart map 
fig.update_traces(marker_color=bar_color)

# Display the bar map
st.plotly_chart(fig, use_container_width=True)

# Execute 'streamlit run uk_population_bar_chart.py' on the terminal
