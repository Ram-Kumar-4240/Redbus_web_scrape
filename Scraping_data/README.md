
# Scraping Data

## First import required packages

```Python
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
```
## Extract all the state name and state link

```Python
def extract_links_by_class(url):
    driver=webdriver.Chrome() # set the driver
    driver.get(url) # open webdriver
    driver.maximize_window() # maximize 
    
# In this part for Using Key element scrolldown the website

    driver.find_element(By.TAG_NAME,"body").send_keys(Keys.PAGE_DOWN)
    time.sleep(1) # waiting time 1 sceond

# Find a tag with By method and XPATH
    view_all = driver.find_elements(By.XPATH,"//a[@class='OfferSection__ViewAllText-sc-16xojcc-1 eVcjqm']") # find a tag class and paste in here 
    ref=view_all[1].get_attribute('href') # Extract href from a tag
    time.sleep(2)
    driver.get(ref) # open link Extract from href tag

    links = driver.find_elements(By.XPATH,"//a[@class='D113_link']") # Find all state link using XPATH 

# Extract all state name and href link from a tag
    state_route_links = []
    for link in links:
        state = link.text # Extract state
        href = link.get_attribute("href") # Extract href link
        if href:
            route_links = href
        state_route_links.append((state, route_links))
    driver.quit() # close drive
    return state_route_links

url = "https://www.redbus.in/" # link for open drive

# call the function and store the data in route_links
route_links  = extract_links_by_class(url) 
```
## Maping extracted value to Correct state name

```Python
state = {'PEPSU (Punjab)':"Punjab",
         'Himachal Pradesh Tourism Development Corporation (HPTDC)':"Himachal Pradesh",
         'RSRTC':"Rajasthan",
         'PEPSU (Punjab)':"Punjab",
         'UPSRTC':"uttar pradesh",
         'Chandigarh Transport Undertaking (CTU)':"Chandigarh",
         'HRTC':"Himachal Pradesh",
         'BSRTC Operated By VIP Travels':"Kathmandu",
         'South Bengal State Transport Corporation (SBSTC)':"South Bengal",
         'NORTH BENGAL STATE TRANSPORT CORPORATION':"North BenGal",
         'Bihar State Tourism Development Corporation (BSTDC)':"Bihar",
         'WBTC (CTC)':"West Bengal",
         'West Bengal Transport Corporation':"West Bengal",
         'Bihar State Road Transport Corporation (BSRTC)':"Bihar",
         'Sikkim Nationalised Transport (SNT)':"Sikkim",
         'Assam State Transport Corporation (ASTC)':"Assam",
         'KAAC TRANSPORT':"Assam",
         'Meghalaya Transport Corporation(MTC)':"Meghalaya",
         'Kadamba Transport Corporation Limited (KTCL)':"Goa",
         'TNSTC':"Tamil Nadu",
         'APSRTC':"Andhra Pradesh",
         'Puducherry Road Transport Corporation (PRTC)':"Puducherry",
         'TSRTC':"Telangana",
         'KSRTC (Kerala)':"Kerala",
         'GSRTC':"Gujarat",
         }
state_rout_link = [] 
for i, k in route_links:
    state_rout_link.append((state[i],k))
```
## Extract all routes by state link

```Python
def extract_links_by_class(state, url, class_name):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

    routes = []

# route_function() for Extract all bus route in one page

    def route_function(): 
        route_elements = driver.find_elements(By.CLASS_NAME, class_name)
        routes_ = [] 
        for route_element in route_elements:
            route_ = route_element.text  
            route_link_ = route_element.get_attribute('href')
            routes_.append((state, route_, route_link_))
        return routes_
# scrolldown the page and click the next page
    try:
        body_element = driver.find_element(By.TAG_NAME, "body") # find body element for scrolldown 
        for _ in range(3): # scrolldown 3 time 
            body_element.send_keys(Keys.PAGE_DOWN) 
            time.sleep(1)          
        view_buses_button = driver.find_elements(By.CLASS_NAME, 'DC_117_pageTabs ') # find all nextpage button like page 2, page 3, page 4
# navigate to next pages
        for i in range(len(view_buses_button)):
            if view_buses_button:
                view_buses_button[i].click()
                routes.append(route_function())
            else:
                print("No button found")

        driver.quit()
            
    except Exception as e:
        print("Error occurred:", e)
        driver.quit()
    return routes

# extract all bus routes
routes = []
for state, link in state_rout_link:
    div_locator_1 = "route" 
    routes.append(extract_links_by_class(state, link, div_locator_1)) 
```

## limit the extracting data only 10 route per state (Optional)
```Python

dic = {}
bus_routes = []
for i in routes:
    for j in i:
        for k,l,p in j:
            if k not in dic:
                dic[k] = 1
            else:
                dic[k] += 1
            if dic[k]<= 10:
                  bus_routes.append((k,l,p))

len(bus_routes) # find count of route
```
## extracting bus data by using bus route link (Add )

```Python
# set for date and time (Optional)
"""def convert_to_datetime(time_str, reference_date):
    try:
        dt = datetime.strptime(time_str, '%H:%M').replace(year=reference_date.year, month=reference_date.month, day=reference_date.day)
        return dt
    except ValueError:
        return None"""

count = 0 # count of route link
bus_details = []
for state, route, route_link in bus_routes:
            try:
                driver = webdriver.Chrome()
                driver.get(route_link)
                driver.maximize_window()
                time.sleep(5) # waiting for loading time of web page
                view_buses_button = driver.find_element(By.CLASS_NAME, 'button') # view bus button for view government buses
                view_buses_button.click()
                time.sleep(1)

                body_element = driver.find_element(By.TAG_NAME, "body") 
                for _ in range(20): # scrolldown 20 times for extract all data 
                    body_element.send_keys(Keys.PAGE_DOWN)          
                time.sleep(2)  # Wait to load the page


            except:
                pass 
# Find all the bus detail element 

            try:
                bus_elements = driver.find_elements(By.CSS_SELECTOR, "div.bus-item")
            except:
                print("No bus elements found")
                continue
# extract all bus data one by one 

            for bus in bus_elements:
                try:
                    busname = bus.find_element(By.CSS_SELECTOR, "div.travels.lh-24.f-bold.d-color").text
                except:
                    busname = "N/A"

                try:
                    bustype = bus.find_element(By.CSS_SELECTOR, "div.bus-type.f-12.m-top-16.l-color.evBus").text
                except:
                    bustype = "N/A"

                try:
                    departing_time = bus.find_element(By.CSS_SELECTOR, "div.dp-time.f-19.d-color.f-bold").text
                    # departing_time_dt = convert_to_datetime(departing_time, datetime.now())
                except:
                    departing_time_dt = None

                try:
                    duration = bus.find_element(By.CSS_SELECTOR, "div.dur.l-color.lh-24").text
                except:
                    duration = "N/A"
                try:
                    reaching_time = bus.find_element(By.CSS_SELECTOR, "div.bp-time.f-19.d-color.disp-Inline").text
                    # reaching_time_dt = convert_to_datetime(reaching_time, datetime.now())
                    if reaching_time_dt and departing_time_dt and reaching_time_dt < departing_time_dt:
                        reaching_time_dt += timedelta(days=1)
                except:
                    reaching_time_dt = None

                try:
                    star_rating = bus.find_element(By.CSS_SELECTOR, "div.rating-sec.lh-24").text
                    star_rating = float(star_rating) if star_rating != "N/A" else 0.0
                except:
                    star_rating = 0.0

                try:
                    price = bus.find_element(By.CSS_SELECTOR, "span.f-19.f-bold").text
                    price = float(price.replace('₹', '').replace(',', '').strip()) if price != "N/A" else None
                except:
                    price = None

                try:
                    try:
                        seats_available = bus.find_element(By.CSS_SELECTOR, "div.seat-left.m-top-16").text
                    except:
                        seats_available = bus.find_element(By.CSS_SELECTOR, "div.seat-left.m-top-30").text

                    seats_available = int(seats_available.split()[0]) if seats_available != "N/A" else 0
                except:
                        seats_available = 0
                bus_details.append((route, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available, state)) # append all the data to bus_details
            count+=1
            print(count)
```
## Setting DataFrame and columns

```Python
import pandas as pd

columns = ['route', 'route_link', 'busname', 'bustype','departing_time','duration','reaching_time','star_rating','price','seats_available', 'state']
redbus_data =  pd.DataFrame(bus_details,columns=columns)
```
## Added From and To columns using route
```Python
From = []
To = []
location_data = redbus_data['route']
for i in location_data:
    From_1, To_1 = i.split(" to ")
    From.append(From_1)
    To.append(To_1)
redbus_data["From"] = From
redbus_data["To"] = To
```
## Converted to csv file for safty perpuse 

```Python
redbus_data.to_csv("redbus_data.csv")
```
## Upload Sql database

```Python
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import mysql.connector

# Your MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
)

# Create a SQLAlchemy engine
engine = create_engine('mysql+mysqlconnector://root:@localhost/redbus_data')

try:
    redbus_data.to_sql('route_data', con=engine, if_exists='replace', index=False)
    print("Data uploaded successfully!")

except SQLAlchemyError as e:
    print(f"An error occurred: {e}")
```



