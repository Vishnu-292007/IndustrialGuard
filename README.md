# IndustrialGuard — Smart Industrial Anomaly Monitoring

IndustrialGuard is a Python-based industrial monitoring dashboard that simulates machine sensor readings and identifies potential anomalies using configurable thresholds.

## Features

- Monitor multiple simulated machines
- Generate temperature and vibration readings
- Configure sensor alert thresholds
- Classify readings as Normal, Medium, or Critical
- Display a demonstration machine health score
- Visualize sensor data with interactive charts
- View alerts and download data as CSV or JSON

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Installation

1. Clone this repository.
2. Open the project folder in your terminal.
3. Create and activate a virtual environment.
4. Install dependencies:

   pip install -r requirements.txt

5. Run the application:

   streamlit run app.py

## How It Works

The application generates simulated temperature and vibration readings. It compares the readings against user-defined thresholds and displays alerts when limits are exceeded.

## Limitations

This is a portfolio demonstration using simulated data. It does not connect to physical sensors, predict equipment failures using a trained machine-learning model, or provide validated industrial health assessments.

## Future Improvements

- Connect real sensors or an IoT data source
- Store historical readings in a database
- Add a trained anomaly-detection model
- Implement authentication and monitoring history
