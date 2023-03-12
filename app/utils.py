import os
import time
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State

import logging as logger
from textwrap import dedent
import openai


def textbox(text, box="assistant", name="user", image="user_img.jpg"):
    text = text.replace("user:", "").replace("assistant:", "")

    if box == "user":
        thumbnail = html.Img(
            src=image,
            className="thumbnail-user",
        )
        textbox = dbc.Card(
            dcc.Markdown(f"""{text}"""),
            class_name="textbox-user",
            body=True,
            color="primary",
            inverse=True,
        )

        return html.Div([thumbnail, textbox])

    elif box == "assistant":
        thumbnail = html.Img(
            src=image,
            className="thumbnail-ai",
        )
        textbox = dbc.Card(
            html.Div(
                [
                    dcc.Markdown(f"""{text}"""),
                    dcc.Clipboard(
                        style={
                            "position": "absolute",
                            "top": 0,
                            "right": 20,
                            "fontSize": 20,
                        },
                    ),
                ]
            ),
            class_name="textbox-ai",
            body=True,
            color="light",
            inverse=False,
        )

        return html.Div([thumbnail, textbox])

    else:
        raise ValueError("Incorrect option for `box`.")


#### Load Promt data


def load_prompts(url, path):
    try:
        logger.info("Loading prompts from github")
        df = pd.read_csv(url)
        if not df.empty:
            df.to_csv(path)
    except Exception as e:
        logger.error(e)
        df = pd.DataFrame(path)

    return df
