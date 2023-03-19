r"""
The sidebar
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
import os
import sys


####################################################################################


def getSidebar():
    """handle to get the entire sidebar"""

    children = [load_data_tab()]
    sidebar = dbc.Col(
        children=[
            dcc.Tabs(
                id="panel-control-tabs",
                value="load-model-tab-value",
                parent_className="custom-tabs",
                className="custom-tabs-container",
                children=children,
            )
        ],
        md=3,
        className="col-dash",
        style={"background-color": "#F5F5F6", "padding": "0px 0px 0px 0px"},
    )
    return sidebar


def load_data_tab():
    """hardcoded first tab"""
    children = [
        html.P("Prompt", className="text-dash-center"),
        dcc.Dropdown(
            id="dropdown-prompt",
            placeholder="Select prompt",
            clearable=False,
        ),
        html.Br(),
        dbc.Textarea(
            valid=True,
            size="lg",
            className="mb-3",
            rows=15,
            id="textarea-prompt",
            class_name="textbox-dash",
        ),
        html.Br(),
        html.P("Response formatting.", className="text-dash-center"),
        dbc.Textarea(
            valid=True,
            size="sm",
            className="mb-3",
            value="Return all responses formatted using markdown.",
            rows=2,
            id="textarea-format",
            class_name="textbox-dash",
        ),
        html.Br(),
        html.P("Model type", className="text-dash-center"),
        dcc.Dropdown(
            id="dropdown-model",
            placeholder="Select model",
            value="gpt-3.5-turbo",
            clearable=False,
        ),
        html.Br(),
        html.P("Max number tokens", className="text-dash-center"),
        dbc.Input(
            type="number",
            min=100,
            max=4000,
            step=1,
            value=256,
            placeholder="Max number tokens",
            id="input-tokens",
        ),
        html.Br(),
        html.P("Temperature", className="text-dash-center"),
        dcc.Slider(
            min=0,
            max=1,
            value=0,
            step=0.1,
            id="input-temp",
        ),
        html.Br(),
        dbc.Button(
            "Click to save",
            outline=True,
            color="secondary",
            className="button-dash",
            id="button-save-prompt",
        ),
        dbc.Tooltip(
            "Save Chat",
            target="button-save-prompt",
        ),
        dbc.Alert(
            id="save-alert",
            is_open=True,
            dismissable=True,
            duration=5000,
        ),
    ]

    div = html.Div(id="tabbox-first", className="tabbox-dash", children=children)

    tab = dcc.Tab(
        id="load-model-tab",
        value="load-model-tab-value",
        label="Update model settings",
        className="custom-tab",
        selected_className="custom-tab--selected",
        children=div,
    )
    return tab
