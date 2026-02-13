# Interactive UK Population Density Dashboard

An interactive Streamlit dashboard visualizing UK population density trends for 2011 and 2022.

The project demonstrates end-to-end data preparation, transformation, and geospatial visualization using demographic segmentation (age and gender) to enable dynamic population analysis across UK local authorities.

---

## Features

- Data cleaning, validation, and transformation using Pandas
- Feature engineering for:
  - Gender-specific population totals
  - Age-group segmentation
  - Population density per square kilometer
- Aggregation and merging of multi-sheet Excel datasets
- Export of processed datasets for dashboard consumption
- Interactive dashboard built with Streamlit
- Geospatial choropleth visualization using Plotly
- Dynamic filtering by:
  - Year (2011 / 2022)
  - Gender
  - Age group
- Real-time chart updates based on user selection
- Hover-based geographic metadata inspection

---

## Requirements

- Python 3.9+
- streamlit
- pandas
- plotly
- openpyxl
