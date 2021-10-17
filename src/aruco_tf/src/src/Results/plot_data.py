import yaml
import glob
import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly

PLOT_XYZ = True

main_dir_path = "/home/makeruser/Desktop/record-wifi-results/"

def read_yaml(yaml_path=''):
    with open(yaml_path) as file:
        room_data = yaml.load(file, Loader=yaml.FullLoader)
    return room_data

def create_df(room_data):
    locations = pd.DataFrame(room_data['locations']).T
    locations['name'] = locations.index
    locations['group'] = locations['x'] * 0
    locations['group'][locations['name'].str.startswith('qr')] = 'qrcodes'
    locations['group'][locations['name'].str.startswith('192')] = 'antennas'
    locations.drop(index='room', inplace=True)

    rx = room_data['locations']['room']['x']
    ry = room_data['locations']['room']['y']
    walls = room_data['wall_structure']
    room_lines_dict = {'x0': [[0, 0], [rx, 0]],
                       'x1': [[0, ry], [rx, ry]],
                       'y0': [[0, 0], [0, ry]],
                       'y1': [[rx, 0], [rx, ry]]
    }
    room_lines = pd.DataFrame()
    for key in room_lines_dict.keys():
        for pts in room_lines_dict[key]:
            room_lines = room_lines.append({'name': key, 'struct': walls[key], 'x': pts[0], 'y': pts[1], 'z': 0}, ignore_index=True)
    return locations, room_lines

def create_fig(dir_path):
    yaml_path = dir_path + '/params.yaml'
    room_data = read_yaml(yaml_path)
    locations, room_lines = create_df(room_data)

    fig = px.line_3d(room_lines, x='x', y='y', z='z', hover_data=['struct'], color='name', title=room_data['description'])

    fig_locations = px.scatter_3d(locations, symbol='group',
                                  x='x', y='y', z='z',
                                  hover_data=['name'])
    for data in fig_locations.data:
        fig.add_trace(data)

    if PLOT_XYZ:
        try:
            df = pd.read_csv(glob.glob(dir_path + '/*.csv')[0])
        except:
            return fig            
        fig.add_trace(plotly.graph_objs.Scatter3d(x=df['x'], y=df['y'], z=df['z'], name='xyz', mode='lines', 
            hovertemplate='<b>%{text}</b><extra></extra>', text = [str(_str/1000) for _str in df['pcapTime']]))


    return fig

app = dash.Dash(__name__)
rec_list = glob.glob(main_dir_path + '/*')
fig = create_fig(rec_list[0])

app.layout = html.Div([
    dcc.Graph(id="scatter-plot", figure=fig, style={"height": "80vh"}),
    html.P("Recording List:"),
    dcc.Dropdown(
        id='rec_dropdown',
        options=[{'label': rec.split('/')[-1], 'value': rec} for rec in rec_list],
        value=rec_list[-1]
    ),
    html.Div(id='dd-output-container')
])

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('rec_dropdown', 'value')
)
def update_output(value):
    return create_fig(value)

app.run_server(debug=True)
