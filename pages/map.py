import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

from pages.demographic_data import demographic_df

#demographic_df = pd.read_csv(r'C:\Users\JessicaMahendran\OneDrive - lumilinks.com\Desktop\streamlit_in_snowflake\demographic_df.csv')

map_df = demographic_df[['Zip', 'Cluster']].copy()

# Generate random lat/lon within a reasonable US range (adjust as needed)
np.random.seed(42)  # For reproducibility
map_df['latitude'] = np.random.uniform(24.396308, 49.384358, size=len(map_df))
map_df['longitude'] = np.random.uniform(-125.000000, -66.934570, size=len(map_df))

# Define cluster colors
cluster_colors = {
    1: [255, 0, 0],   # Red
    2: [0, 255, 0],   # Green
    3: [255, 165, 0]  # Orange (Better than blue for visibility)
}

# Assign colors based on Cluster values
map_df['color'] = map_df['Cluster'].map(cluster_colors)

# Pydeck Layer with Tooltip
layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_df,
    get_position=["longitude", "latitude"],
    get_color="color",
    get_radius=20000,  # Adjust dot size
    pickable=True,
    tooltip=True
)

# View Settings
view_state = pdk.ViewState(
    latitude=map_df["latitude"].mean(),
    longitude=map_df["longitude"].mean(),
    zoom=4
)

# Define Tooltip
tooltip = {
    "html": "<b>Cluster:</b> {Cluster}",
    "style": {"backgroundColor": "white", "color": "black"}
}

# Render Map with Light Theme
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="light", tooltip=tooltip))

# Display Legend (Key)
st.markdown("### Cluster Color Legend")
st.markdown(
    """
    <div style="display: flex; gap: 10px;">
        <div style="width: 20px; height: 20px; background-color: #FF0000; display: inline-block;"></div> Cluster 1 (Red)  
        <div style="width: 20px; height: 20px; background-color: #00FF00; display: inline-block;"></div> Cluster 2 (Green)  
        <div style="width: 20px; height: 20px; background-color: #FFA500; display: inline-block;"></div> Cluster 3 (Orange)  
    </div>
    """,
    unsafe_allow_html=True
)
