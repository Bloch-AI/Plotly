import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration as the very first Streamlit command
st.set_page_config(page_title="Interactive FIFA Data Dashboard", layout="wide")

# Inject custom CSS for Roboto font and blue slider styling
st.markdown("""
    <style>
    /* Import the Roboto font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    
    /* Custom slider styling for WebKit browsers */
    input[type="range"]::-webkit-slider-thumb {
        background: #007BFF !important;
    }
    input[type="range"]::-webkit-slider-runnable-track {
        background: #007BFF !important;
    }
    
    /* Custom slider styling for Mozilla browsers */
    input[type="range"]::-moz-range-thumb {
        background: #007BFF !important;
    }
    input[type="range"]::-moz-range-track {
        background: #007BFF !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Interactive FIFA Data Dashboard")

# Load the dataset with caching to speed up reloads
@st.cache_data
def load_data():
    df = pd.read_csv("FIFA DATA.csv")
    return df

df = load_data()

# -------------------------------
# Sidebar for interactive filters
# -------------------------------
st.sidebar.header("Filter Options")

# Filter: Age range slider
age_min, age_max = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", age_min, age_max, (age_min, age_max))

# Filter: Overall rating range slider
overall_min, overall_max = int(df['OverallRating'].min()), int(df['OverallRating'].max())
overall_range = st.sidebar.slider("Select Overall Rating Range", overall_min, overall_max, (overall_min, overall_max))

# Filter: Nationality multiselect
nationality_options = sorted(df['Nationality'].unique())
selected_nationalities = st.sidebar.multiselect("Select Nationalities", nationality_options, default=nationality_options)

# Apply filters to the DataFrame
filtered_df = df[
    (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1]) &
    (df['OverallRating'] >= overall_range[0]) & (df['OverallRating'] <= overall_range[1]) &
    (df['Nationality'].isin(selected_nationalities))
]

st.sidebar.markdown(f"**Filtered Players:** {filtered_df.shape[0]}")

# Option to show raw filtered data
if st.sidebar.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.dataframe(filtered_df)

# Additional interactive options for the plots
bins = st.sidebar.slider("Number of bins for histogram", 10, 50, 20)
bubble_scale = st.sidebar.slider("Bubble size scale factor", 10, 100, 30)

# -------------------------------
# Layout: Display plots in two columns
# -------------------------------
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

# -------------------------------
# Bar Chart: Top 10 Clubs by Average Overall Rating
# -------------------------------
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




