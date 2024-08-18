import streamlit as st
import requests
import json
from datetime import datetime

# RapidAPI key
RAPIDAPI_KEY = "ef226c67f5mshd6b7804d788181dp149128jsn57bc02f8868f"

# List of ticker symbols
tickers = ["AEE", "REZ", "1AE", "1MC", "NRZ"]

# Function to get announcements for a given ticker using scrapeninja API to bypass Imperva Incapsula
def get_announcements(ticker):
    url = 'https://scrapeninja.p.rapidapi.com/scrape'
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "scrapeninja.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    payload = {
        "url": f"https://www.asx.com.au/asx/1/company/{ticker}/announcements?count=20&market_sensitive=false",
        "method": "GET",
        "retryNum": 1,
        "geo": "us"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


# Function to convert ISO 8601 datetime to a readable format
def convert_datetime(iso_datetime_str):
    parsed_datetime = datetime.strptime(iso_datetime_str, "%Y-%m-%dT%H:%M:%S%z")
    return parsed_datetime.strftime("%d-%m-%Y %H:%M:%S")  # Adjust format as needed

# Streamlit application
st.markdown("<h1>📈 Stock Announcements</h1>", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("Filters")
show_trading_halt = st.sidebar.checkbox("Show only 'Trading Halt' announcements")

# Checkbox filters for additional fields
show_document_date = st.sidebar.checkbox("Show Document Date")
show_relative_url = st.sidebar.checkbox("Show Relative URL")
show_market_sensitive = st.sidebar.checkbox("Show Market Sensitivity")
show_legacy_announcement = st.sidebar.checkbox("Show Legacy Announcement Status")
show_issuer_code = st.sidebar.checkbox("Show Issuer Code")
show_issuer_short_name = st.sidebar.checkbox("Show Issuer Short Name")

# Select a ticker symbol
selected_ticker = st.selectbox("Select Ticker Symbol", tickers)

# Get announcements for the selected ticker
if selected_ticker:
    data = get_announcements(selected_ticker)
    announcements = json.loads(data['body'])['data']
    
    # Extract issuer full name from the first announcement
    issuer_full_name = announcements[0]['issuer_full_name'] if announcements else "Unknown"


    # Filter based on checkbox selection
    if show_trading_halt:
        announcements = [a for a in announcements if "Trading Halt" in a['header']]
        if not announcements:
            st.write(f"No trading halt announcement for ticker: {selected_ticker}")

    st.markdown(f"### Announcements for {selected_ticker} <span style='font-size:25px;'> - {issuer_full_name}</span>", unsafe_allow_html=True)

    for announcement in announcements:
        # Convert the document release date to a readable format
        readable_release_date = convert_datetime(announcement['document_release_date'])
        st.write(f"- **{readable_release_date}**: {announcement['header']}")
        st.write(f"  [Link to Document]({announcement['url']})")
        st.write(f"  Number of Pages: {announcement['number_of_pages']}, Size: {announcement['size']}")
        
        # Display additional fields based on user selection
        if show_document_date:
            readable_document_date = convert_datetime(announcement['document_date'])
            st.write(f"  Document Date: {readable_document_date}")
        if show_relative_url:
            st.write(f"  Relative URL: {announcement['relative_url']}")
        if show_market_sensitive:
            st.write(f"  Market Sensitive: {announcement['market_sensitive']}")
        if show_legacy_announcement:
            st.write(f"  Legacy Announcement: {announcement['legacy_announcement']}")
        if show_issuer_code:
            st.write(f"  Issuer Code: {announcement['issuer_code']}")
        if show_issuer_short_name:
            st.write(f"  Issuer Short Name: {announcement['issuer_short_name']}")
        
        st.write("---")

st.write("**Note:** This application fetches data from the ScrapeNinja API. Ensure you have a valid API key and subscription.")

