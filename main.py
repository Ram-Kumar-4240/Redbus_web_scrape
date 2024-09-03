import streamlit as st
import mysql.connector as sconn
from mysql.connector import Error
import pandas as pd

def connection():
    try:
        config = {
            "user": "root",
            "password": "",
            "host": "localhost",
            "database": "redbus_data"
        }
        conn = sconn.connect(**config)
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"Connection Error: {e}")
        return None

def fetch_data(query, conn):
    try:
        df = pd.read_sql(query, conn)
        return df
    except Error as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

st.set_page_config(
    page_title="Redbus",
    page_icon=":oncoming_bus:",
    layout="wide",
)

# Add custom CSS to push the title upwards
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Centering the title using custom HTML
st.markdown("<h1 style='text-align: center; color: red;'>REDBUS - 🔍 Search Bus</h1>", unsafe_allow_html=True)

# Reduce the space between the title and filters
st.write("")  # Minimal space

# Layout adjustments
state_col, location_col, filter_col = st.columns([1, 2, 5])

# State filter first (smaller size)
with state_col:
    # Fetch unique values for the 'State' dropdown from the database
    conn = connection()
    if conn:
        state_query = "SELECT DISTINCT `state` FROM bus_data"
        state_options = ["--- Select State ---"] + fetch_data(state_query, conn)['state'].tolist()
        conn.close()
    else:
        state_options = ["--- Select State ---"]

    selected_state = st.selectbox("State", state_options)

# From and To filters (smaller and aligned horizontally)
if selected_state != "--- Select State ---":
    conn = connection()
    if conn:
        from_query = f"SELECT DISTINCT `From` FROM bus_data WHERE `state` = '{selected_state}'"
        to_query = f"SELECT DISTINCT `To` FROM bus_data WHERE `state` = '{selected_state}'"
        
        from_options = ["--- Select From Location ---"] + fetch_data(from_query, conn)['From'].tolist()
        to_options = ["--- Select To Location ---"] + fetch_data(to_query, conn)['To'].tolist()

        conn.close()
    else:
        from_options = ["--- Select From Location ---"]
        to_options = ["--- Select To Location ---"]

    with location_col:
        From = st.selectbox("From", from_options)
        To = st.selectbox("To", to_options)

# Other filters aligned to the right
with filter_col:
    # Filters Section - Align filters horizontally using columns
    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        price_range = st.slider("Price Range", 100, 5000, (500, 3000))
        dep_time_range = st.slider("Departing Time (Hour)", 0, 24, (6, 18))  # Time in 24-hour format

    with filter_col2:
        star_rating = st.slider("Star Rating", 1, 5, 3)
        reach_time_range = st.slider("Reaching Time (Hour)", 0, 24, (10, 22))

    with filter_col3:
        seats_available = st.slider("Seats Available", 1, 100, (10, 50))

        # Add Bus Type Filter below Seats Available
        bus_type_query = "SELECT DISTINCT `bustype` FROM bus_data"
        conn = connection()
        if conn:
            bus_type_options = ["All Types"] + fetch_data(bus_type_query, conn)['bustype'].tolist()
            conn.close()
        else:
            bus_type_options = ["All Types"]

        selected_bus_type = st.selectbox("Bus Type", bus_type_options)

# Fetch and display results on search
if st.button("SEARCH"):
    query = f"""
    SELECT * FROM bus_data
    WHERE `From` = '{From}' AND `To` = '{To}'
    AND star_rating >= {star_rating}
    AND price BETWEEN {price_range[0]} AND {price_range[1]}
    AND HOUR(departing_time) BETWEEN {dep_time_range[0]} AND {dep_time_range[1]}
    AND HOUR(reaching_time) BETWEEN {reach_time_range[0]} AND {reach_time_range[1]}
    AND seats_available BETWEEN {seats_available[0]} AND {seats_available[1]}
    """
    
    # Only filter by bus type if a specific type is selected (not "All Types")
    if selected_bus_type != "All Types":
        query += f" AND `bustype` = '{selected_bus_type}'"

    conn = connection()
    if conn:
        df = fetch_data(query, conn)

        if not df.empty:
            # Customize the displayed columns
            df = df[['busname', 'bustype', 'star_rating', 'price', 'departing_time', 'reaching_time', 'duration', 'seats_available', 'route_link']]
            
            # Add headers for the columns
            header_col1, header_col2, header_col3, header_col4, header_col5, header_col6, header_col7, header_col8, header_col9 = st.columns(9)
            header_col1.markdown("**Bus Name**")
            header_col2.markdown("**Bus Type**")
            header_col3.markdown("**Star Rating**")
            header_col4.markdown("**Price**")
            header_col5.markdown("**Departing Time**")
            header_col6.markdown("**Reaching Time**")
            header_col7.markdown("**Duration**")
            header_col8.markdown("**Seats Available**")
            header_col9.markdown("**Route Link**")

            # Display data in the same order as headers
            for i in range(len(df)):
                row = df.iloc[i]
                col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
                
                # Display row data
                col1.text(row['busname'])
                col2.text(row['bustype'])
                col3.text(f"{row['star_rating']}⭐")
                col4.text(f"₹{row['price']}")
                col5.text(row['departing_time'])
                col6.text(row['reaching_time'])
                col7.text(row['duration'])
                col8.text(row['seats_available'])
                
                # Add clickable link using markdown
                col9.markdown(f"[View Route]({row['route_link']})")

        else:
            st.error("No buses found for the selected filters.")
        conn.close()
    else:
        st.error("Failed to connect to the database.")
