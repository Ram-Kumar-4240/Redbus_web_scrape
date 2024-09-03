import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as sconn
from mysql.connector import Error
import pandas as pd

# Define a connection configuration to MySQL
def configuration():
    try:
        config = {
            "user": "root",
            "password": "",
            "host": "localhost",
            "database": "redbus_data"
        }
        return config
    except Error as e:
        st.error(f"Configuration Error: {e}")
        return None

def connection():
    try:
        config = configuration()
        if config is None:
            return None
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

# Page Configuration
st.set_page_config(
    page_title="Redbus",
    page_icon=":oncoming_bus:",
    layout="wide",
)

# Sidebar Styling and Menu Options
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Search Bus"],
        icons=["house-door-fill", "search"],
        menu_icon="bus",
        default_index=0
    )

# Home Page Content
if selected == "Home":
    st.title(":red[REDBUS] - Book Your Ride in Bus 🚌")
    st.image("https://i.pinimg.com/564x/04/6b/38/046b3884bbd9d16ba053a80c95b8f295.jpg", use_column_width=True, width=300)
    st.subheader("Redbus is an online platform for booking bus tickets across India and other countries.")
    st.markdown("""
        Redbus offers services in India, Malaysia, Indonesia, and more.
        You can book buses, hotels, and rental cars, providing a comprehensive travel solution.
    """)

# Search Bus Page Content
if selected == "Search Bus":
    st.title(":red[REDBUS] - 🔍 Search Bus")
    col1, col2 = st.columns([3, 1])

    # Fetch unique values for the 'State' dropdown from the database
    conn = connection()
    if conn:
        state_query = "SELECT DISTINCT `state` FROM route_data"
        state_options = ["--- Select State ---"] + fetch_data(state_query, conn)['state'].tolist()
        conn.close()
    else:
        state_options = ["--- Select State ---"]

    # State selection
    selected_state = st.selectbox("State", state_options)

    # Fetch unique values for 'From' and 'To' dropdowns based on the selected state
    if selected_state != "--- Select State ---":
        conn = connection()
        if conn:
            from_query = f"SELECT DISTINCT `From` FROM route_data WHERE `state` = '{selected_state}'"
            to_query = f"SELECT DISTINCT `To` FROM route_data WHERE `state` = '{selected_state}'"
            
            from_options = ["--- Select From Location ---"] + fetch_data(from_query, conn)['From'].tolist()
            to_options = ["--- Select To Location ---"] + fetch_data(to_query, conn)['To'].tolist()

            conn.close()
        else:
            from_options = ["--- Select From Location ---"]
            to_options = ["--- Select To Location ---"]

        # State and Route selection
        with col1:
            From = st.selectbox("From", from_options)
            To = st.selectbox("To", to_options)

        # Filters Section
        with col2:
            price_range = st.slider("Price Range", 100, 5000, (500, 3000))
            star_rating = st.slider("Star Rating", 1, 5, 3)
            start_time = st.slider("Starting Time", 0, 24, (6, 22))

        # Fetch and display results on search
        if st.button("SEARCH"):
            query = f"""
            SELECT * FROM route_data
            WHERE `From` = '{From}' AND `To` = '{To}'
            AND star_rating >= {star_rating}
            AND price BETWEEN {price_range[0]} AND {price_range[1]}
            """
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
    else:
        st.error("Please select a state to continue.")
