Mamaearth Sales and Returns Analysis
Project Overview
This project analyses MamaEarth order data to understand sales performance, product returns, and customer behaviour. It uses MySQL for database Queries, Python for data cleaning and analysis, and a narrative-generation script to turn the findings into business insights.
1.)	The Capstone_Project_NehaAgarwal_repo/data folder contains the provided data stored in the CSV format:
    1.) Customers.csv
    2.)  Products.csv
    3.)Orders.csv
        It also contains the two csv files 
    1.)	orders_clean.csv : contains the clean orders data which has been cleaned using EDA in python.
    2.)	Merged.csv – contains the merged data from products, orders and customers which is further used in analysis

2.)	SQL Layer — Database and Reports
The SQL files are stored in the Capstone_Project_NehaAgarwal_repo/ sql/ folder. Run them in the following order using MySQL Workbench:
1.	schema.sql – creates the database tables customers, products and orders.
2.	seed_data.sql – inserts the data into the tables.
3.	reports.sql – runs queries to analyse sales and returns.

3.)Data Cleaning, Analysis and Visualizations – Python   
•	Capstone_Project_NehaAgarwal_repo/analysis /clean_and_eda
First, run analysis/clean_and_eda.py to clean the order data, handle missing values and duplicates, check outliers, and perform exploratory data analysis. The cleaned data is saved as orders_clean.csv, and the merged data is saved as merged.csv for further analysis.
•	Capstone_Project_NehaAgarwal_repo/ analysis /visualize.py
            1.) return_rate_by_payment.png – compares return rates across payment methods.
            2.) monthly_revenue_trend.png – shows monthly revenue trends.
•	Both charts are saved in the Capstone_Project_NehaAgarwal_repo/ visualizations/ folder.

•	The key analysis results to Capstone_Project_NehaAgarwal_repo/ narrator/findings.json. This file contains the calculated data used in the final business narrative.
4). GenAI-Powered Insight Narrator – Business Insights

The final step is to run Capstone_Project_NehaAgarwal_repo/ narrator/generate_narrative.py. It reads narrator/findings.json and generates a business narrative in the Situation, Complication, and Resolution (SCR) format.
To use Gemini, set the API key.
Replace YOUR_API_KEY with your actual key and keep it private.
If no API key is available, run the script without setting the environment variable:
The script uses the offline fallback to generate the narrative from the existing findings without calling the Gemini API.
Execution Flow
Run the project in this order:
SQL setup and reports → Python cleaning and EDA → Visualizations and findings.json → SCR narrative generation
This sequence connects the original data to the final analysis and business insights.


