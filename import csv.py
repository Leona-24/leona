import csv
from datetime import datetime, timedelta

# Step 1: Load and clean the dataset
dates = []
unique_visits = []

with open(r"C:\Users\leona\Downloads\daily-website-visitors.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            date = datetime.strptime(row['Date'], "%m/%d/%Y")
            visits = int(row['Unique.Visits'].replace(",", ""))
            dates.append(date)
            unique_visits.append(visits)
        except Exception as e:
            print(f"Skipping row due to error: {e}")

# Step 2: Forecast using simple moving average (last 7 days)
def moving_average_forecast(data, window_size, forecast_days):
    forecasts = []
    temp_data = data.copy()
    for i in range(forecast_days):
        window = temp_data[-window_size:]
        avg = sum(window) // window_size
        forecasts.append(avg)
        temp_data.append(avg)  # Add to temp list for rolling forecast
    return forecasts

# Step 3: Forecast next 30 days
forecast_days = 30
forecast = moving_average_forecast(unique_visits, window_size=7, forecast_days=forecast_days)

# Step 4: Create future dates
last_date = dates[-1]
forecast_dates = [last_date + timedelta(days=i+1) for i in range(forecast_days)]

# Step 5: Display output
print("\nForecasted Unique Visitors (Next 30 Days):")
print("Date\t\tPredicted Visitors")
for date, visitors in zip(forecast_dates, forecast):
    print(f"{date.strftime('%Y-%m-%d')}\t{visitors}")

# Step 6: Save to CSV
output_file = r"C:\Users\leona\Downloads\forecast_output.csv"
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Predicted Unique Visitors"])
    for date, visitors in zip(forecast_dates, forecast):
        writer.writerow([date.strftime("%Y-%m-%d"), visitors])

print(f"\n✅ Forecast saved to '{output_file}'")
