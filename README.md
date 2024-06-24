# PayReco
Payment Reconciliation Application

This project provides a Streamlit-based dashboard for analyzing ecommerce data. It allows users to upload CSV files and view various metrics and analyses.

## Features

- Upload CSV files for data analysis.
- View key metrics such as total orders, gross profit, net profit, etc.
- Analyze critical orders, location-based order distribution, and SKU-level analytics.

## How to Run

1. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the Streamlit application:
    ```bash
    streamlit run src/app.py
    ```

3. Upload a CSV file through the Streamlit interface to view the analytics dashboard.

## File Structure

- **data/**: Contains CSV files for analysis.
- **src/**: Source code for the application.
    - `app.py`: Main application file.
    - `data_loader.py`: Functions for loading and cleaning data.
    - `metrics_calculator.py`: Functions for calculating metrics.
    - `plot_helpers.py`: Functions for generating plots and displaying results.
- **tests/**: Contains unit tests for the modules.

