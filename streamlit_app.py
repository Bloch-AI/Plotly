import streamlit as st
import pandas as pd
import plotly.express as px

# Set the title for the Streamlit app
st.title("FIFA Data Dashboard")

# Load the dataset (adjust the file path if necessary)
df = pd.read_csv("FIFA DATA.csv")

# ----------------------------------
# 1. Histogram: Distribution of Player Overall Ratings
# ----------------------------------
fig1 = px.histogram(
    df, 
    x='OverallRating',  # Using the 'OverallRating' column for player ratings
    nbins=20,
    title="Distribution of Player Overall Ratings",
    labels={"OverallRating": "Overall Rating", "count": "Number of Players"}
)
fig1.update_layout(bargap=0.1)
st.plotly_chart(fig1, use_container_width=True)

# ----------------------------------
# 2. Scatter Plot: Age vs Overall Rating
# (Bubble size represents Player Value and colours represent Nationality)
# ----------------------------------
fig2 = px.scatter(
    df,
    x='Age',
    y='OverallRating',  # Using the 'OverallRating' column for player ratings
    size='Value ',      # Using the 'Value ' column to represent player value (ensure the column name matches exactly)
    color='Nationality',
    hover_name='Name',  # Displays the player's name on hover
    title="Player Age vs Overall Rating (Bubble size represents Value)",
    size_max=30         # Maximum bubble size for clarity
)
fig2.update_layout(xaxis_title="Age", yaxis_title="Overall Rating")
st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------
# 3. Bar Chart: Top 10 Clubs by Average Overall Rating
# ----------------------------------
# Calculate the average overall rating per club and sort in descending order
club_avg = df.groupby('Club', as_index=False)['OverallRating'].mean()
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

