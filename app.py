import streamlit as st
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# Database connection setup using SQLAlchemy
@st.cache_resource
def get_connection():
    engine = create_engine("mysql+mysqlconnector://root:@localhost/redbus_data")
    return engine

# Function to fetch data from the database
@st.cache_data
def load_data():
    engine = get_connection()
    query = "SELECT * FROM route_data"
    df = pd.read_sql(query, engine)
    location_data = df['route']
    From = []
    To = []
    for i in location_data:
        From_1, To_1 = i.split(" to ")
        From.append(From_1)
        To.append(To_1)
    df["From"] = From
    df["To"] = To
    print(From, To)
    return df

# Streamlit app layout
def main():
    st.title("indian Bus Data")
    
    # Load data from the database
    data = load_data()


    # Show raw data
    if st.checkbox("Show raw data"):
        st.write(data)

    # Filtering options
    st.sidebar.header("Filter options")

    # Example filter: Filter by a column
    column_to_filter = st.sidebar.selectbox("Select a column to filter", data.columns)
    unique_values = data[column_to_filter].dropna().unique()
    selected_value = st.sidebar.selectbox(f"Filter {column_to_filter}", unique_values)

    # Apply filter to the data
    filtered_data = data[data[column_to_filter] == selected_value]

    # Show filtered data
    st.write(f"Filtered Data ({column_to_filter} = {selected_value})")
    st.write(filtered_data)

    # Additional features (e.g., downloading the filtered data as CSV)
    if st.button("Download filtered data as CSV"):
        csv = filtered_data.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name='filtered_data.csv', mime='text/csv')

if __name__ == "__main__":
    main()
