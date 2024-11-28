import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from src.process_data import load_data
from datetime import datetime
import json

def main():
    file_path = 'data/brokerage_data.csv'
    data = load_data(file_path)
    
    if not data:
        print("No data available to plot.")
        return
    
    # Extract dates, account values, deposits, and withdrawals for plotting
    dates = [datetime.strptime(entry['Date'], "%Y-%m-%d") for entry in data]
    account_values = [float(entry['Account_Value']) for entry in data]
    deposits = [float(entry['Deposit']) for entry in data]
    withdrawals = [-float(entry['Withdrawal']) for entry in data]  # Negative for plotting below zero

    # Create a figure with subplots
    fig = make_subplots(rows=2, cols=1, 
                        shared_xaxes=True, 
                        vertical_spacing=0.1,
                        subplot_titles=('Account Value Over Time', 'Deposits and Withdrawals Over Time'))

    # Add account values to the first subplot
    fig.add_trace(
        go.Scatter(
            x=dates, 
            y=account_values, 
            mode='lines+markers',
            name='Account Value',
            marker=dict(color='blue'),
            hovertemplate='<b>%{x| %b %d, %Y}</b><br>' + 
                          'Account Value: %{y:.2f} PLN<extra></extra>'
        ),
        row=1, col=1
    )

    # Add a trendline for account values
    z = np.polyfit(range(len(dates)), account_values, 1)
    p = np.poly1d(z)
    trendline = p(range(len(dates)))
    fig.add_trace(
        go.Scatter(
            x=dates, 
            y=trendline, 
            mode='lines',
            name='Trendline',
            line=dict(dash='dash', color='red'),
            hoverinfo='skip'
        ),
        row=1, col=1
    )

    # Add deposits as green bars in the second subplot
    fig.add_trace(
        go.Bar(
            x=dates, 
            y=deposits,
            name='Deposits',
            marker_color='green',
            hovertemplate='<b>%{x| %b %d, %Y}</b><br>' + 
                          'Deposit: %{y:.2f} PLN<extra></extra>'
        ),
        row=2, col=1
    )

    # Add withdrawals as red bars in the second subplot
    fig.add_trace(
        go.Bar(
            x=dates, 
            y=withdrawals,
            name='Withdrawals',
            marker_color='red',
            hovertemplate='<b>%{x| %b %d, %Y}</b><br>' + 
                          'Withdrawal: %{y:.2f} PLN<extra></extra>'
        ),
        row=2, col=1
    )

    # Customize the layout
    fig.update_layout(
        height=800,  # Adjust as necessary
        title_text="Financial Overview",
        showlegend=True,
        barmode='relative',  # Stacks deposits and withdrawals
        xaxis1=dict(title='Date', automargin=True),
        yaxis1=dict(title='Account Value (PLN)', automargin=True),
        xaxis2=dict(title='Date', automargin=True),
        yaxis2=dict(title='Deposits / Withdrawals (PLN)', automargin=True),
    )

    # Show the plot
    fig.show()

    # Pretty print the data structure
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()