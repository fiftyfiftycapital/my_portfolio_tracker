import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from src.process_data import load_data
from datetime import datetime
import src.mail_downloader as mail_downloader
import src.process_pdf_statement as process_pdf_statement
import json

def main():
    file_path = 'data/brokerage_data1.csv'
    data = load_data(file_path)
    
    if not data:
        print("No data available to plot.")
        return
    
    # Extract dates, account values, deposits, withdrawals, realized and unrealized gains, and overnight fees
    dates = [datetime.strptime(entry['Date'], "%Y-%m-%d") for entry in data]
    account_values = [float(entry['Account_Value'].replace(',', '.')) for entry in data]
    deposits = [float(entry['Deposit'].replace(',', '.')) for entry in data]
    withdrawals = [float(entry['Withdrawal'].replace(',', '.')) for entry in data]
    realized_pl = [float(entry['Realized_P/L'].replace(',', '.')) for entry in data]
    unrealized_pl = [float(entry['Unrealized_P/L'].replace(',', '.')) for entry in data]
    overnight_fees = [float(entry['Overnight_Fee'].replace(',', '.')) for entry in data]

    # Calculate net account value
    net_account_values = []
    cumulative_adjustment = 0
    for value, deposit, withdrawal in zip(account_values, deposits, withdrawals):
        cumulative_adjustment += deposit - abs(withdrawal)
        net_account_values.append(value - cumulative_adjustment)

    # Calculate realized and unrealized gains as percentages of 8000 PLN
    initial_investment = 8000  # PLN
    realized_gains_percent = [(pl / initial_investment) * 100 for pl in realized_pl]
    unrealized_gains_percent = [(pl / initial_investment) * 100 for pl in unrealized_pl]

    # Calculate position size from overnight fees and interest rate
    overnight_interest_rate = 0.000165  # 0.0165% in decimal
    position_sizes = [fee / overnight_interest_rate for fee in overnight_fees]

    # Create a figure with subplots
    fig = make_subplots(rows=7, cols=1,  # Changed to 7 rows for the new chart
                        shared_xaxes=True, 
                        vertical_spacing=0.1,
                        subplot_titles=('Account Value Over Time', 
                                        'Deposits and Withdrawals Over Time', 
                                        'Net Account Value Over Time', 
                                        'Realized Gains as % of 8000 PLN',
                                        'Unrealized Gains as % of 8000 PLN',
                                        'Overnight Fees Over Time',
                                        'Position Size Over Time'))  # Added new subplot title

    # Account Value
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

    # Trendline for Account Value
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

    # Deposits and Withdrawals
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

    fig.add_trace(
        go.Bar(
            x=dates, 
            y=[-w for w in withdrawals],  # Negative withdrawals for plotting
            name='Withdrawals',
            marker_color='red',
            hovertemplate='<b>%{x| %b %d, %Y}</b><br>' + 
                          'Withdrawal: %{y:.2f} PLN<extra></extra>'
        ),
        row=2, col=1
    )

    # Net Account Value
    fig.add_trace(
        go.Scatter(
            x=dates, 
            y=net_account_values, 
            mode='lines+markers',
            name='Net Account Value',
            marker=dict(color='purple'),
            hovertemplate='<b>%{x| %b %d, %Y}</b><br>' + 
                          'Net Account Value: %{y:.2f} PLN<extra></extra>'
        ),
        row=3, col=1
    )

    # Realized Gains as % of 8000 PLN
    fig.add_trace(
        go.Bar(
            x=dates, 
            y=realized_gains_percent,
            name='Realized Gains (%)',
            marker=dict(color='orange'),
            hovertemplate='<b>%{x| %b %d, %Y}</b><br>' + 
                          'Realized Gains: %{y:.2f}%<extra></extra>'
        ),
        row=4, col=1
    )

    # Unrealized Gains as % of 8000 PLN
    fig.add_trace(
        go.Bar(
            x=dates, 
            y=unrealized_gains_percent,
            name='Unrealized Gains (%)',
            marker=dict(color='cyan'),
            hovertemplate='<b>%{x| %b %d, %Y}</b><br>' + 
                          'Unrealized Gains: %{y:.2f}%<extra></extra>'
        ),
        row=5, col=1
    )

    # Overnight Fees
    fig.add_trace(
        go.Bar(
            x=dates, 
            y=overnight_fees,
            name='Overnight Fees',
            marker=dict(color='brown'),
            hovertemplate='<b>%{x| %b %d, %Y}</b><br>' + 
                          'Overnight Fees: %{y:.2f} PLN<extra></extra>'
        ),
        row=6, col=1
    )

    # Position Size
    fig.add_trace(
        go.Scatter(
            x=dates, 
            y=position_sizes,
            mode='lines+markers',
            name='Position Size',
            marker=dict(color='magenta'),
            hovertemplate='<b>%{x| %b %d, %Y}</b><br>' + 
                          'Position Size: %{y:.2f} PLN<extra></extra>'
        ),
        row=7, col=1
    )

    # Customize the layout
    fig.update_layout(
        height=1800,  # Increased height to accommodate the new chart
        title_text="Comprehensive Financial Performance",
        showlegend=True,
        barmode='group',  # Changed to group for better visibility of percentage changes
        xaxis1=dict(title='Date', automargin=True),
        yaxis1=dict(title='Account Value (PLN)', automargin=True),
        xaxis2=dict(title='Date', automargin=True),
        yaxis2=dict(title='Deposits / Withdrawals (PLN)', automargin=True),
        xaxis3=dict(title='Date', automargin=True),
        yaxis3=dict(title='Net Account Value (PLN)', automargin=True),
        xaxis4=dict(title='Date', automargin=True),
        yaxis4=dict(title='Realized Gains (%)', automargin=True),
        xaxis5=dict(title='Date', automargin=True),
        yaxis5=dict(title='Unrealized Gains (%)', automargin=True),
        xaxis6=dict(title='Date', automargin=True),  # Added new x-axis
        yaxis6=dict(title='Overnight Fees (PLN)', automargin=True),  # Added new y-axis
        xaxis7=dict(title='Date', automargin=True),  # Added new x-axis
        yaxis7=dict(title='Position Size (PLN)', automargin=True),  # Added new y-axis
        legend=dict(x=0, y=1.2, orientation='h')
    )

    # Show the plot
    fig.show()
    fig.write_html("plot8000.html")

if __name__ == "__main__":
    mail_downloader.main()
    while True:
        try:
            result = process_pdf_statement.main()
            if result != 0:  # Exit on non-success (None, non-zero, or error)
                break
        except Exception as e:
            print(f"Error in process_data.main: {e}")
            break  # Exit on exception
    main()