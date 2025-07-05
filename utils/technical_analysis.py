import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from typing import Dict, List, Tuple

class TechnicalAnalyzer:
    def __init__(self):
        pass
    
    def calculate_sma(self, data: pd.Series, window: int) -> pd.Series:
        """Calculate Simple Moving Average"""
        return data.rolling(window=window).mean()
    
    def calculate_ema(self, data: pd.Series, window: int) -> pd.Series:
        """Calculate Exponential Moving Average"""
        return data.ewm(span=window).mean()
    
    def calculate_rsi(self, data: pd.Series, window: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        exp1 = data.ewm(span=fast).mean()
        exp2 = data.ewm(span=slow).mean()
        macd = exp1 - exp2
        macd_signal = macd.ewm(span=signal).mean()
        macd_histogram = macd - macd_signal
        
        return {
            'macd': macd,
            'signal': macd_signal,
            'histogram': macd_histogram
        }
    
    def calculate_bollinger_bands(self, data: pd.Series, window: int = 20, num_std: float = 2) -> Dict:
        """Calculate Bollinger Bands"""
        sma = data.rolling(window=window).mean()
        std = data.rolling(window=window).std()
        
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        
        return {
            'upper': upper_band,
            'middle': sma,
            'lower': lower_band
        }
    
    def calculate_stochastic(self, high: pd.Series, low: pd.Series, close: pd.Series, k_window: int = 14, d_window: int = 3) -> Dict:
        """Calculate Stochastic Oscillator"""
        lowest_low = low.rolling(window=k_window).min()
        highest_high = high.rolling(window=k_window).max()
        
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_window).mean()
        
        return {
            'k': k_percent,
            'd': d_percent
        }
    
    def calculate_volume_sma(self, volume: pd.Series, window: int = 20) -> pd.Series:
        """Calculate Volume Simple Moving Average"""
        return volume.rolling(window=window).mean()
    
    def identify_support_resistance(self, data: pd.Series, window: int = 20) -> Dict:
        """Identify support and resistance levels"""
        highs = data.rolling(window=window, center=True).max()
        lows = data.rolling(window=window, center=True).min()
        
        resistance_levels = data[data == highs].dropna()
        support_levels = data[data == lows].dropna()
        
        return {
            'resistance': resistance_levels.tail(5).tolist(),
            'support': support_levels.tail(5).tolist()
        }
    
    def generate_signals(self, stock_data: pd.DataFrame) -> Dict:
        """Generate buy/sell signals based on technical indicators"""
        signals = {}
        
        # Calculate indicators
        stock_data['SMA_20'] = self.calculate_sma(stock_data['Close'], 20)
        stock_data['SMA_50'] = self.calculate_sma(stock_data['Close'], 50)
        stock_data['RSI'] = self.calculate_rsi(stock_data['Close'])
        
        macd_data = self.calculate_macd(stock_data['Close'])
        stock_data['MACD'] = macd_data['macd']
        stock_data['MACD_Signal'] = macd_data['signal']
        
        # Moving Average Crossover Signal
        ma_signal = np.where(stock_data['SMA_20'] > stock_data['SMA_50'], 1, -1)
        signals['ma_crossover'] = ma_signal[-1] if len(ma_signal) > 0 else 0
        
        # RSI Signal
        current_rsi = stock_data['RSI'].iloc[-1] if not stock_data['RSI'].empty else 50
        if current_rsi > 70:
            signals['rsi'] = -1  # Overbought - Sell signal
        elif current_rsi < 30:
            signals['rsi'] = 1   # Oversold - Buy signal
        else:
            signals['rsi'] = 0   # Neutral
        
        # MACD Signal
        if len(stock_data) >= 2:
            current_macd = stock_data['MACD'].iloc[-1]
            current_signal = stock_data['MACD_Signal'].iloc[-1]
            prev_macd = stock_data['MACD'].iloc[-2]
            prev_signal = stock_data['MACD_Signal'].iloc[-2]
            
            if prev_macd <= prev_signal and current_macd > current_signal:
                signals['macd'] = 1  # Bullish crossover
            elif prev_macd >= prev_signal and current_macd < current_signal:
                signals['macd'] = -1  # Bearish crossover
            else:
                signals['macd'] = 0  # No signal
        else:
            signals['macd'] = 0
        
        return signals
    
    def create_technical_chart(self, stock_data: pd.DataFrame, symbol: str) -> go.Figure:
        """Create comprehensive technical analysis chart"""
        # Calculate technical indicators
        stock_data = stock_data.copy()
        stock_data['SMA_20'] = self.calculate_sma(stock_data['Close'], 20)
        stock_data['SMA_50'] = self.calculate_sma(stock_data['Close'], 50)
        stock_data['EMA_12'] = self.calculate_ema(stock_data['Close'], 12)
        
        bollinger = self.calculate_bollinger_bands(stock_data['Close'])
        stock_data['BB_Upper'] = bollinger['upper']
        stock_data['BB_Lower'] = bollinger['lower']
        stock_data['BB_Middle'] = bollinger['middle']
        
        stock_data['RSI'] = self.calculate_rsi(stock_data['Close'])
        macd_data = self.calculate_macd(stock_data['Close'])
        stock_data['MACD'] = macd_data['macd']
        stock_data['MACD_Signal'] = macd_data['signal']
        stock_data['MACD_Histogram'] = macd_data['histogram']
        
        # Create subplots
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(f'{symbol} - Price & Volume', 'RSI', 'MACD', 'Volume'),
            row_heights=[0.5, 0.2, 0.2, 0.1]
        )
        
        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=stock_data.index,
                open=stock_data['Open'],
                high=stock_data['High'],
                low=stock_data['Low'],
                close=stock_data['Close'],
                name='Price',
                increasing_line_color='#00ff00',
                decreasing_line_color='#ff0000'
            ),
            row=1, col=1
        )
        
        # Moving Averages
        fig.add_trace(
            go.Scatter(
                x=stock_data.index,
                y=stock_data['SMA_20'],
                mode='lines',
                name='SMA 20',
                line=dict(color='orange', width=1)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=stock_data.index,
                y=stock_data['SMA_50'],
                mode='lines',
                name='SMA 50',
                line=dict(color='blue', width=1)
            ),
            row=1, col=1
        )
        
        # Bollinger Bands
        fig.add_trace(
            go.Scatter(
                x=stock_data.index,
                y=stock_data['BB_Upper'],
                mode='lines',
                name='BB Upper',
                line=dict(color='gray', width=1, dash='dash'),
                showlegend=False
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=stock_data.index,
                y=stock_data['BB_Lower'],
                mode='lines',
                name='BB Lower',
                line=dict(color='gray', width=1, dash='dash'),
                fill='tonexty',
                fillcolor='rgba(128,128,128,0.1)',
                showlegend=False
            ),
            row=1, col=1
        )
        
        # RSI
        fig.add_trace(
            go.Scatter(
                x=stock_data.index,
                y=stock_data['RSI'],
                mode='lines',
                name='RSI',
                line=dict(color='purple', width=2)
            ),
            row=2, col=1
        )
        
        # RSI overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        fig.add_hline(y=50, line_dash="dot", line_color="gray", row=2, col=1)
        
        # MACD
        fig.add_trace(
            go.Scatter(
                x=stock_data.index,
                y=stock_data['MACD'],
                mode='lines',
                name='MACD',
                line=dict(color='blue', width=2)
            ),
            row=3, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=stock_data.index,
                y=stock_data['MACD_Signal'],
                mode='lines',
                name='Signal',
                line=dict(color='red', width=2)
            ),
            row=3, col=1
        )
        
        # MACD Histogram
        colors = ['green' if x >= 0 else 'red' for x in stock_data['MACD_Histogram']]
        fig.add_trace(
            go.Bar(
                x=stock_data.index,
                y=stock_data['MACD_Histogram'],
                name='MACD Histogram',
                marker_color=colors,
                opacity=0.7
            ),
            row=3, col=1
        )
        
        # Volume
        volume_colors = ['green' if stock_data['Close'].iloc[i] >= stock_data['Open'].iloc[i] 
                        else 'red' for i in range(len(stock_data))]
        
        fig.add_trace(
            go.Bar(
                x=stock_data.index,
                y=stock_data['Volume'],
                name='Volume',
                marker_color=volume_colors,
                opacity=0.7
            ),
            row=4, col=1
        )
        
        # Update layout
        fig.update_layout(
            title=f'Technical Analysis - {symbol}',
            xaxis_title='Date',
            height=800,
            showlegend=True,
            template='plotly_white'
        )
        
        # Update y-axes
        fig.update_yaxes(title_text="Price (₹)", row=1, col=1)
        fig.update_yaxes(title_text="RSI", row=2, col=1, range=[0, 100])
        fig.update_yaxes(title_text="MACD", row=3, col=1)
        fig.update_yaxes(title_text="Volume", row=4, col=1)
        
        return fig
    
    def get_technical_summary(self, stock_data: pd.DataFrame) -> Dict:
        """Generate technical analysis summary"""
        signals = self.generate_signals(stock_data)
        
        # Calculate current indicator values
        current_rsi = self.calculate_rsi(stock_data['Close']).iloc[-1] if len(stock_data) > 14 else 50
        macd_data = self.calculate_macd(stock_data['Close'])
        current_macd = macd_data['macd'].iloc[-1] if len(macd_data['macd']) > 0 else 0
        current_signal = macd_data['signal'].iloc[-1] if len(macd_data['signal']) > 0 else 0
        
        # Support and resistance
        support_resistance = self.identify_support_resistance(stock_data['Close'])
        
        # Overall signal
        signal_sum = sum(signals.values())
        if signal_sum > 0:
            overall_signal = "BUY"
            signal_strength = min(signal_sum / 3 * 100, 100)
        elif signal_sum < 0:
            overall_signal = "SELL"
            signal_strength = min(abs(signal_sum) / 3 * 100, 100)
        else:
            overall_signal = "HOLD"
            signal_strength = 0
        
        return {
            'overall_signal': overall_signal,
            'signal_strength': signal_strength,
            'rsi': current_rsi,
            'macd': current_macd,
            'macd_signal': current_signal,
            'support_levels': support_resistance['support'],
            'resistance_levels': support_resistance['resistance'],
            'individual_signals': signals
        }
