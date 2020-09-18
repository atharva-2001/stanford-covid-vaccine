import os
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

pd.set_option("max_columns", None)

# train = pd.read_csv('https://raw.githubusercontent.com/bigpappathanos-web/open_vaccine_covid/master/train_outliers_removed.csv')
train = pd.read_csv("train_outliers_removed.csv")


num = 13


def int_list(lst):
    lst = lst.split(",")
    lst[0] = lst[0].split("[")[1]
    lst[-1] = lst[-1].split("]")[0]

    lst = [float(item) for item in lst]
    return lst


import plotly.express as px
import plotly.offline as po
import plotly.graph_objects as go

import colorsys


def get_color(rtg):
    if type(rtg) is int:
        pass
    else:
        rtg = 1
    mark = 100
    val = [120, 50, mark * rtg]
    if val[2] > 250:
        val[2] = 254
    val_str = "rgb" + "(" + str(val[0]) + ", " + str(val[1]) + ", " + str(val[2]) + ")"
    return val_str


get_color("p")

sequences = dict()
colors = dict()
from tqdm import tqdm

for index, row in tqdm(train.iterrows()):
    sequences[row["id"]] = {
        "sequence": row["sequence"],
        "structure": row["structure"],
    }
    colors[row["id"]] = {
        str(index): get_color(int(item))
        for index, item in enumerate(int_list(row["deg_error_Mg_pH10"]))
    }

sequences = dict(list(sequences.items())[0:10])
colors = dict(list(colors.items())[0:10])


import dash
import dash_bio as dashbio
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash_table import DataTable

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = True


# sequences is a dict with ids as keys and sequence and structure key value pairs as the sub dictionary to each key
df = pd.DataFrame(
    {
        "ID": ["id_001f94081"],
        "sequence": [sequences["id_001f94081"]["sequence"]],
        "stucture": [sequences["id_001f94081"]["structure"]],
    }
).to_dict("records")

cols = [
    {"name": "ID", "id": "ID"},
    {"name": "sequence", "id": "sequence"},
    {"name": "stucture", "id": "stucture"},
]
app.layout = html.Div(
    [
        dashbio.FornaContainer(
            id="forna",
            colorScheme="structure",
            # customColors = colors,
            height=700,
            width=1000,
        ),
        html.Div(
            DataTable(
                id="brief-data",
                data=df,
                columns=cols,
                style_cell={
                    "font-size": "22px",
                    "whiteSpace": "normal",
                    "height": "auto",
                },
            ),
            style={"display": "inline-block"},
        ),  # table
        html.Hr(),
        html.P(
            "Select the sequences to display below.",
            style={"font-size": "22px", "fontFamily": "Lucida Console"},
        ),
        dcc.Dropdown(
            id="forna-sequence-display",
            options=[{"label": name, "value": name} for name in sequences.keys()],
            multi=True,
            value=["id_001f94081"],
            style={"font-size": "22px", "fontFamily": "Lucida Console",},
        ),
    ]
)


@app.callback(
    [
        dash.dependencies.Output("forna", "sequences"),
        dash.dependencies.Output("brief-data", "data"),
    ],
    [dash.dependencies.Input("forna-sequence-display", "value")],
)
def show_selected_sequences(value):
    if value is None:
        raise PreventUpdate

    sent = ""
    seq, struc = [], []

    for index, selection in enumerate(value):

        seq.append(sequences[selection]["sequence"])
        struc.append(sequences[selection]["structure"])
        # sent = sent + "For ID {}, Sequence: {} \n Structure: {}".format(selection, seq[-1], struc[-1])

    df = pd.DataFrame({"ID": value, "sequence": seq, "stucture": struc})
    print()
    print(df.to_dict("records"))
    print("\t")
    return (
        [sequences[selected_sequence] for selected_sequence in value],
        df.to_dict("records"),
    )


if __name__ == "__main__":
    app.run_server(debug=True)
