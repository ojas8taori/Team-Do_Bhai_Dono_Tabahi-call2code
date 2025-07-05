import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st

def create_candlestick_chart(data, symbol, timeframe):
    """
    Create interactive candlestick chart
    
    Args:
        data (pd.DataFrame): Stock data with OHLCV
        symbol (str): Stock symbol
        timeframe (str): Chart timeframe
    
    Returns:
        plotly.graph_objects.Figure: Candlestick chart
    """
    try:
        if data is None or data.empty:
            return create_empty_chart("No data available")
        
        # Create subplots with secondary y-axis
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=(f'{symbol} - {timeframe}', 'Volume'),
            row_width=[0.7, 0.3]
        )
        
        # Add candlestick chart with better colors
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name=symbol,
                increasing_line_color='#00C851',  # Bright green
                decreasing_line_color='#FF4444',  # Bright red
                increasing_fillcolor='rgba(0, 200, 81, 0.8)',
                decreasing_fillcolor='rgba(255, 68, 68, 0.8)'
            ),
            row=1, col=1
        )
        
        # Add volume bars with enhanced colors
        colors = ['#00C851' if close >= open else '#FF4444' 
                 for close, open in zip(data['Close'], data['Open'])]
        
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.8,
                marker_line_color='rgba(0,0,0,0.1)',
                marker_line_width=0.5
            ),
            row=2, col=1
        )
        
        # Add moving averages with vibrant colors
        if len(data) >= 20:
            data['MA20'] = data['Close'].rolling(window=20).mean()
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['MA20'],
                    name='MA20',
                    line=dict(color='#FF9800', width=2),  # Orange
                    opacity=0.9
                ),
                row=1, col=1
            )
        
        if len(data) >= 50:
            data['MA50'] = data['Close'].rolling(window=50).mean()
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['MA50'],
                    name='MA50',
                    line=dict(color='#2196F3', width=2),  # Blue
                    opacity=0.9
                ),
                row=1, col=1
            )
        
        # Update layout with enhanced styling
        fig.update_layout(
            title=dict(
                text=f'{symbol} Stock Price - {timeframe}',
                font=dict(size=20, color='#1f2937'),
                x=0.5
            ),
            yaxis_title='Price',
            xaxis_title='Date',
            template='plotly_white',
            height=600,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1
            ),
            plot_bgcolor='rgba(248,250,252,0.8)',
            paper_bgcolor='white',
            font=dict(color='#374151')
        )
        
        # Update x-axis
        fig.update_xaxes(
            rangeslider_visible=False,
            type='date'
        )
        
        # Update y-axis for volume
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return create_empty_chart("Error creating chart")

def create_price_chart(data, symbol, chart_type='line'):
    """
    Create price chart (line or area)
    
    Args:
        data (pd.DataFrame): Stock data
        symbol (str): Stock symbol
        chart_type (str): 'line' or 'area'
    
    Returns:
        plotly.graph_objects.Figure: Price chart
    """
    try:
        if data is None or data.empty:
            return create_empty_chart("No data available")
        
        fig = go.Figure()
        
        if chart_type == 'area':
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['Close'],
                    name=symbol,
                    fill='tonexty',
                    line=dict(color='#1f77b4', width=2)
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['Close'],
                    name=symbol,
                    line=dict(color='#1f77b4', width=2)
                )
            )
        
        fig.update_layout(
            title=f'{symbol} Price Chart',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            template='plotly_white',
            height=400
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating price chart: {str(e)}")
        return create_empty_chart("Error creating chart")

def create_volume_chart(data, symbol):
    """
    Create volume chart
    
    Args:
        data (pd.DataFrame): Stock data
        symbol (str): Stock symbol
    
    Returns:
        plotly.graph_objects.Figure: Volume chart
    """
    try:
        if data is None or data.empty:
            return create_empty_chart("No data available")
        
        # Color bars based on price movement
        colors = ['green' if close >= open else 'red' 
                 for close, open in zip(data['Close'], data['Open'])]
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.7
            )
        )
        
        fig.update_layout(
            title=f'{symbol} Volume',
            xaxis_title='Date',
            yaxis_title='Volume',
            template='plotly_white',
            height=300
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating volume chart: {str(e)}")
        return create_empty_chart("Error creating chart")

def create_performance_chart(data, symbol):
    """
    Create performance comparison chart
    
    Args:
        data (pd.DataFrame): Stock data
        symbol (str): Stock symbol
    
    Returns:
        plotly.graph_objects.Figure: Performance chart
    """
    try:
        if data is None or data.empty:
            return create_empty_chart("No data available")
        
        # Calculate performance relative to first price
        performance = ((data['Close'] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=performance,
                name=f'{symbol} Performance',
                line=dict(color='#1f77b4', width=2),
                fill='tonexty'
            )
        )
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig.update_layout(
            title=f'{symbol} Performance (%)',
            xaxis_title='Date',
            yaxis_title='Performance (%)',
            template='plotly_white',
            height=400
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating performance chart: {str(e)}")
        return create_empty_chart("Error creating chart")

def create_technical_indicators_chart(data, symbol):
    """
    Create comprehensive chart with technical indicators
    
    Args:
        data (pd.DataFrame): Stock data
        symbol (str): Stock symbol
    
    Returns:
        plotly.graph_objects.Figure: Technical indicators chart
    """
    try:
        if data is None or data.empty:
            return create_empty_chart("No data available")
        
        # Calculate technical indicators
        data = calculate_technical_indicators(data)
        
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=(
                f'{symbol} with Bollinger Bands & Moving Averages', 
                'RSI (Relative Strength Index)', 
                'MACD (Moving Average Convergence Divergence)',
                'Volume with Price Overlay'
            ),
            row_heights=[0.4, 0.2, 0.2, 0.2]
        )
        
        # 1. Price Chart with Bollinger Bands and Moving Averages
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Close'],
                name='Close Price',
                line=dict(color='#2E86AB', width=2)
            ),
            row=1, col=1
        )
        
        # Moving Averages
        if 'MA20' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['MA20'],
                    name='MA20',
                    line=dict(color='#F18F01', width=2),
                    opacity=0.8
                ),
                row=1, col=1
            )
        
        if 'MA50' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['MA50'],
                    name='MA50',
                    line=dict(color='#C73E1D', width=2),
                    opacity=0.8
                ),
                row=1, col=1
            )
        
        # Bollinger Bands
        if 'BB_Upper' in data.columns and 'BB_Lower' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['BB_Upper'],
                    name='Upper BB',
                    line=dict(color='#9D4EDD', width=1, dash='dash'),
                    opacity=0.7
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['BB_Lower'],
                    name='Lower BB',
                    line=dict(color='#9D4EDD', width=1, dash='dash'),
                    fill='tonexty',
                    fillcolor='rgba(157, 78, 221, 0.1)',
                    opacity=0.7
                ),
                row=1, col=1
            )
        
        # 2. RSI
        if 'RSI' in data.columns:
            # Color RSI line based on overbought/oversold levels
            rsi_colors = []
            for rsi_val in data['RSI']:
                if pd.isna(rsi_val):
                    rsi_colors.append('#FFA726')
                elif rsi_val >= 70:
                    rsi_colors.append('#FF5252')  # Red for overbought
                elif rsi_val <= 30:
                    rsi_colors.append('#4CAF50')  # Green for oversold
                else:
                    rsi_colors.append('#FFA726')  # Orange for neutral
            
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['RSI'],
                    name='RSI',
                    line=dict(color='#FFA726', width=2),
                    mode='lines'
                ),
                row=2, col=1
            )
            
            # Add overbought/oversold zones
            fig.add_hrect(y0=70, y1=100, fillcolor="rgba(255, 82, 82, 0.2)", 
                         line_width=0, row=2, col=1)
            fig.add_hrect(y0=0, y1=30, fillcolor="rgba(76, 175, 80, 0.2)", 
                         line_width=0, row=2, col=1)
            
            # RSI reference lines
            fig.add_hline(y=70, line_dash="dash", line_color="#FF5252", 
                         opacity=0.8, line_width=1, row=2, col=1)
            fig.add_hline(y=50, line_dash="dot", line_color="#757575", 
                         opacity=0.5, line_width=1, row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="#4CAF50", 
                         opacity=0.8, line_width=1, row=2, col=1)
        
        # 3. MACD
        if 'MACD' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['MACD'],
                    name='MACD',
                    line=dict(color='#1976D2', width=2)
                ),
                row=3, col=1
            )
            
            if 'MACD_Signal' in data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=data['MACD_Signal'],
                        name='Signal Line',
                        line=dict(color='#D32F2F', width=2)
                    ),
                    row=3, col=1
                )
            
            if 'MACD_Histogram' in data.columns:
                # Color histogram bars
                colors = ['#4CAF50' if val >= 0 else '#FF5252' for val in data['MACD_Histogram']]
                fig.add_trace(
                    go.Bar(
                        x=data.index,
                        y=data['MACD_Histogram'],
                        name='MACD Histogram',
                        marker_color=colors,
                        opacity=0.6
                    ),
                    row=3, col=1
                )
            
            # Zero line
            fig.add_hline(y=0, line_dash="solid", line_color="#757575", 
                         opacity=0.5, line_width=1, row=3, col=1)
        
        # 4. Volume
        volume_colors = ['#4CAF50' if close >= open else '#FF5252' 
                        for close, open in zip(data['Close'], data['Open'])]
        
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker_color=volume_colors,
                opacity=0.7,
                yaxis='y4'
            ),
            row=4, col=1
        )
        
        # Update layout with enhanced styling
        fig.update_layout(
            title=dict(
                text=f'{symbol} - Comprehensive Technical Analysis',
                font=dict(size=18, color='#1f2937'),
                x=0.5
            ),
            template='plotly_white',
            height=900,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor='rgba(248,250,252,0.8)',
            paper_bgcolor='white'
        )
        
        # Update y-axis labels
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="RSI", row=2, col=1, range=[0, 100])
        fig.update_yaxes(title_text="MACD", row=3, col=1)
        fig.update_yaxes(title_text="Volume", row=4, col=1)
        fig.update_xaxes(title_text="Date", row=4, col=1)
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating technical indicators chart: {str(e)}")
        return create_empty_chart("Error creating chart")

def calculate_technical_indicators(data):
    """
    Calculate technical indicators
    
    Args:
        data (pd.DataFrame): Stock data
    
    Returns:
        pd.DataFrame: Data with technical indicators
    """
    try:
        df = data.copy()
        
        # Moving averages
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        ema12 = df['Close'].ewm(span=12).mean()
        ema26 = df['Close'].ewm(span=26).mean()
        df['MACD'] = ema12 - ema26
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        return df
        
    except Exception as e:
        st.error(f"Error calculating technical indicators: {str(e)}")
        return data

def create_empty_chart(message):
    """
    Create empty chart with message
    
    Args:
        message (str): Message to display
    
    Returns:
        plotly.graph_objects.Figure: Empty chart
    """
    fig = go.Figure()
    
    fig.add_annotation(
        x=0.5,
        y=0.5,
        text=message,
        showarrow=False,
        font=dict(size=16),
        xref="paper",
        yref="paper"
    )
    
    fig.update_layout(
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    return fig

def create_comparison_chart(data_dict, symbols):
    """
    Create comparison chart for multiple stocks
    
    Args:
        data_dict (dict): Dictionary with stock data
        symbols (list): List of stock symbols
    
    Returns:
        plotly.graph_objects.Figure: Comparison chart
    """
    try:
        fig = go.Figure()
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        for i, symbol in enumerate(symbols):
            if symbol in data_dict and data_dict[symbol] is not None:
                data = data_dict[symbol]
                
                # Normalize to percentage change from first price
                performance = ((data['Close'] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
                
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=performance,
                        name=symbol,
                        line=dict(color=colors[i % len(colors)], width=2)
                    )
                )
        
        fig.update_layout(
            title='Stock Performance Comparison',
            xaxis_title='Date',
            yaxis_title='Performance (%)',
            template='plotly_white',
            height=500,
            showlegend=True
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating comparison chart: {str(e)}")
        return create_empty_chart("Error creating comparison chart")
