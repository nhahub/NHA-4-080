
# Northy 🌊

**Egypt Coastal Hotels Market Intelligence**

🔗 **Live Website:** [[https://northy-hotel-directo-4qul.bolt.host](https://northy-hotel-directo-4qul.bolt.host)]

## 📖 Overview

Northy is a comprehensive market intelligence dashboard and data pipeline built to track and visualize hotel data across the North Coast of Egypt, Alexandria, and Marsa Matruh. The project aggregates listings from major booking platforms like Airbnb, Booking, and Hotels.com to provide insights into pricing trends, hotel ratings, and overall market composition.
![Northy Dashboard Interface](images/Interface.png)

## ✨ Features

* **Data Processing Pipeline**: Structured data layers following a Medallion architecture (Silver and Gold) for clean granular listings and aggregated market metrics.
* **Interactive Dashboard**: A responsive, custom-built HTML/CSS/JS dashboard tracking Key Performance Indicators (KPIs).
* **Live Slicing & Filtering**: Filter the market data dynamically by destination, source website, and rating bands.
* **Market Insights**: Real-time KPI tracking for Total Listings, Average Price per Night, Median Price, and Average Rating.

## 🔄 Workflow & Data Pipeline
* **Engineering Flow** (images/flow.png)


The project follows a structured methodology that begins with collecting raw listing data and ends with professional dashboard visualization. After the data is scraped, Databricks is used to execute ETL (Extract, Transform, Load) operations, organizing the data into a medallion architecture.

The flow of work is broken down into the following stages:

* **1. Data Scraping:** Raw hotel and accommodation records are collected from Airbnb, Booking, and Hotels.com.
* **2. Bronze Layer:** The original, uncleaned collected hotel records are preserved in this raw stage.
* **3. Silver Layer:** The data is transformed into a cleaned listing fact table. This detailed CSV layer supports advanced filtering and comprehensive pricing, rating, and source analysis.
* **4. Gold Layer:** The cleaned data is summarized into aggregated market metrics. This creates a dashboard-ready layer for executive reporting.
* **5. Application Storage (Lovable DB):** The finished Silver and Gold CSV outputs are uploaded to the Lovable application environment to power the user-facing database.
* **6. Reporting:** The final datasets are deployed to feed the interactive web dashboard, presentation visuals, and a Power BI-ready analysis workbook.

## 📂 Repository Structure

### 1. Data Engineering Layers

* **`data/Silver_Layer (1).csv`**: Contains the cleaned, granular listing data. Key columns include hotel `name`, `destination`, `price_egp`, `rating`, `url`, `source_website`, and `image_url`.
* **`data/Gold_Layer (1).csv`**: Contains the aggregated, presentation-ready market data. It summarizes `total_hotels`, `avg_price`, and `avg_rating` categorized by destination and source website.

### 2. Front-End Dashboard

* **`dashboard/Egypt_Hotels_PowerBI_Dashboard.html`**: The interactive user interface visualizing the processed data through scatter charts, bar charts, and KPI cards.

## 🚀 How to Access the Dashboard

You do not need to download or clone any files to explore the data!

Simply visit the live interactive dashboard here: [https://northy-hotel-directo-4qul.bolt.host]

## 📊 Visuals & Screenshots



* **Secondary Interface Overview:** ![Overview](images/Interface2.png)



* **Filtered Hotels View:** ![Filtered Hotels](images/Filtered_hotels.png)



* **Location Filters in Action:** ![Location Filters](images/Filters_according_to_locations.png)



* **Source Filters in Action:** ![Source Filters](images/Filter_according_to_sources.png)
## 🛠️ Built With

* **Data Processing:** Python / Pandas / Databricks
* **Front-End:** HTML5, CSS3, JavaScript (Vanilla JS / Chart.js)
* **Design System:** Fraunces & Inter fonts, FontAwesome icons
