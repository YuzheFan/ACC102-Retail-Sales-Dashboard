\# Retail Sales Performance Dashboard for Small Business Decision-Making



\## 1. Project Overview



This project is an interactive retail sales performance dashboard built with Python and Streamlit. It is designed to help small business users understand sales trends, product category performance, regional profit differences, and key business indicators.



The project was developed for the ACC102 Mini Assignment, Track 4: Interactive Data Analysis Tool.



\## 2. Problem and Intended User



Small business owners and store managers often need a simple way to explore sales and profit data without reading large raw transaction tables.



The analytical problem of this project is:



\*\*How can small business users identify important sales patterns and profit differences from retail transaction data?\*\*



The intended users are:



\- Small business owners

\- Store managers

\- Business students

\- Beginner data analysis learners



\## 3. Dataset



The project uses a sample retail sales dataset based on Superstore sales data. The dataset includes retail transaction information such as:



\- Order Date

\- Ship Date

\- Segment

\- Region

\- Category

\- Sub-Category

\- Sales

\- Quantity

\- Discount

\- Profit



The dataset is suitable for analysing retail performance because it contains both sales and profit information across different product categories, regions, and time periods.



Dataset source: Sample Superstore / Superstore.csv  

Access date: April 2026



The dataset file is included in the `data` folder as:



```text

data/retail\_sales.csv

4\. Python Methods Used



The project uses Python for data loading, cleaning, transformation, analysis, and visualisation.



Main Python methods include:



Loading CSV data with pandas

Inspecting missing values and duplicate records

Converting date columns into datetime format

Creating new variables such as Month, Year, and Profit Margin

Grouping data by month, category, region, and sub-category

Calculating key performance indicators

Creating charts with Plotly

Building an interactive dashboard with Streamlit

5\. Dashboard Features



The Streamlit dashboard includes:



Sidebar filters for date range, region, product category, and customer segment

Key performance indicators:

Total Sales

Total Profit

Total Quantity

Average Profit Margin

Total Orders

Monthly sales trend chart

Sales by product category chart

Profit by region chart

Top 10 sub-categories by sales chart

Summary tables

Automatically generated key findings based on selected filters

6\. Key Findings



The Python analysis produced several useful findings:



The highest monthly sales occurred in November 2018.

Technology was the strongest product category in both total sales and total profit.

The West region generated the highest total profit.

Phones was the top sub-category by total sales.

Sales and profit performance differ across categories and regions.



These findings can help small business users identify stronger product areas, profitable regions, and possible sales patterns.



7\. How to Run the App



To run this project locally, first install the required packages:



pip install -r requirements.txt



Then run the Streamlit app:



streamlit run app.py



The dashboard will open in a web browser.



8\. Repository Structure

ACC102-Retail-Sales-Dashboard/

│

├── app.py

├── analysis\_notebook.ipynb

├── README.md

├── requirements.txt

│

└── data/

&#x20;   └── retail\_sales.csv

9\. Limitations



This project has several limitations.



First, the dataset appears to be a sample retail dataset rather than real-time company data, so the results should be used for educational and exploratory analysis.



Second, the analysis is mainly descriptive. It does not include advanced forecasting, causal analysis, or predictive modelling.



Third, external factors such as marketing campaigns, competitor behaviour, economic conditions, and holiday effects are not included in the dataset.



Future improvements could include using more recent data, adding forecasting functions, including customer-level analysis, and improving profit margin analysis.



10\. Demo Video



Demo video link: To be added after recording.



11\. Product Link



GitHub repository link: https://github.com/YuzheFan/ACC102-Retail-Sales-Dashboard

