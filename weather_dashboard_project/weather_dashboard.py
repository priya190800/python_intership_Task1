import requests
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import argparse
import plotly.express as px

# ---------------------------
# Fetch weather data
# ---------------------------
def fetch_weather(city, api_key, units="metric"):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geo_resp = requests.get(geo_url)
    geo_resp.raise_for_status()
    geo = geo_resp.json()[0]
    lat, lon = geo["lat"], geo["lon"]

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units={units}&appid={api_key}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    records = []
    for entry in data["list"]:
        records.append({
            "datetime": entry["dt_txt"],
            "temp": entry["main"]["temp"],
            "feels_like": entry["main"]["feels_like"],
            "humidity": entry["main"]["humidity"],
            "weather": entry["weather"][0]["description"]
        })
    return pd.DataFrame(records)

# ---------------------------
# Save charts as PNG
# ---------------------------
def make_plots(df, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df["datetime"] = pd.to_datetime(df["datetime"])

    # Temperature chart
    plt.figure(figsize=(10, 5))
    plt.plot(df["datetime"], df["temp"], marker="o")
    plt.title("Temperature Forecast")
    plt.xlabel("Date/Time")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)
    plt.savefig(outdir / "temperature.png")
    plt.close()

    # Humidity chart
    plt.figure(figsize=(10, 5))
    plt.plot(df["datetime"], df["humidity"], marker="o", color="orange")
    plt.title("Humidity Forecast")
    plt.xlabel("Date/Time")
    plt.ylabel("Humidity (%)")
    plt.grid(True)
    plt.savefig(outdir / "humidity.png")
    plt.close()

# ---------------------------
# Make interactive HTML dashboard
# ---------------------------
def make_html_dashboard(df, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df["datetime"] = pd.to_datetime(df["datetime"])

    fig_temp = px.line(df, x="datetime", y="temp", title="Temperature Forecast")
    fig_humidity = px.line(df, x="datetime", y="humidity", title="Humidity Forecast")

    html_path = outdir / "dashboard.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write("<h1>Weather Dashboard</h1>")
        f.write("<h3>Generated from OpenWeatherMap API</h3>")
        f.write(fig_temp.to_html(full_html=False, include_plotlyjs="cdn"))
        f.write(fig_humidity.to_html(full_html=False, include_plotlyjs=False))
        f.write("<h3>Forecast Data (first 10 rows)</h3>")
        f.write(df.head(10).to_html(index=False))

    print(f"🌍 Interactive dashboard ready: {html_path}")

# ---------------------------
# Main execution
# ---------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", required=True, help="City name (e.g. Surat,IN)")
    parser.add_argument("--api-key", required=True, help="OpenWeatherMap API key")
    parser.add_argument("--units", default="metric", help="Units: metric, imperial")
    parser.add_argument("--outdir", default="output", help="Output directory")
    args = parser.parse_args()

    print(f"Fetching forecast for {args.city}...")
    df = fetch_weather(args.city, args.api_key, args.units)

    print("Generating charts...")
    make_plots(df, args.outdir)

    # NEW: Create interactive HTML dashboard
    make_html_dashboard(df, args.outdir)

    # Save CSV
    df.to_csv(Path(args.outdir) / "forecast1.csv", index=False)

    print("✅ Dashboard ready in:", args.outdir)