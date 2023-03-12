import os
import logging
import binascii
from textwrap import dedent

import flask
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import openai
import pandas as pd


from layout_files.layout import Navbar, Body
import utils as ui

logger_file_path = "./log/debug.log"
logging.basicConfig(
    format="[%(asctime)s] : [%(levelname)s] : [%(filename)s:%(lineno)s] : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
    handlers=[logging.FileHandler(logger_file_path, mode="a"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Create Flask app
app = flask.Flask(__name__)

#### Load configuration
app.config.from_pyfile("config/default.cfg")
app.config["ENVIRONMENT"] = "local"  # os.getenv("AWS_ENV", "local").lower()
app.config["SECRET_KEY"] = binascii.hexlify(os.urandom(24))
app.config.from_pyfile("config/" + app.config["ENVIRONMENT"] + ".cfg")
APP_NAME = app.config["APP_NAME"]
USER_IMG = app.config["USER_IMG"]
AI_IMG = app.config["AI_IMG"]
logger.info(f"Loading {APP_NAME}")

# Authentication
app.config.from_pyfile("config/.env")
API_KEY = app.config["API_KEY"]
openai.api_key = API_KEY
gpt_models = openai.Model.list()

#### Create Dash app
dash_app = dash.Dash(__name__, server=app, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_app.title = app.config["APP_NAME"]

#### Load Promt data
PROMPT_PATH = "./data/prompts.csv"
url = "https://raw.githubusercontent.com/f/awesome-chatgpt-prompts/main/prompts.csv"
df = ui.load_prompts(url, PROMPT_PATH)

#### Layout
dash_app.layout = html.Div(
    children=[
        html.Div(
            [
                Navbar(APP_NAME, app.config["ISSUE_LINK"]),
                Body(APP_NAME),
            ]
        )
    ]
)


#### Callbacks
@dash_app.callback(
    [
        Output("dropdown-prompt", "options"),
        Output("dropdown-prompt", "value"),
        Output("textarea-prompt", "value"),
        Output("dropdown-model", "options"),
    ],
    [
        Input("url", "href"),
        Input("dropdown-prompt", "value"),
    ],
)
def populate_dropdown_on_load(url, prompt_value):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

    if "url" in changed_id:
        prompt_values = sorted(list(df.act.unique()))
        prompt = [{"label": name, "value": name} for name in prompt_values]
        prompt_value = prompt_values[0]
        prompt_text = df[df.act == prompt_value].prompt.values[0]

        models = sorted([mod["root"] for mod in gpt_models["data"]])
        model_options = [{"label": name, "value": name} for name in models]

        return prompt, prompt_value, prompt_text, model_options

    if "dropdown-prompt" in changed_id and prompt_value:
        prompt_text = df[df.act == prompt_value].prompt.values[0]

        return dash.no_update, dash.no_update, prompt_text, dash.no_update


@dash_app.callback(
    Output("display-conversation", "children"),
    [Input("store-conversation", "data")],
    State("dropdown-model", "value"),
)
def update_display(chat_history, model):
    if "turbo" in model:
        chat_list = [
            ui.textbox(x["content"], box="user", image=USER_IMG)
            if x["role"] == "user"
            else ui.textbox(x["content"], box="assistant", image=AI_IMG)
            for x in chat_history
        ]
    else:
        chat_list = [
            ui.textbox(x, box="user", image=USER_IMG) if i % 2 == 0 else ui.textbox(x, box="assistant", image=AI_IMG)
            for i, x in enumerate(chat_history.split("<split>")[:-1])
        ]

    return chat_list


@dash_app.callback(
    Output("user-input", "value"),
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
)
def clear_input(n_clicks, n_submit):
    return ""


@dash_app.callback(
    [Output("store-conversation", "data"), Output("loading-component", "children")],
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    [
        State("user-input", "value"),
        State("store-conversation", "data"),
        State("dropdown-model", "value"),
        State("textarea-prompt", "value"),
        State("textarea-format", "value"),
        State("input-tokens", "value"),
        State("input-temp", "value"),
    ],
)
def run_chatbot(
    n_clicks,
    n_submit,
    user_input,
    chat_history,
    model,
    tone,
    response_format,
    tokens,
    temp,
):
    if n_clicks == 0 and n_submit is None:
        return "", None

    if user_input is None or user_input == "":
        return chat_history, None

    name_ai = "assistant"
    name_user = "user"

    if "turbo" in model:
        if chat_history is None or chat_history == "":
            chat_history = []
        prompt = {"role": "system", "content": f"{tone} {response_format}\n"}
        chat_history.append({"role": "user", "content": user_input})
        model_input = chat_history.copy()
        model_input.insert(0, prompt)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=model_input,
            max_tokens=tokens,
            temperature=temp,
        )
        model_output = response.choices[0]["message"]["content"].strip()
        chat_history.append({"role": "assistant", "content": model_output})

    else:
        prompt = dedent(f"system:{tone} {response_format}.\n")

        # First add the user input to the chat history
        chat_history += f"{name_user}: {user_input}<split>{name_ai}:"

        model_input = prompt + chat_history.replace("<split>", "\n")

        response = openai.Completion.create(
            engine=model,
            prompt=model_input,
            max_tokens=tokens,
            stop=[f"{name_user}:"],
            temperature=temp,
        )
        model_output = response.choices[0].text.strip()

        chat_history += f"{model_output}<split>"

    return chat_history, None


#### Start the Dash app
if __name__ == "__main__":
    if app.config["DEBUG"] == True:
        # run interactive debugger with hot-reloading which Flask cannot serve
        dash_app.run_server(port=app.config["PORT"], host="0.0.0.0", debug=True)
    else:
        dash_app.run(port=app.config["PORT"], host="0.0.0.0", debug=False)
