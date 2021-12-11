import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import boto3
from s3Connector import read_file,load_objects
from visualisations import get_visualisations

external_stylesheets = [dbc.themes.LUX]
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server
app._favicon = ('favicon.ico')
app.title = 'NYT Visualizations'

print("hello")

introduction = ['Project: New York Times User Engagement Analysis']
intro_para = "This project was done for SFU's CMPT 732 (Big Data I) course, with the goal of analyzing reader engagement for articles published in the New York Times (NYT). This was achieved by using NYT article and comment metadata for the years 2017-2021 to create visualizations to depict metrics and trends related to user engagement."

chart_type = ['CHLOROPLETH CHART', 'BAR CHART', 'PIE CHART', 'BAR CHART', 'BUBBLE CHART', 'BUBBLE CHART', 'LINE CHART', 'BAR CHART']

header = ['Location of NYT Commenters in the US', 'Top 10 Publishing Authors', 'Most Engaging News Desks', 'Top 10 Categories Of Articles', 'Highest Comment Count based on Authors & Categories', 'Highest Engagement based on Authors & Categories', 'Countries referenced by Articles on Covid-19', 'Sentiments amongst NYT Commenters']

para = ['The majority of commenters on NYT articles are from the United States. By seeing which states these commenters are from, we can gain insight into which states have the most avid NYT readers.', 'NYT employs a large number of authors to write their articles. This visualization shows that some of them are far more prolific than others. Their topics and writing style is likely what viewers mentally associate with NYT articles.', 'NYT articles are split across various news desks. Of all these, Editorial Opinions consistently hold the top position by a considerable margin. This reveals that viewers are often more interested in NYT’s stances, rather than facts, on ongoing affairs. ', 'NYT publishes articles about a diverse range of categories. The ‘US’ category far outstrips the rest - a reflection of the fact that most NYT readers are located within the country. Notably, opinion pieces are once again seen to outshine other categories, being consistently present within the top few contenders. ', 'The number of comments left on an article provides valuable insight into what viewers find interesting or worthwhile to discuss. Combined with our previous information on authors and categories, this visualization concisely reveals which combinations of them provoke the strongest response from viewers. ', 'Comment numbers alone do not provide the full picture. Commenters can leave recommendations to show their approval, which can be invaluable in measuring engagement between commenters. This visualization showcases which combinations of authors and topics provide the greatest amount of interaction and discussion between commenters.', 'Covid-19 was a topic that dominated the news for the past few years, both in NYT and elsewhere. Seeing the timeframe of which countries held prominence in the news cycles at various periods reflects the uneven progression of the Covid-19 pandemic across the world. ','Seeing the prevailing sentiments left in comments can be invaluable in giving a clearer picture of what viewers of NYT express after reading articles. We see that excitement consistently outstrips confusion in comments.' ]

type_colors = ['#E3747E', '#D96972', '#656EF2', '#DE6583', '#A6E8B3', '#CD5C58', '#F3A568', '#656EF2']

files_dict = load_objects()
figs = get_visualisations(files_dict=files_dict)

colors = {
    'background': '#242424',
    'text': '#7FDBFF'
}

navbar = dbc.Row(
                [
                    dbc.Col(html.Img(src="https://dataknyts-nyt-dump.s3.us-west-2.amazonaws.com/meta/dataknyts_logo.svg", alt='Data Knyts Logo',className='left_nav'),className="col-2 justify-content-right"),
                    dbc.Col(html.P("CMPT 732: BIG DATA 1 - PROJECT", className="mid_nav"),className="col-8 "),
                    dbc.Col(html.A([html.Img(src="https://dataknyts-nyt-dump.s3.us-west-2.amazonaws.com/meta/github.svg", alt='Github Logo')],href='https://github.com/banerj10/CMPT732_NYT_User_Engagement', className='left_nav' ),className="col-2 justify-content-left")
                ],
                style={'background':'white', 'height':'72px', 'box-shadow': '0px 4px 12px rgba(255, 255, 255, 0.08)'}
            )

def build_intro():
    div = html.Div(
            className = 'intro_div',
            children=[
            html.P(children='INTRODUCTION',
                   className='intro_chart_type',
                   style={
                       'color': '#A6E8B3'
                   }),
            html.H2(children=introduction[0],
                className = 'intro_header'),
            html.Br(),
            html.P(children = intro_para,
                   className = 'intro_para')
            ]
    )
    return div


def build_graph_divs(id,graph,graph_type,header_text,descriptor_text,graph_type_color):
    div = html.Div(
        className = 'graph_div',
        children=[
            html.P(children=graph_type,
                   className='graph_chart_type',
                   style={
                       'color': graph_type_color
                   }),
            html.H2(children=header_text,
                className = 'graph_header'),
            html.Br(),
            html.P(children = descriptor_text,
                   className = 'graph_para'),
            html.Br(),
            html.Br(),
            dcc.Graph(
                id='Graph'+str(id),
                figure=graph,
            )
        ]
    )
    return div

def build_children():
    children = []
    for x in range(8):
        children.append(build_graph_divs(x+1,figs[x],chart_type[x],header[x],para[x],type_colors[x]))
        children.append(html.Br())
        children.append(html.Br())
        children.append(html.Br())
    return children

main_children = build_children()
main_children.insert(0,html.Br())
main_children.insert(0,build_intro())

app.layout = html.Div(style={'backgroundColor': colors['background']},
 children=[
    #dbc.NavItem(dbc.NavLink("Time-Series", href="/time-series")),
    navbar,
    html.Div(
    className = 'graph',
    children=main_children
    )
])

if __name__ == '__main__':
    #app.run_server(port=5000,debug=True)
    app.run_server(host="127.0.0.1",debug = True, port = 8050)


    '''[build_graph_divs(1,figs[0],chart_type[0],header[1],para[1]),
    
    build_graph_divs(2,figs[1],chart_type[1],header[1],para[1]),
    dcc.Graph(
        id='Graph3',
        figure=figs[2],    
    ),
    dcc.Graph(
        id='Graph4',
        figure=figs[3],    
    ),
    dcc.Graph(
        id='Graph5',
        figure=figs[4],
    ),
    dcc.Graph(
        id='Graph6',
        figure=figs[5],    
    ),
    dcc.Graph(
        id='Graph7',
        figure=figs[6],    
    ),
    dcc.Graph(
        id='Graph8',
        figure=figs[7],
    )
]'''