import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime
from components.header import header_value
from components.solar_first_card import solar_first_card_value
from components.solar_second_card import solar_second_card_value
from components.solar_third_card import solar_third_card_value
from components.solar_fourth_card import solar_fourth_card_value
from components.solar_fifth_card import solar_fifth_card_value
from components.solar_current_power_chart import solar_current_power_chart_value
from components.solar_today_power_chart import solar_today_power_chart_value
from components.solar_yesterday_power_chart import solar_yesterday_power_chart_value
from components.current_weather import current_weather_value

font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
meta_tags = [{"name": "viewport", "content": "width=device-width"}]
external_stylesheets = [meta_tags, font_awesome]

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

tabs_styles = {
    "flex-direction": "row",
}
tab_style = {
    "padding": "0vh",
    "color": '#1a1a1a',
    "font-family": "Calibri",
    "font-size": "16px",
    "backgroundColor": 'rgb(255, 255, 255)',
    'width': '120px',
}

tab_selected_style = {
    "color": '#FF0000',
    "font-family": "Calibri",
    "font-size": "16px",
    "padding": "0vh",
    "backgroundColor": 'rgb(255, 255, 255)',
    'border-bottom': '2px #FF0000 solid',
    'width': '120px',
}

solar_current_power_chart = dcc.Graph(id = 'solar_current_power_chart',
                                      animate = True,
                                      config = {'displayModeBar': False},
                                      className = 'background2')
solar_today_power_chart = dcc.Graph(id = 'solar_today_power_chart',
                                    animate = True,
                                    config = {'displayModeBar': False},
                                    className = 'background2')
solar_yesterday_power_chart = dcc.Graph(id = 'solar_yesterday_power_chart',
                                        animate = True,
                                        config = {'displayModeBar': False},
                                        className = 'background2')

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src = app.get_asset_url('solar-panel.png'),
                     style = {'height': '30px'},
                     className = 'title_image'
                     ),
            html.H6('Solar Power Predictions',
                    style = {'color': '#1a1a1a'},
                    className = 'title'
                    ),
        ], className = 'logo_title'),
        html.P(id = 'get_date_time',
               style = {'color': '#eb6e4b'},
               className = 'adjust_date_time'
               )
    ], className = 'title_date_time_container'),
    html.Div([
        dcc.Interval(id = 'update_time',
                     interval = 1000,
                     n_intervals = 0),
    ]),
    html.Div([
        dcc.Interval(id = 'update_date_time_value',
                     interval = 60000,
                     n_intervals = 0),
    ]),
    html.Div([
        html.Div([
            html.Div([
                html.Div(id = 'solar_first_card')
            ], className = 'adjust_card'),
            html.Div([
                html.Div(id = 'solar_second_card')
            ], className = 'adjust_card'),
            html.Div([
                html.Div(id = 'solar_third_card')
            ], className = 'adjust_card'),
            html.Div([
                html.Div(id = 'solar_fourth_card')
            ], className = 'adjust_card'),
            html.Div([
                html.Div(id = 'solar_fifth_card')
            ], className = 'adjust_last_card'),
        ], className = 'background1')
    ], className = 'adjust_margin1'),
    html.Div([
        html.Div([
            dcc.Tabs(value = 'solar_today_power_chart', children = [
                dcc.Tab(solar_current_power_chart,
                        label = 'Current Power',
                        value = 'solar_current_power_chart',
                        style = tab_style,
                        selected_style = tab_selected_style,
                        ),
                dcc.Tab(solar_today_power_chart,
                        label = 'Today Power',
                        value = 'solar_today_power_chart',
                        style = tab_style,
                        selected_style = tab_selected_style,
                        ),
                dcc.Tab(solar_yesterday_power_chart,
                        label = 'Yesterday Power',
                        value = 'solar_yesterday_power_chart',
                        style = tab_style,
                        selected_style = tab_selected_style,
                        ),
            ], style = tabs_styles,
                     colors = {"border": None,
                               "primary": None,
                               "background": None}),
        ], className = 'tabs'),
        html.Div([
            html.Div([
                html.Div([
                    html.H6('Worcester, GB', className = 'title_city'),
                    html.Div(id = 'current_weather')
                ], className = 'weather1'),
                html.Div([
                ], className = 'weather2')
            ], className = 'weather_column')
        ], className = 'weather_background')
    ], className = 'adjust_margin2'),
])


@app.callback(Output('get_date_time', 'children'),
              [Input('update_time', 'n_intervals')])
def header_value_callback(n_intervals):
    header_value_data = header_value(n_intervals)

    return header_value_data


@app.callback(Output('solar_first_card', 'children'),
              [Input('update_date_time_value', 'n_intervals')])
def solar_first_card_value_callback(n_intervals):
    solar_first_card_value_data = solar_first_card_value(n_intervals)

    return solar_first_card_value_data


@app.callback(Output('solar_second_card', 'children'),
              [Input('update_date_time_value', 'n_intervals')])
def solar_second_card_value_callback(n_intervals):
    solar_second_card_value_data = solar_second_card_value(n_intervals)

    return solar_second_card_value_data


@app.callback(Output('solar_third_card', 'children'),
              [Input('update_date_time_value', 'n_intervals')])
def solar_third_card_value_callback(n_intervals):
    solar_third_card_value_data = solar_third_card_value(n_intervals)

    return solar_third_card_value_data


@app.callback(Output('solar_fourth_card', 'children'),
              [Input('update_date_time_value', 'n_intervals')])
def solar_fourth_card_value_callback(n_intervals):
    solar_fourth_card_value_data = solar_fourth_card_value(n_intervals)

    return solar_fourth_card_value_data


@app.callback(Output('solar_fifth_card', 'children'),
              [Input('update_date_time_value', 'n_intervals')])
def solar_fifth_card_value_callback(n_intervals):
    solar_fifth_card_value_data = solar_fifth_card_value(n_intervals)

    return solar_fifth_card_value_data


@app.callback(Output('solar_current_power_chart', 'figure'),
              [Input('update_date_time_value', 'n_intervals')])
def solar_current_power_chart_value_callback(n_intervals):
    solar_current_power_chart_value_data = solar_current_power_chart_value(n_intervals)

    return solar_current_power_chart_value_data


@app.callback(Output('solar_today_power_chart', 'figure'),
              [Input('update_date_time_value', 'n_intervals')])
def solar_today_power_chart_value_callback(n_intervals):
    solar_today_power_chart_value_data = solar_today_power_chart_value(n_intervals)

    return solar_today_power_chart_value_data


@app.callback(Output('solar_yesterday_power_chart', 'figure'),
              [Input('update_date_time_value', 'n_intervals')])
def solar_yesterday_power_chart_value_callback(n_intervals):
    solar_yesterday_power_chart_value_data = solar_yesterday_power_chart_value(n_intervals)

    return solar_yesterday_power_chart_value_data


@app.callback(Output('current_weather', 'children'),
              [Input('update_date_time_value', 'n_intervals')])
def current_weather_value_callback(n_intervals):
    current_weather_value_data = current_weather_value(n_intervals)

    return current_weather_value_data


if __name__ == "__main__":
    app.run_server(debug = True)
