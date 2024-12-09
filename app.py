import streamlit as st
import pandas as pd
import plotly.express as px

# Ensure set_page_config is the first Streamlit command
st.set_page_config(
    page_title="Olympic Data Analysis",
    page_icon="🏅",
    layout="wide"
)

# Load data
@st.cache_data
def load_data(file_path):
    try:
        return pd.read_excel(file_path, sheet_name='athlete_events')
    except FileNotFoundError:
        st.error(f"File not found: {file_path}. Please check the file path and try again.")
        return pd.DataFrame()  # Return an empty DataFrame

# File path (update if necessary)
data = load_data("athlete_events Data set.xlsx")

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Analysis"])

# Home Page
if page == "Home":
    st.title("🏠 Welcome to the Olympic Athletes Data Analysis App!")
    st.write(
        """
        This app allows you to explore and analyze data about Olympic athletes.
        
        ### Features:
        - Filter athletes by year, sport, and medal type.
        - Visualize gender distribution and country medal counts.
        - Explore average athlete heights and weights by sport.
        
        ### How to Use:
        - Use the Navigation panel in the sidebar to switch between pages.
        - On the Data Analysis page, interact with the filters to customize the data and visualizations.
        """
    )
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg", width=400)


# Data Analysis Page
elif page == "Data Analysis":
    st.title("Olympic Athletes Data Analysis")

    if not data.empty:
        # Sidebar Filters
        st.sidebar.title("Filters")
        selected_year = st.sidebar.slider("Select Year Range", int(data['Year'].min()), int(data['Year'].max()), (2000, 2016))
        selected_sport = st.sidebar.selectbox("Select Sport", ["All"] + sorted(data['Sport'].unique().tolist()))
        selected_medal = st.sidebar.selectbox("Select Medal", ["All", "Gold", "Silver", "Bronze"])

        # Filter data based on selection
        filtered_data = data[
            (data['Year'] >= selected_year[0]) & (data['Year'] <= selected_year[1])
        ]
        if selected_sport != "All":
            filtered_data = filtered_data[filtered_data['Sport'] == selected_sport]
        if selected_medal != "All":
            filtered_data = filtered_data[filtered_data['Medal'] == selected_medal]

        # Display Filtered Data
        st.write("### Filtered Dataset")
        st.dataframe(filtered_data)

        # Gender Distribution Over the Years
        st.write("### Gender Distribution Over the Years")
        gender_trend = filtered_data.groupby(['Year', 'Sex']).size().reset_index(name='Count')
        gender_fig = px.line(gender_trend, x="Year", y="Count", color="Sex", title="Gender Distribution Over the Years")
        st.plotly_chart(gender_fig)

        # Medal Distribution by Country
        st.write("### Medal Distribution by Country")
        if selected_medal != "All":
            medal_data = filtered_data[filtered_data['Medal'].notnull()]
            medal_country = medal_data.groupby(['NOC', 'Medal']).size().reset_index(name='Count')
            medal_fig = px.bar(medal_country, x='NOC', y='Count', color='Medal', title="Medal Distribution by Country")
            st.plotly_chart(medal_fig)

        # Average Height and Weight by Sport
        st.write("### Average Height and Weight by Sport")
        avg_metrics = filtered_data.groupby('Sport')[['Height', 'Weight']].mean().reset_index()
        avg_fig = px.scatter(avg_metrics, x="Height", y="Weight", size="Height", color="Sport", title="Average Height and Weight by Sport")
        st.plotly_chart(avg_fig)
    else:
        st.warning("No data available to display. Please check your dataset.")
