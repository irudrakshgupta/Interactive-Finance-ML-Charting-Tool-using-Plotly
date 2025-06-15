"""
Base chart implementations for FinancePlotter
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional, List, Union, Dict, Any

class Chart:
    """Base class for all chart types"""
    
    def __init__(self, data: pd.DataFrame, title: str = None):
        self.data = data
        self.title = title
        self.fig = None
        
    def add_range_slider(self) -> 'Chart':
        """Add a range slider to the chart"""
        if self.fig:
            self.fig.update_xaxes(rangeslider_visible=True)
        return self
    
    def add_zoom_pan(self) -> 'Chart':
        """Enable zoom and pan functionality"""
        if self.fig:
            self.fig.update_layout(
                dragmode='zoom',
                modebar_add=['zoom', 'pan', 'zoomIn', 'zoomOut', 'resetScale']
            )
        return self
    
    def add_tooltips(self) -> 'Chart':
        """Add interactive tooltips"""
        if self.fig:
            self.fig.update_traces(hovertemplate='%{x}<br>%{y:.2f}<extra></extra>')
        return self
    
    def show(self) -> None:
        """Display the chart"""
        if self.fig:
            self.fig.show()
    
    def write_html(self, filename: str) -> None:
        """Save the chart as an interactive HTML file"""
        if self.fig:
            self.fig.write_html(filename)

def create_candlestick(
    data: pd.DataFrame,
    title: str = None,
    volume: bool = True,
    indicators: List[str] = None
) -> Chart:
    """
    Create an interactive candlestick chart
    
    Args:
        data: DataFrame with OHLCV data
        title: Chart title
        volume: Whether to show volume bars
        indicators: List of technical indicators to add
    
    Returns:
        Chart object
    """
    # Create subplots if volume is enabled
    rows = 2 if volume else 1
    fig = make_subplots(
        rows=rows,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3] if volume else [1]
    )
    
    # Add candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='OHLC'
        ),
        row=1, col=1
    )
    
    # Add volume if requested
    if volume and 'Volume' in data.columns:
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume'
            ),
            row=2, col=1
        )
    
    # Update layout
    fig.update_layout(
        title=title,
        yaxis_title='Price',
        yaxis2_title='Volume' if volume else None,
        xaxis_rangeslider_visible=False
    )
    
    chart = Chart(data, title)
    chart.fig = fig
    return chart

def create_line(
    data: pd.DataFrame,
    title: str = None,
    x: str = None,
    y: str = None
) -> Chart:
    """
    Create an interactive line chart
    
    Args:
        data: DataFrame with data to plot
        title: Chart title
        x: Column name for x-axis
        y: Column name for y-axis
    
    Returns:
        Chart object
    """
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=data[x] if x else data.index,
            y=data[y] if y else data.iloc[:, 0],
            mode='lines',
            name=y if y else data.columns[0]
        )
    )
    
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y
    )
    
    chart = Chart(data, title)
    chart.fig = fig
    return chart

def create_bar(
    data: pd.DataFrame,
    title: str = None,
    x: str = None,
    y: str = None
) -> Chart:
    """
    Create an interactive bar chart
    
    Args:
        data: DataFrame with data to plot
        title: Chart title
        x: Column name for x-axis
        y: Column name for y-axis
    
    Returns:
        Chart object
    """
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=data[x] if x else data.index,
            y=data[y] if y else data.iloc[:, 0],
            name=y if y else data.columns[0]
        )
    )
    
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y
    )
    
    chart = Chart(data, title)
    chart.fig = fig
    return chart

def create_area(
    data: pd.DataFrame,
    title: str = None,
    x: str = None,
    y: str = None
) -> Chart:
    """
    Create an interactive area chart
    
    Args:
        data: DataFrame with data to plot
        title: Chart title
        x: Column name for x-axis
        y: Column name for y-axis
    
    Returns:
        Chart object
    """
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=data[x] if x else data.index,
            y=data[y] if y else data.iloc[:, 0],
            fill='tozeroy',
            name=y if y else data.columns[0]
        )
    )
    
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y
    )
    
    chart = Chart(data, title)
    chart.fig = fig
    return chart

def create_scatter(
    data: pd.DataFrame,
    title: str = None,
    x: str = None,
    y: str = None,
    color: str = None
) -> Chart:
    """
    Create an interactive scatter plot
    
    Args:
        data: DataFrame with data to plot
        title: Chart title
        x: Column name for x-axis
        y: Column name for y-axis
        color: Column name for color coding
    
    Returns:
        Chart object
    """
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=data[x] if x else data.index,
            y=data[y] if y else data.iloc[:, 0],
            mode='markers',
            marker=dict(
                color=data[color] if color else None,
                colorscale='Viridis',
                showscale=True if color else False
            ),
            name=y if y else data.columns[0]
        )
    )
    
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y
    )
    
    chart = Chart(data, title)
    chart.fig = fig
    return chart 