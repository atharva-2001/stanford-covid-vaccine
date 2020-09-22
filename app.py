import os
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import plotly.express as px
import plotly.offline as po
import plotly.graph_objects as go
import colorsys
from plotly.subplots import make_subplots
import dash
import dash_bio as dashbio
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash_table import DataTable


train = pd.read_csv("train_outliers_removed.csv")

num = 13


def int_list(lst):
    lst = lst.split(",")
    lst[0] = lst[0].split("[")[1]
    lst[-1] = lst[-1].split("]")[0]

    lst = [float(item) for item in lst]
    return lst


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


# sequences is a dict with ids as keys and sequence and structure key value pairs as the sub dictionary to each key
sequences = dict()
colors = dict()
# from collections import defaultdict
options = [
    "deg_error_Mg_pH10",
    "deg_error_pH10",
    "deg_error_Mg_50C",
    "deg_error_50C",
    "deg_Mg_pH10",
    "deg_pH10",
    "deg_Mg_50C",
    "deg_50C",
    "reactivity_error",
    "reactivity",
]
# options_n_vals = dict.fromkeys(options, [])

from tqdm import tqdm

for index, row in tqdm(train.iterrows()):
    vals = {
        "sequence": row["sequence"][0:68],
        "structure": row["structure"][0:68],
    }
    for item in options:
        vals[item] = int_list(row[item])
        # options_n_vals[item] += vals[item]
    sequences[row["id"]] = vals

    colors[row["id"]] = {
        str(index): get_color(int(item))
        for index, item in enumerate(int_list(row["deg_error_Mg_pH10"]))
    }

# for datatable
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

# degrade = make_subplots(rows = 4, cols = 2)
# rows = [1,2,3,4,1,2,3,4]
# cols = [1,1,1,1,2,2,2,2]
# for option, row, col in zip(options, rows, cols):
#     degrade.add_trace(go.Histogram(x = options_n_vals[option]), row = row, col = col)


def grapher(ids, option):
    """
    The argument given to this function is a list of ids. and a column name
    The function's desired output is to return graph for the ids
    the value of the data is stored in sequences['column-name'], and the degradation values
    are yes, in float :)
    """

    fig = go.Figure()
    for id_ in ids:
        y = sequences[id_][option]
        fig.add_trace(
            go.Bar(
                x=list(sequences[id_]["sequence"]),
                y=y,
                name=id_ + "<br>" + sequences[id_]["sequence"],
            )
        )
    fig.update_layout(title=option, barmode="relative", bargap=0.1)
    return fig


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = True
server = app.server

app.layout = html.Div(
    [
        dashbio.FornaContainer(
            id="forna",
            colorScheme="structure",
            # customColors = colors,
            height=600,
            width=1000,
        ),  # forna container
        html.Div(
            DataTable(
                id="brief-data",
                data=df,
                columns=cols,
                style_cell={
                    "font-size": "16px",
                    "whiteSpace": "normal",
                    "height": "auto",
                },
            ),
            style={"display": "inline-block"},
        ),  # table
        html.Hr(),
        html.P(
            "Select the sequences to display below.",
            style={"font-size": "21px", "fontFamily": "Lucida Console"},
        ),
        dcc.Dropdown(
            id="forna-sequence-display",
            options=[{"label": name, "value": name} for name in sequences.keys()],
            multi=True,
            value=["id_001f94081"],
            style={"font-size": "17px", "fontFamily": "Lucida Console",},
        ),
        dcc.Graph(id="base-histogram"),
        dcc.Graph(id="bar1"),
        dcc.Graph(id="bar2"),
        dcc.Graph(id="bar3"),
        dcc.Graph(id="bar4"),
        dcc.Graph(id="bar5"),
        dcc.Graph(id="bar6"),
        dcc.Graph(id="bar7"),
        dcc.Graph(id="bar8"),
        dcc.Graph(id="bar9"),
        dcc.Graph(id="bar10"),
        dcc.Graph(
            id="stn-histogram",
            figure=px.histogram(
                x=train["signal_to_noise"], title="signal to noise histogram"
            ),
        )
        # dcc.Graph(id = 'degrade', figure = degrade )
        # dcc.Dropdown(
        #     id = 'selector',
        #     options = [{'label': item, 'value': item} for item in ["id_001f94081"]],
        #     multi = True,
        #     value = ["id_001f94081"],
        #     style={"font-size": "22px", "fontFamily": "Lucida Console"}
        # )
    ]
)


@app.callback(
    [
        dash.dependencies.Output("forna", "sequences"),
        dash.dependencies.Output("brief-data", "data"),
        dash.dependencies.Output("base-histogram", "figure"),
        dash.dependencies.Output("bar1", "figure"),
        dash.dependencies.Output("bar2", "figure"),
        dash.dependencies.Output("bar3", "figure"),
        dash.dependencies.Output("bar4", "figure"),
        dash.dependencies.Output("bar5", "figure"),
        dash.dependencies.Output("bar6", "figure"),
        dash.dependencies.Output("bar7", "figure"),
        dash.dependencies.Output("bar8", "figure"),
        dash.dependencies.Output("bar9", "figure"),
        dash.dependencies.Output("bar10", "figure"),
    ],
    [dash.dependencies.Input("forna-sequence-display", "value")],
)
def show_selected_sequences(value):
    if value is None:
        raise PreventUpdate

    # opts are options for the second dropdown
    # value has selected values

    seq, struc = [], []
    for index, selection in enumerate(value):
        _ = index  # was giving me an error so this
        seq.append(sequences[selection]["sequence"])
        struc.append(sequences[selection]["structure"])
        # sent = sent + "For ID {}, Sequence: {} \n Structure: {}".format(selection, seq[-1], struc[-1])

    df = pd.DataFrame({"ID": value, "sequence": seq, "stucture": struc})

    lst2 = []
    base_count_hist = go.Figure()
    for selection, item in zip(value, seq):
        lst2 = list(item)
        y = [
            lst2.count("A"),
            lst2.count("C"),
            lst2.count("G"),
            lst2.count("U"),
        ]
        base_count_hist.add_trace(
            go.Bar(
                x=["A", "C", "G", "U"],
                y=y,
                name=selection + "<br>" + item
                #  marker={'colorscale': 'Viridis'}
            )
        )

    base_count_hist.update_layout(title="Base Count", barmode="group", bargap=0.1)

    return (
        [sequences[selected_sequence] for selected_sequence in value],
        df.to_dict("records"),
        base_count_hist,
        grapher(value, "reactivity_error"),
        grapher(value, "deg_error_Mg_pH10"),
        grapher(value, "deg_error_pH10"),
        grapher(value, "deg_error_Mg_50C"),
        grapher(value, "deg_error_50C"),
        grapher(value, "reactivity"),
        grapher(value, "deg_Mg_pH10"),
        grapher(value, "deg_pH10"),
        grapher(value, "deg_Mg_50C"),
        grapher(value, "deg_50C"),
    )


if __name__ == "__main__":
    app.run_server(debug=True)
