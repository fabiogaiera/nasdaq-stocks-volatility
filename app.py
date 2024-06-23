import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load the CSV files
aapl_df = pd.read_csv('datasets/AAPL.csv')
msft_df = pd.read_csv('datasets/MSFT.csv')

# Convert the 'Date' column to datetime
aapl_df['Date'] = pd.to_datetime(aapl_df['Date'])
msft_df['Date'] = pd.to_datetime(msft_df['Date'])

# Sort the DataFrames by date
aapl_df.sort_values('Date', inplace=True)
msft_df.sort_values('Date', inplace=True)

# Calculate daily returns
aapl_df['Daily Return'] = aapl_df['Adj Close'].pct_change()
msft_df['Daily Return'] = msft_df['Adj Close'].pct_change()

# Calculate volatility (rolling standard deviation)
aapl_df['Volatility'] = aapl_df['Daily Return'].rolling(window=21).std()
msft_df['Volatility'] = msft_df['Daily Return'].rolling(window=21).std()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Volatility of AAPL and MSFT Stocks"),

    dcc.Graph(id='volatility-graph'),
])


# Define callback to update graph
@app.callback(
    Output('volatility-graph', 'figure'),
    Input('volatility-graph', 'hoverData')
)
def update_graph(hoverData):
    # Create a subplot
    fig = go.Figure()

    # Add AAPL volatility trace
    fig.add_trace(
        go.Scatter(x=aapl_df['Date'], y=aapl_df['Volatility'], mode='lines', name='AAPL Volatility')
    )

    # Add MSFT volatility trace
    fig.add_trace(
        go.Scatter(x=msft_df['Date'], y=msft_df['Volatility'], mode='lines', name='MSFT Volatility')
    )

    # Update layout
    fig.update_layout(
        title='January 2020 - December 2023',
        xaxis_title='Date',
        yaxis_title='Volatility',
        hovermode='x'  # Set hover mode to show data on hover
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
