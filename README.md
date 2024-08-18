# Streamlit AU Stock Announcements
Streamlit application to view top 20 AU stock announcements 

This Streamlit application provides a user-friendly interface for displaying and filtering stock announcements from the Australian Stock Exchange (ASX). It utilizes the ScrapeNinja API to fetch and present recent announcements for selected ticker symbols.

## Features

- **Ticker Selection**: Choose from a list of ticker symbols to fetch announcements.
- **Filters**:
  - **Show only 'Trading Halt' announcements**: Filter announcements to show only those related to trading halts.
  - **Additional Fields**: Optionally display extra fields for each announcement, including:
    - Document Date
    - Relative URL
    - Market Sensitivity
    - Legacy Announcement Status
    - Issuer Code
    - Issuer Short Name
- **Date Conversion**: Converts ISO 8601 date formats to a more readable format.

