from dash import html, dcc
import dash_bootstrap_components as dbc
from layout_files.sidebar import getSidebar
from layout_files.main_window import getMain

# text displayed in Instructions box at bottom of page.
_instructions = dcc.Markdown(
    """
    # **Instructions**
    click around
    """
)


def Navbar(app_name, issues_link):
    """The navbar of the website"""
    return dbc.NavbarSimple(
        children=[
            dcc.Store(id="browser-json-storage"),
            dcc.Location(id="url", refresh=False),  # navigation
            html.Label(
                [
                    "",
                    html.A(
                        "Request Features and Feedback!",
                        className="nav-link",
                        target="_blank",
                        href=issues_link,
                    ),
                ]
            ),
        ],
        brand="PriceResearchLab",
        brand_href="#",
        color="#272727",
        style={"font-weight": "bold"},
        dark=True,
        sticky="top",
    )


def Body(app_name):
    """The body of the website"""
    row1 = dbc.Row(
        [
            dbc.Col(
                html.H1(
                    id="header",
                    children=[app_name],
                ),
                md=9,
            )
        ]
    )
    row2 = dbc.Row([getSidebar(), getMain()])
    row3 = dbc.Row(
        children=[
            dbc.Col(
                children=[
                    _instructions,
                ],
                md=12,
                style={
                    "backgroundColor": "#FCFCFC",
                    "font-size": "12px",
                    "font-family": "Verdana",
                },
                className="col-dash",
            )
        ]
    )
    return dbc.Container(
        [
            row1,
            row2,
            html.Div(id="show-selected", style={"color": "#000000", "display": "none"}),
            html.Div(
                id="show-browser-data",
                style={"color": "#000000", "display": "none"},
                children="",
            ),
            html.Div(id="show-CV-selection", style={"color": "#000000"}, children=""),
        ]
    )
