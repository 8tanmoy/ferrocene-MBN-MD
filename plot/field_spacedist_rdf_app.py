import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots

#-- load and process dataframe --
df = pd.read_pickle('df_all.pkl')
#--------------------------------

app = dash.Dash(__name__)

def make_fig(selected_mbn):
    df_imbn         = df.iloc[selected_mbn]
    fig_freq        = px.violin(data_frame=df_imbn, y=df_imbn['freq'] , range_y=[-40, 40], box=True, labels={'y' : 'Δν'})
    fig_rdf         = px.line(data_frame=df_imbn, x=df_imbn['dist'], y=df_imbn['rdf'], range_y=[0, 1.0], range_x=[0, 1.5],
        labels={'y' : 'RDF', 'x' : 'r(nm)'})
    fig_rdf_cn      = px.line(data_frame=df_imbn, x=df_imbn['dist'], y=df_imbn['rdf_cn'], range_y=[0, 50], range_x=[0, 1.5],
        labels={'y' : 'Integrated RDF', 'x' : 'r(nm)'})
    return fig_freq, fig_rdf, fig_rdf_cn

fig_freq, fig_rdf, fig_rdf_cn = make_fig(0)

app.layout = html.Div(
    children=[
        dcc.Interval(id="animate", disabled=True), #interval=
        html.H1(children='Solvatochromic Frequency Shift with RDF',
            style={'textAlign' : 'center', 'color' : 'black'}),
        dcc.Graph(id='violin-plot',
            figure=fig_freq,
            style={'width' : '33.33%', 'float' : 'left'}),
        dcc.Graph(id='rdf',
            figure=fig_rdf,
            style={'width' : '33.33%', 'float' : 'left'}),
        dcc.Graph(id='rdf_cn',
            figure=fig_rdf_cn,
            style={'width' : '33.33%', 'float' : 'left'}),
        html.Br(),
        dcc.Slider(id='mbnpicker',
            min=0,
            max=31,
            step=1,
            value=0,
            tooltip={'placement' : 'bottom', 'always_visible' : True},
            marks={str(idx) : str(idx) for idx in df.index}
            ),
        html.Button("Play", id="play", style={'textAlign' : 'center', 'position' : 'relative', 'left' : '50%', 'font-size' : '24px'})
    ]
)

@app.callback(
    Output(component_id='violin-plot', component_property='figure'),
    Output(component_id='rdf', component_property='figure'),
    Output(component_id='rdf_cn', component_property='figure'),
    Output(component_id='mbnpicker', component_property='value'),
    Input(component_id="animate", component_property="n_intervals"),
    Input(component_id="mbnpicker", component_property="value"),
    #State(component_id='mbnpicker', component_property='value'),
    prevent_initial_call=True
    )
def update_figures(n, selected_mbn):
    mbn_idx = selected_mbn
    #mbn_idx = (selected_mbn + 1)%32
    fig_freq, fig_rdf, fig_rdf_cn = make_fig(mbn_idx)
    return fig_freq, fig_rdf, fig_rdf_cn, mbn_idx

@app.callback(
    Output("animate", "disabled"),
    Input("play", "n_clicks"),
    State("animate", "disabled"),
)
def toggle(n, playing):
    if n:
        return not playing
    return playing

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)