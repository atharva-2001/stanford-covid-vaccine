

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
pd.set_option('max_columns', None)

# train = pd.read_csv('https://raw.githubusercontent.com/bigpappathanos-web/open_vaccine_covid/master/train_outliers_removed.csv')
train = pd.read_csv('train_outliers_removed.csv')
num = 13
def int_list(lst):
    lst = lst.split(',')
    lst[0] = lst[0].split('[')[1]
    lst[-1] = lst[-1].split(']')[0]
    
    lst = [float(item) for item in lst]
    return lst

# import plotly.express as px
# import plotly.offline as po
# import plotly.graph_objects as go

# po.init_notebook_mode(connected = True)
# px.histogram(x=int_list(train['deg_error_Mg_pH10'].tolist()[0])).show()
# main_ = []

# for item in train['deg_error_Mg_pH10'].tolist():
#     main_ = main_ + int_list(item)

# fig = go.Figure(data=[go.Histogram(x=main_)])
# fig.show()
import colorsys
def get_color(rtg):
    if type(rtg) is int:
        pass
    else:
        rtg = 1
#     assert 0 <= red_to_green <= 20
    # in HSV, red is 0 deg and green is 120 deg (out of 360);
    # divide red_to_green with 3 to map [0, 1] to [0, 1./3.]
#     hue = rtg / 3.0
#     r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
#     val = list(map(lambda x: int(255 * x), (r, g, b)))
    mark = 100
    val = [120, 50, mark * rtg]
    if val[2]>250:
        val[2] = 254
    val_str = 'rgb' + '(' + str(val[0])  + ', ' + str(val[1]) + ', ' + str(val[2]) + ')'
    return val_str


get_color('p')

sequences = dict()
colors = dict()
from tqdm import tqdm
for index, row in tqdm(train.iterrows()):
    sequences[row['id']] = {
        'sequence': row['sequence'][0:68],
        'structure': row['structure'][0:68]
    }
    colors[row['id']] = {str(index):get_color(int(item)) for index, item in enumerate(int_list(row['deg_error_Mg_pH10']))}
    
# sequences = dict(list(sequences.items())[0: 10])  
# colors = dict(list(colors.items())[0: 10])  
# sequences



import dash
import dash_bio as dashbio
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
# sequences is a dict with ids as keys and sequence and structure key value pairs as the sub dictionary to each key
sequences = sequences

app.layout = html.Div([
    dashbio.FornaContainer(
        id='forna',colorScheme='custom',
    customColors=colors
    ),
    html.Hr(),
    html.P('Select the sequences to display below.'),
    dcc.Dropdown(
        id='forna-sequence-display',
        options=[
            {'label': name, 'value': name} for name in sequences.keys()
        ],
        multi=True,
        value=['id_001f94081']
    )
])


@app.callback(
    dash.dependencies.Output('forna', 'sequences'),
    [dash.dependencies.Input('forna-sequence-display', 'value')]
)


def show_selected_sequences(value):
    if value is None:
        raise PreventUpdate
    return [
        sequences[selected_sequence]
        for selected_sequence in value
    ]


if __name__ == '__main__':
    app.run_server(debug=True)