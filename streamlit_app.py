#**********************************************
# Interactive FIFA Data Dashboard
# Version 1.0
# 5th March 2025
# Jamie Crossman-Smith
# jamie@bloch.ai
#**********************************************
# This Streamlit app demonstrates how you can filter, visualise, and explore data
# from the FIFA dataset using interactive charts and controls.
#
# The app does the following:
# 1. Loads and caches the FIFA data.
# 2. Lets you filter players by Age, Overall Rating, and Nationality.
# 3. Shows a histogram of player Overall Ratings, with an adjustable number of bins.
# 4. Displays a scatter plot of Age vs. Overall Rating, where bubble sizes represent Value.
# 5. Presents a bar chart of the Top 10 Clubs by average Overall Rating.
# 6. Pins a custom footer at the bottom of the page.
#
# In simple terms, this dashboard uses sliders and multiselect options in the sidebar
# to help you explore the data. The filters dynamically update all the charts so you
# can quickly see how different subsets of the data compare.
#
# This type of interactive approach is common in modern data exploration, allowing
# users to quickly spot trends and insights without having to write additional code.
#
#**********************************************

import streamlit as st
import pandas as pd
import plotly.express as px

# IMPORTANT: set_page_config must be the very first Streamlit command
st.set_page_config(page_title="Interactive FIFA Data Dashboard", layout="wide")

# -----------------------------------------------------------------------------
# Custom CSS to:
#  - Use Roboto font
#  - Override Streamlit slider colours to blue (if possible)
#  - Adjust the title's style (larger font and negative top margin)
#  - Pin the footer to the bottom
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Import the Roboto font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }

    /* Title styling */
    .big-title {
        font-size: 3em !important;
        font-weight: 700 !important;
        margin-top: -40px !important; /* Move the title up */
        margin-bottom: 20px !important;
    }

    /* Modern browsers: use accent-color for range inputs */
    input[type="range"] {
        accent-color: #007BFF;
    }
    
    /* Attempt to override Base Web slider styling used by Streamlit */
    [data-baseweb="slider"] * {
        --bds-primary: #007BFF !important;
        --bds-accent: #007BFF !important;
    }

    /* Fallback for potential slider classes */
    .stSlider .css-1544gdk,
    .stSlider .css-1cuwqtl {
        background-color: #007BFF !important;
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: black;
        color: white;
        text-align: center;
        padding: 10px 0;
        z-index: 9999; /* Ensure footer stays on top */
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Custom Title
# -----------------------------------------------------------------------------
st.markdown('<h1 class="big-title">Interactive FIFA Data Dashboard</h1>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Data Loading
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("FIFA DATA.csv")
    return df

df = load_data()

# -----------------------------------------------------------------------------
# Sidebar for Interactive Filters
# -----------------------------------------------------------------------------
st.sidebar.header("Filter Options")

# Filter: Age Range
age_min, age_max = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", age_min, age_max, (age_min, age_max))

# Filter: Overall Rating Range
overall_min, overall_max = int(df['OverallRating'].min()), int(df['OverallRating'].max())
overall_range = st.sidebar.slider("Select Overall Rating Range", overall_min, overall_max, (overall_min, overall_max))

# Filter: Nationality
nationality_options = sorted(df['Nationality'].unique())
selected_nationalities = st.sidebar.multiselect("Select Nationalities", nationality_options, default=nationality_options)

# Apply Filters
filtered_df = df[
    (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1]) &
    (df['OverallRating'] >= overall_range[0]) & (df['OverallRating'] <= overall_range[1]) &
    (df['Nationality'].isin(selected_nationalities))
]

st.sidebar.markdown(f"**Filtered Players:** {filtered_df.shape[0]}")

# Option to Show Raw Filtered Data
if st.sidebar.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.dataframe(filtered_df)

# Additional Interactive Options for the Plots
bins = st.sidebar.slider("Number of bins for histogram", 10, 50, 20)
bubble_scale = st.sidebar.slider("Bubble size scale factor", 10, 100, 30)

# -----------------------------------------------------------------------------
# Layout: Display Plots in Two Columns
# -----------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribution of Player Overall Ratings")
    fig1 = px.histogram(
        filtered_df,
        x='OverallRating',
        nbins=bins,
        title="Distribution of Player Overall Ratings",
        labels={"OverallRating": "Overall Rating", "count": "Number of Players"}
    )
    fig1.update_layout(bargap=0.1)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Player Age vs Overall Rating")
    fig2 = px.scatter(
        filtered_df,
        x='Age',
        y='OverallRating',
        size='Value ',          # Ensure the column name matches exactly
        color='Nationality',
        hover_name='Name',
        title="Player Age vs Overall Rating (Bubble size represents Value)",
        size_max=bubble_scale
    )
    fig2.update_layout(xaxis_title="Age", yaxis_title="Overall Rating")
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------------------------------------------------
# Bar Chart: Top 10 Clubs by Average Overall Rating
# -----------------------------------------------------------------------------
st.subheader("Top 10 Clubs by Average Overall Rating")
club_avg = filtered_df.groupby('Club', as_index=False)['OverallRating'].mean()
club_avg = club_avg.sort_values(by='OverallRating', ascending=False).head(10)

fig3 = px.bar(
    club_avg,
    x='Club',
    y='OverallRating',
    title="Top 10 Clubs by Average Overall Rating",
    labels={"OverallRating": "Average Overall Rating", "Club": "Club"}
)
fig3.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------------------------------------------------
# Footer Section
# -----------------------------------------------------------------------------
footer = st.container()
footer.markdown(
    '''
    <div class="footer">
        <p>© 2025 Bloch AI LTD - All Rights Reserved. 
        <a href="https://www.bloch.ai" style="color: white;">www.bloch.ai</a></p>
    </div>
    ''',
    unsafe_allow_html=True
)
