# main.py
import matplotlib.pyplot as plt
import numpy as np
from src.process_data import load_data
from datetime import datetime
import json

def main():
    file_path = 'data/brokerage_data.csv'  # or whatever your path is
    data = load_data(file_path)
    
    if not data:
        print("No data available to plot.")
        return
    
    # Extract dates and account values for plotting
    dates = [datetime.strptime(entry['Date'], "%Y-%m-%d") for entry in data]
    account_values = [float(entry['Account_Value']) for entry in data]
    
    # Create a figure and axis object
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Plot the data
    ax.plot(dates, account_values, marker='o')
    
    # Customize the plot
    ax.set_title('Account Value Over Time', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Account Value (PLN)', fontsize=12)
    ax.grid(True)
    
    # Format x-axis to show dates nicely
    fig.autofmt_xdate()
    
    # Add a trendline
    z = np.polyfit(range(len(dates)), account_values, 1)
    p = np.poly1d(z)
    ax.plot(dates, p(range(len(dates))), "r--", label="Trendline")
    
    # Show legend for trendline
    ax.legend()
    
    # Display the plot
    plt.tight_layout()
    plt.show()

    print(json.dumps(data, indent=2))  # Pretty print the data structure

if __name__ == "__main__":
    main()