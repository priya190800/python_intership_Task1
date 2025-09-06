# Weather Dashboard (OpenWeatherMap + Seaborn)

## Overview
This project fetches weather forecast data from OpenWeatherMap API and visualizes it using **Seaborn** and **Matplotlib**.

## Features
- Fetches **5-day/3-hour forecast**
- Saves clean CSV
- Generates charts:
  - Temperature trend
  - Humidity trend
  - Wind speed distribution

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Get a free API key from [OpenWeatherMap](https://openweathermap.org/).
3. Run:
   ```bash
   python weather_dashboard.py --city "Surat,IN" --api-key YOUR_API_KEY
   ```

## Outputs
- `output/forecast.csv` – forecast data
- `output/temp_trend.png` – temperature trend
- `output/humidity_trend.png` – humidity trend
- `output/wind_distribution.png` – wind distribution

