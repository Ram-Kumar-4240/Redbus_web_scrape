# Redbus Data Scraping with Selenium & Streamlit

Project Summary: This project automates the extraction of bus route and travel data from the Redbus website using Selenium, and presents the data through an interactive Streamlit web application. The tool allows users to filter bus routes based on various criteria such as state, departure and arrival times, ticket price, star rating, and seat availability, making it a valuable tool for customers, market analysts, and travel agencies.
## Key Features:

Web Scraping: Automated data collection from the Redbus website using Selenium.
SQL Database: Efficient storage of scraped data in a structured SQL database.
Dynamic Filtering: A Streamlit-based web app to visualize and filter bus route data by state, departure, seat availability, and more.
Responsive and Interactive: Real-time data interaction with SQL backend for efficient data fetching and filtering.
## Skills Developed:

Web Scraping with Selenium
Streamlit for interactive applications
SQL for database management
Python for data processing and analysis
Data cleaning and manipulation
## Business Use Cases:

Travel Aggregators: Offer customers real-time information on bus schedules and seat availability.
Market Analysis: Identify travel patterns for business strategy and marketing.
Customer Experience: Enhance user experience by offering filtered and customized bus travel options.
Competitor Analysis: Compare prices and services with other providers.
## Technology Stack:

Python: Core programming language.
Selenium: For automated web scraping.
Streamlit: For building the front-end application.
SQL/MySQL: For storing and querying scraped data.
Pandas: For data manipulation.
## How to Run the Project:

Clone the Repository: git clone [https://github.com/Ram-Kumar-4240/redbus_web_scrape.git]
Install Requirements:
Copy code
```Python
pip install -r requirements.txt
```
Scrape Data: Run the Python script for Selenium web scraping to fetch bus route data.
Upload Data to SQL Database: Store the scraped data in a MySQL database.
Run Streamlit App:
Arduino
Copy code
```Python
streamlit run app.py
```
Filter Data: Use the app’s intuitive interface to filter bus routes by state, price range, seat availability, and more.
## Future Enhancements:

Real-time data updates using APIs.
Advanced filtering with machine learning models.
Deployment on a cloud platform for broader accessibility.
## Credits: Developed by Ram Kumar.
