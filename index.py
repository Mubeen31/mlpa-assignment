import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime
from components.last_data_update_time import last_data_update_time_value
from components.solar_yesterday_power_chart import solar_yesterday_power_chart_value
from components.dt_regression import dt_regression_chart_value
from components.knn_regression import knn_regression_chart_value, n_neighbors_list
from components.summary import summary_value
from components.current_weather import current_weather_value
from components.first_hour_forecast import first_hour_forecast_weather_value
from components.second_hour_forecast import second_hour_forecast_weather_value
from components.third_hour_forecast import third_hour_forecast_weather_value

font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
meta_tags = [{"name": "viewport", "content": "width=device-width"}]
external_stylesheets = [meta_tags, font_awesome]

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
server = app.server
app.title = 'Solar Energy Predictions'

tabs_styles = {
    "flex-direction": "row",
}
tab_style = {
    "padding": "0vh",
    "color": '#1a1a1a',
    "font-family": "Calibri",
    "font-size": "16px",
    "backgroundColor": '#d9d9d9',
    # 'border-bottom': '2px #FF0000 solid',
    'border-left': '2px #ffffff solid',
    # 'width': '120px',
}

tab_style1 = {
    "padding": "0vh",
    "color": '#1a1a1a',
    "font-family": "Calibri",
    "font-size": "16px",
    "backgroundColor": '#d9d9d9',
    # 'border-bottom': '2px #FF0000 solid',
    # 'width': '120px',
}

tab_selected_style = {
    "color": '#FF0000',
    "font-family": "Calibri",
    "font-size": "16px",
    "padding": "0vh",
    "backgroundColor": 'rgb(255, 255, 255)',
    # 'width': '120px',
}

solar_yesterday_power_chart = dcc.Graph(id = 'solar_yesterday_power_chart',
                                        animate = True,
                                        config = {'displayModeBar': False},
                                        className = 'background2')
dt_regression_chart = dcc.Graph(id = 'dt_regression_chart',
                                animate = True,
                                config = {'displayModeBar': False},
                                className = 'background2')
knn_regression_chart = html.Div([
    html.Div([
        html.Div([
            dcc.Graph(id = 'knn_regression_chart',
                      animate = True,
                      config = {'displayModeBar': False},
                      className = 'background2')
        ], className = 'random_forest_regression_chart'),
        html.Div([
            html.Div([
                html.P('N neighbors',
                       style = {'color': '#D35940'},
                       className = 'drop_down_list_title'
                       ),
                dcc.Dropdown(id = 'select_neighbors',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             value = 6,
                             placeholder = 'Select neighbors',
                             options = n_neighbors_list,
                             className = 'drop_down_list'),
            ], className = 'title_drop_down_list'),
            # html.Div([
            #     html.P('Random states',
            #            style = {'color': '#D35940'},
            #            className = 'drop_down_list_title'
            #            ),
            #     dcc.Dropdown(id = 'select_random_state',
            #                  multi = False,
            #                  clearable = True,
            #                  disabled = False,
            #                  style = {'display': True},
            #                  value = 0,
            #                  placeholder = 'Select random states',
            #                  options = random_state_list,
            #                  className = 'drop_down_list'),
            # ], className = 'title_drop_down_list')
        ], className = 'drop_down_list_row')
    ], className = 'three_elements_column'),

]),

summary = html.Div(id = 'summary',
                   className = 'background2')

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src = app.get_asset_url('solar-panel.png'),
                     style = {'height': '30px'},
                     className = 'title_image'
                     ),
            html.H6('Solar Energy Predictions Using K Nearest Neighbors and Decision Tree Regressions Models',
                    style = {'color': '#1a1a1a'},
                    className = 'title'
                    ),
        ], className = 'logo_title'),
        html.P(id = 'last_data_update_time',
               style = {'color': '#eb6e4b'},
               className = 'adjust_date_time'
               ),
        # html.P(id = 'get_date_time',
        #        style = {'color': '#eb6e4b'},
        #        className = 'adjust_date_time'
        #        )
    ], className = 'title_date_time_container'),
    # html.Div([
    #     dcc.Interval(id = 'update_time',
    #                  interval = 1000,
    #                  n_intervals = 0),
    # ]),
    html.Div([
        dcc.Interval(id = 'update_date_time_value',
                     interval = 60000,
                     n_intervals = 0),
    ]),

    html.Div([
        html.Div([
            dcc.Tabs(value = 'knn_regression_chart', children = [
                dcc.Tab(solar_yesterday_power_chart,
                        label = 'Yesterday Energy',
                        value = 'solar_yesterday_power_chart',
                        style = tab_style1,
                        selected_style = tab_selected_style,
                        ),
                dcc.Tab(dt_regression_chart,
                        label = 'DTR Model',
                        value = 'dt_regression_chart',
                        style = tab_style,
                        selected_style = tab_selected_style,
                        ),
                dcc.Tab(knn_regression_chart,
                        label = 'KNN Model',
                        value = 'knn_regression_chart',
                        style = tab_style,
                        selected_style = tab_selected_style,
                        ),
                dcc.Tab(summary,
                        label = 'Summary',
                        value = 'summary',
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
                    html.Div([
                        html.Div(id = 'first_hour_forecast'),
                        html.Div(id = 'second_hour_forecast'),
                        html.Div(id = 'third_hour_forecast')
                    ], className = 'forecast_cards_row'),
                ], className = 'weather2')
            ], className = 'weather_column')
        ], className = 'weather_background')
    ], className = 'adjust_margin2'),
])


@app.callback(Output('last_data_update_time', 'children'),
              [Input('update_date_time_value', 'n_intervals')])
def last_data_update_time_value_callback(n_intervals):
    last_data_update_time_value_data = last_data_update_time_value(n_intervals)

    return last_data_update_time_value_data


@app.callback(Output('solar_yesterday_power_chart', 'figure'),
              [Input('update_date_time_value', 'n_intervals')])
def solar_yesterday_power_chart_value_callback(n_intervals):
    solar_yesterday_power_chart_value_data = solar_yesterday_power_chart_value(n_intervals)

    return solar_yesterday_power_chart_value_data


@app.callback(Output('dt_regression_chart', 'figure'),
              [Input('update_date_time_value', 'n_intervals')])
def dt_regression_chart_value_callback(n_intervals):
    dt_regression_chart_value_data = dt_regression_chart_value(n_intervals)

    return dt_regression_chart_value_data


@app.callback(Output('knn_regression_chart', 'figure'),
              [Input('update_date_time_value', 'n_intervals')],
              [Input('select_neighbors', 'value')])
def knn_regression_chart_value_callback(n_intervals, select_neighbors):
    knn_regression_chart_value_data = knn_regression_chart_value(n_intervals, select_neighbors)

    return knn_regression_chart_value_data


@app.callback(Output('summary', 'children'),
              [Input('update_date_time_value', 'n_intervals')],
              [Input('select_neighbors', 'value')])
def summary_value_callback(n_intervals, select_neighbors):
    summary_value_data = summary_value(n_intervals, select_neighbors)

    return summary_value_data


@app.callback(Output('current_weather', 'children'),
              [Input('update_date_time_value', 'n_intervals')])
def current_weather_value_callback(n_intervals):
    current_weather_value_data = current_weather_value(n_intervals)

    return current_weather_value_data


@app.callback(Output('first_hour_forecast', 'children'),
              [Input('update_date_time_value', 'n_intervals')])
def first_hour_forecast_value_callback(n_intervals):
    first_hour_forecast_value_data = first_hour_forecast_weather_value(n_intervals)

    return first_hour_forecast_value_data


@app.callback(Output('second_hour_forecast', 'children'),
              [Input('update_date_time_value', 'n_intervals')])
def second_hour_forecast_value_callback(n_intervals):
    second_hour_forecast_value_data = second_hour_forecast_weather_value(n_intervals)

    return second_hour_forecast_value_data


@app.callback(Output('third_hour_forecast', 'children'),
              [Input('update_date_time_value', 'n_intervals')])
def third_hour_forecast_value_callback(n_intervals):
    third_hour_forecast_value_data = third_hour_forecast_weather_value(n_intervals)

    return third_hour_forecast_value_data


if __name__ == "__main__":
    app.run_server(debug = True)
