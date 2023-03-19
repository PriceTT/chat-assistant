import os
import time
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State

import sqlite3

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


def create_chat_info_table(path: str = "./data/chat.db"):
    try:
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS "chat_info" ("index" INTEGER PRIMARY KEY, "model" TEXT, "title" TEXT, "prompt" TEXT, "chat" TEXT)'
        )
        conn.commit()
        conn.close()

    except Exception as err:
        logger.error(f"Error when trying to recreate the database - internal error: '{err}'")


def add_row_chat_info(title, model, prompt, chat, path: str = "./data/chat.db"):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO chat_info (title, model, prompt, chat) VALUES (?, ?, ?, ?)", (title, model, prompt, chat))
    conn.commit()
    conn.close()


# add_row_chat_info('Test', 'Test Prompt', 'Test Chat')


def update_chat_info(title, chat, path: str = "./data/chat.db"):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("UPDATE chat_info SET chat = ? WHERE title = ?", (chat, title))
    conn.commit()
    conn.close()


# update_chat_info(1, 'Updated Chat')


def get_row_chat_info(title):
    query = f"SELECT * FROM chat_info WHERE title = '{title}'"
    df = _generic_query(query)
    return df


def get_distinct_titles():
    query = "SELECT DISTINCT title FROM chat_info"
    df = _generic_query(query)
    return list(df.title.unique())


def _generic_query(query: str, path: str = "./data/chat.db") -> pd.DataFrame:
    conn = sqlite3.connect(path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
