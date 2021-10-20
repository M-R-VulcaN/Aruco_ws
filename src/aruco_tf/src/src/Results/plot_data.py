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

def add_person_data(csv_path, res_df = []):
    df = pd.read_csv(csv_path)
    

def create_fig(dir_path, max_time=-1, fig=None):
    global csv_df
    global rec_dir_path
    if rec_dir_path != dir_path or fig is None: #TODO: global fig and update instead of add_trace
        rec_dir_path = dir_path
        print(rec_dir_path)
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
                csv_df = pd.read_csv(glob.glob(dir_path + '/*.csv')[0])
                csv_df['time_sec_str'] =  (csv_df['pcapTime'] / 1000.0).apply(lambda x: '{0:.2f}'.format(x))
            except:
                print('no csv...')
                return fig  

    if PLOT_XYZ:
        csv_df_local = csv_df.copy()     
        if max_time > 0:
            csv_df_local = csv_df_local[csv_df_local['pcapTime'] / 1000.0 < max_time]
        #df['color_scale_str'] =  (df['pcapTime'] / 1000.0).apply(lambda x: int(x))
        tmp = px.scatter_3d(csv_df_local, x='x', y='y', z='z', text='time_sec_str', symbol='Lable', color='Lable').update_traces(mode='lines')
        for data in tmp.data:
            fig.add_trace(data)

    return fig

csv_df = None
rec_dir_path = None
app = dash.Dash(__name__)
rec_list = glob.glob(main_dir_path + '/*')
fig = create_fig(rec_list[-1])

app.layout = html.Div([
    dcc.Graph(id="scatter-plot", figure=fig, style={"height": "80vh"}),
    html.Div([
    dcc.Slider(
        id='my-slider',
        min=0,
        max=2000,
        step=1,
        value=2000,
    ),
    html.Div(id='slider-output-container')
]),
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
    Output('slider-output-container', 'children'),
    Input('rec_dropdown', 'value'), 
    Input('my-slider', 'value')
)
def update_output(rec_value, slider_value):
    return [create_fig(rec_value, slider_value, fig=None), None]

app.run_server(debug=True)
