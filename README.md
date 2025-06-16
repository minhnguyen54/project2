# Car Maintenance Tracker

This Python-based Car Maintenance Tracker helps manage service records for multiple vehicles by logging data such as date, mileage, service type, cost, and notes. It provides visual insights through graphs showing cost trends, service frequency, and spending by service type.

## Features

- Add and track car maintenance records from a CSV file
- Summarizes total cost, number of services, and breakdown by vehicle
- Generates visualizations:
  - Cumulative cost over time
  - Cost distribution by service type (pie chart)
  - Frequency of each service performed (bar chart)

## Technologies Used

- Python 3
- pandas
- matplotlib
- seaborn

## Folder Structure

car-maintenance-tracker/
├── main.py
├── data/
│ └── maintenance_log.csv
├── plots/
│ ├── cost_over_time.png
│ ├── cost_by_service.png
│ └── service_frequency.png

## How to Run

1. Install dependencies:

2. Run the script:

3. View the generated plots in the `plots/` folder.

## Author

Minh Nguyen
