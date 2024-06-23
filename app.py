import dash
import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the CSV files
aapl_df = pd.read_csv('datasets/AAPL.csv')
amzn_df = pd.read_csv('datasets/AMZN.csv')
googl_df = pd.read_csv('datasets/GOOGL.csv')
msft_df = pd.read_csv('datasets/MSFT.csv')
meta_df = pd.read_csv('datasets/META.csv')

# Convert the 'Date' column to datetime
aapl_df['Date'] = pd.to_datetime(aapl_df['Date'])
amzn_df['Date'] = pd.to_datetime(amzn_df['Date'])
googl_df['Date'] = pd.to_datetime(googl_df['Date'])
msft_df['Date'] = pd.to_datetime(msft_df['Date'])
meta_df['Date'] = pd.to_datetime(meta_df['Date'])

# Sort the DataFrames by date
aapl_df.sort_values('Date', inplace=True)
amzn_df.sort_values('Date', inplace=True)
googl_df.sort_values('Date', inplace=True)
msft_df.sort_values('Date', inplace=True)
meta_df.sort_values('Date', inplace=True)

# Calculate daily returns
aapl_df['Daily Return'] = aapl_df['Adj Close'].pct_change()
amzn_df['Daily Return'] = amzn_df['Adj Close'].pct_change()
googl_df['Daily Return'] = googl_df['Adj Close'].pct_change()
msft_df['Daily Return'] = msft_df['Adj Close'].pct_change()
meta_df['Daily Return'] = meta_df['Adj Close'].pct_change()


# Calculate volatility (rolling standard deviation)
aapl_df['Volatility'] = aapl_df['Daily Return'].rolling(window=21).std()
amzn_df['Volatility'] = amzn_df['Daily Return'].rolling(window=21).std()
googl_df['Volatility'] = googl_df['Daily Return'].rolling(window=21).std()
msft_df['Volatility'] = msft_df['Daily Return'].rolling(window=21).std()
meta_df['Volatility'] = meta_df['Daily Return'].rolling(window=21).std()


# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define the layout of the app
app.layout = html.Div([

    html.H1("Volatility of principal NASDAQ stocks"),
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

    # Add AMZN volatility trace
    fig.add_trace(
        go.Scatter(x=amzn_df['Date'], y=amzn_df['Volatility'], mode='lines', name='AMZN Volatility')
    )

    # Add GOOGL volatility trace
    fig.add_trace(
        go.Scatter(x=googl_df['Date'], y=googl_df['Volatility'], mode='lines', name='GOOGL Volatility')
    )

    # Add MSFT volatility trace
    fig.add_trace(
        go.Scatter(x=msft_df['Date'], y=msft_df['Volatility'], mode='lines', name='MSFT Volatility')
    )

    # Add META volatility trace
    fig.add_trace(
        go.Scatter(x=meta_df['Date'], y=meta_df['Volatility'], mode='lines', name='META Volatility')
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
    app.run_server(debug=False)
