#!/usr/bin/env python
# coding: utf-8

# # Graded Assignment (Python Project for Data Science)

# In[20]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[21]:


import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# In[22]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# ## Question 1 - Extracting Tesla Stock Data Using yfinance - 2 Points

# In[ ]:


import yfinance as yf

# Define the ticker symbol for Tesla
ticker_symbol_tesla = "TSLA"

# Create a ticker object for Tesla
tesla_ticker = yf.Ticker(ticker_symbol_tesla)

# Get historical market data for Tesla
tesla_data = tesla_ticker.history(period="max")

# Reset the index of the DataFrame
tesla_data.reset_index(inplace=True)

# Display the first five rows of the DataFrame
print(tesla_data.head())


# ## Question 2 - Extracting Tesla Revenue Data Using Webscraping - 1 Points

# In[42]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Save the HTML content as a variable named html_data
    html_data = response.text
    print("HTML data downloaded successfully.")
else:
    print("Failed to download HTML data. Status code:", response.status_code)
    
soup = BeautifulSoup(html_data, "html.parser")
table = soup.find_all("tbody")[1]

dates = []
revenues = []

for row in table.find_all("tr"):
    cols = row.find_all("td")

    if len(cols) == 2:
        date = cols[0].get_text().strip()
        revenue = cols[1].get_text().strip()
        dates.append(date)
        revenues.append(revenue)
        
tesla_revenue = pd.DataFrame({"Date": dates, "Revenue": revenues})

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")

tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

print(tesla_revenue.tail())


# ## Question 3 - Extracting GameStop Stock Data Using yfinance - 2 Points

# In[ ]:


import yfinance as yf

# Define the ticker symbol for GameStop
ticker_symbol_gme = "GME"

# Create a ticker object for GameStop
gme_ticker = yf.Ticker(ticker_symbol_gme)

gme_data = gme_ticker.history(period="max")

gme_data.reset_index(inplace=True)

# Display the first five rows of the DataFrame
print(gme_data.head())


# ## Question 4 - Extracting GameStop Revenue Data Using Webscraping - 1 Points

# In[48]:


import pandas as pd
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
response = requests.get(url)

if response.status_code == 200:
   
    soup = BeautifulSoup(response.content, "html.parser")
  
else:
    print("Failed to retrieve HTML data. Status code:", response.status_code)
    


table = soup.find_all("tbody")[1]
dates = []
revenues = []

for row in table.find_all("tr"):
    cols = row.find_all("td")
    
    if len(cols) == 2:
        # Extract date and revenue
        date = cols[0].get_text().strip()
        revenue = cols[1].get_text().strip()
        
        
        revenue = revenue.replace(",", "").replace("$", "")
        dates.append(date)
        revenues.append(revenue)

gme_revenue = pd.DataFrame({"Date": dates, "Revenue": revenues})
print(gme_revenue.tail())


# ## Question 5 - Tesla Stock and Revenue Dashboard - 2 Points

# In[ ]:


import matplotlib.pyplot as plt

# Define the make_graph function
def make_graph(stock_data, revenue_data, title):
    # Plot Tesla stock data
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Close'], label='Close Price', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Stock Price (USD)')
    plt.title(title + ' Stock Data')
    plt.legend()
    plt.grid(True)
    
    # Overlay revenue data as scatter plot
    plt.scatter(revenue_data['Date'], revenue_data['Revenue'], label='Revenue', color='red', marker='o')
    plt.legend(loc='upper left')
    
    # Show the plot
    plt.show()

# Call the make_graph function
make_graph(tesla_data, tesla_revenue, 'Tesla')


# ## Question 6: Plot GameStop Stock Graph

# In[ ]:


make_graph(gme_data, gme_revenue, 'GameStop')

