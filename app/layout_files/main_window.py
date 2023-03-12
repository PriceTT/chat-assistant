"""
The main window
"""
from dash import html, dcc
import dash_bootstrap_components as dbc


def getMain():
    """The main thing"""
    style = {"background-color": "#F5F5F6", "padding": "0px 0px 0px 0px"}
    children = [
        first_tab(),
        second_tab(),
    ]
    temp = dbc.Col(
        [
            dcc.Tabs(
                id="main-window-tabs",
                children=children,
                parent_className="custom-tabs",
                className="custom-tabs-container",
                value="first-tab-value",
            ),
        ],
        md=9,
        className="col-dash",
        style=style,
    )
    return temp


def first_tab():
    """hardcoded first tab"""
    # Define Layout
    conversation = html.Div(
        html.Div(id="display-conversation"),
        className="conversation-dash",
    )

    controls = dbc.InputGroup(
        children=[
            dbc.Input(
                id="user-input", placeholder="Write to the chatbot...", type="text"
            ),
            dbc.Button("Submit", id="submit"),
        ]
    )

    card = dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    html.Hr(),
                    dcc.Store(id="store-conversation", data=""),
                    conversation,
                    controls,
                    dbc.Spinner(html.Div(id="loading-component")),
                ],
            ),
            class_name="card-dash",
        ),
    )

    div = html.Div(id="main-first", className="tabbox-dash", children=card)

    tab = dcc.Tab(
        id="first-tab",
        value="first-tab-value",
        label="Chat",
        className="custom-tab",
        selected_className="custom-tab--selected",
        children=div,
    )

    return tab


def second_tab():
    """hardcoded second tab"""
    children = [
        html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            html.H2("Second Tab"),
                        )
                    )
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                dcc.Graph(
                                    id="graph-3",
                                    config={
                                        "displayModeBar": True,
                                        "displaylogo": False,
                                    },
                                )
                            ),
                            width=12,
                        ),
                        dbc.Col(
                            html.Div(
                                dcc.Graph(
                                    id="graph-4",
                                    config={
                                        "displayModeBar": True,
                                        "displaylogo": False,
                                    },
                                )
                            ),
                            width=12,
                        ),
                    ]
                ),
            ]
        )
    ]

    div = html.Div(id="main-multi-first", className="tabbox-dash", children=children)

    tab = dcc.Tab(
        id="second-tab",
        value="second-tab-value",
        label="Second Tab",
        className="custom-tab",
        selected_className="custom-tab--selected",
        children=div,
    )

    return tab
