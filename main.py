import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# File paths
csv_path = "data/maintenance_log.csv"
plot_folder = "plots"

# Ensure plot directory exists
os.makedirs(plot_folder, exist_ok=True)

# Load the maintenance data
df = pd.read_csv(csv_path)
df["Date"] = pd.to_datetime(df["Date"])

# Summary Output
total_cost = df["Cost"].sum()
service_count = df.shape[0]
vehicle_counts = df["Vehicle"].value_counts()

print(f"Total spent: ${total_cost:.2f}")
print(f"Total number of services: {service_count}")
print("\nService count by vehicle:")
print(vehicle_counts)

# Plot 1: Cumulative cost over time
df_sorted = df.sort_values("Date")
df_sorted["Cumulative Cost"] = df_sorted["Cost"].cumsum()
plt.figure()
plt.plot(df_sorted["Date"], df_sorted["Cumulative Cost"], marker="o")
plt.title("Total Maintenance Cost Over Time")
plt.xlabel("Date")
plt.ylabel("Cumulative Cost ($)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{plot_folder}/cost_over_time.png")

# Plot 2: Cost by Service Type (Pie)
plt.figure()
df_costs = df.groupby("Service")["Cost"].sum()
df_costs = df_costs[df_costs > 0]  # Remove 0-cost services
df_costs.plot.pie(autopct="%1.1f%%", startangle=140)
plt.title("Cost Distribution by Service Type")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{plot_folder}/cost_by_service.png")

# Plot 3: Frequency of Each Service
plt.figure()
service_counts = df["Service"].value_counts()
sns.barplot(x=service_counts.index, y=service_counts.values)
plt.title("Service Frequency")
plt.xlabel("Service Type")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{plot_folder}/service_frequency.png")
