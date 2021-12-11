#Import Libs
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

import dash
from dash import dcc
from dash import html

def get_visualisations(files_dict):
    figs = []
    #fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
    #Graph-1: TOP 10 CATEGORIES OF ARTICLES - BY YEAR // df_keyword_count_overall['count'] vs df_keyword_count_overall['section_name']

    df_keyword_count_overall = files_dict['section_name_count']['0']
    df_keyword_count_2021 = files_dict['section_name_count']['1']
    df_keyword_count_2020 = files_dict['section_name_count']['2']
    df_keyword_count_2019 = files_dict['section_name_count']['3']
    df_keyword_count_2018 = files_dict['section_name_count']['4']
    df_keyword_count_2017 = files_dict['section_name_count']['5']

    df_keyword_count_overall = df_keyword_count_overall.iloc[::-1]
    df_keyword_count_2021 = df_keyword_count_2021.iloc[::-1]
    df_keyword_count_2020 = df_keyword_count_2020.iloc[::-1]
    df_keyword_count_2019 = df_keyword_count_2019.iloc[::-1]
    df_keyword_count_2018 = df_keyword_count_2018.iloc[::-1]
    df_keyword_count_2017 = df_keyword_count_2017.iloc[::-1]


    # In[4]:


    #Graph-1 TOP 10 CATEGORIES OF ARTICLES - BY YEAR"

    fig1 = go.Figure(data=[go.Bar(
        name='Overall',
        x=df_keyword_count_overall['count'],
        y=df_keyword_count_overall['section_name'],
        orientation='h', text=df_keyword_count_overall['count'],
        marker_color=df_keyword_count_overall['count'], marker_colorscale = px.colors.sequential.Agsunset,
    ),
        go.Bar(
        name='2021',
        x=df_keyword_count_2021['count'],
        y=df_keyword_count_2021['section_name'],
        orientation='h',text=df_keyword_count_2021['count'],visible=False,
        marker_color=df_keyword_count_2021['count'], marker_colorscale = px.colors.sequential.Agsunset,
    ),                       
        go.Bar(
        name='2020',
        x=df_keyword_count_2020['count'],
        y=df_keyword_count_2020['section_name'],
        orientation='h',text=df_keyword_count_2020['count'],visible=False,
        marker_color=df_keyword_count_2020['count'], marker_colorscale = px.colors.sequential.Agsunset,
    ),
        go.Bar(
        name='2019',
        x=df_keyword_count_2019['count'],
        y=df_keyword_count_2019['section_name'],
        orientation='h',text=df_keyword_count_2019['count'],visible=False,
        marker_color=df_keyword_count_2019['count'], marker_colorscale = px.colors.sequential.Agsunset,
    ),
        go.Bar(
        name='2018',
        x=df_keyword_count_2018['count'],
        y=df_keyword_count_2018['section_name'],
        orientation='h',text=df_keyword_count_2018['count'],visible=False,
        marker_color=df_keyword_count_2018['count'], marker_colorscale = px.colors.sequential.Agsunset,
            
    ),
        go.Bar(
        name='2017',
        x=df_keyword_count_2017['count'],
        y=df_keyword_count_2017['section_name'],
        orientation='h',text=df_keyword_count_2017['count'],visible=False,
        marker_color=df_keyword_count_2017['count'], marker_colorscale = px.colors.sequential.Agsunset,
    ),                    
    ])
    

    # Add dropdown
    fig1.update_layout(
        updatemenus=[ 
            dict(
                #direction='down',
                showactive= False,
                x=0.11,
                y = 1.15,
                active=0,
                buttons=list([
                    dict(label="Overall",
                        method="update",
                        args=[{"visible": [True, False, False, False, False, False]}
                            ]),
                    dict(label="2021",
                        method="update",
                        args=[{"visible": [False, True, False, False, False, False]}
                            ]),
                    dict(label="2020",
                        method="update",
                        args=[{"visible": [False, False, True, False, False, False]}
                                ]),
                    dict(label="2019",
                        method="update",
                        args=[{"visible": [False, False, False, True, False, False]}]),
                    dict(label="2018",
                        method="update",
                        args=[{"visible": [False, False, False, False, True, False]}]),
                    dict(label="2017",
                        method="update",
                        args=[{"visible": [False, False, False, False, False, True]}]),
                ]),
            )

        ])


    fig1.update_layout(
        title_x=0.5,#title_y=0.88,
        xaxis_title="Number of Articles",
        yaxis_title="Categories",
        template='plotly_dark',
        height= 600,
        xaxis=dict(showspikes=True, linecolor="#BCCCDC",
            #showspikes=True, # Show spike line for X-axis
            # Format spike
            spikethickness=2,
            spikedash="dot",
            spikecolor="#999999",
            spikemode="across",
        ),
        #legend_title="Legend Title",
    )

    fig1.update_traces(textposition = "outside")

    #fig1.show()


    # In[38]:


    #Graph-2: MOST ENGAGING ARTICLES BY EDITORIAL HOUSE (NEWS DESK) // df_news_desk_count_overall['newsdesk'] vs df_news_desk_count_overall['engagement']
    df_news_desk_count_overall = files_dict['piechart_news_desk_sum']['0']
    df_news_desk_count_2021 = files_dict['piechart_news_desk_sum']['1']
    df_news_desk_count_2020 = files_dict['piechart_news_desk_sum']['2']
    df_news_desk_count_2019 = files_dict['piechart_news_desk_sum']['3']
    df_news_desk_count_2018 = files_dict['piechart_news_desk_sum']['4']
    df_news_desk_count_2017 = files_dict['piechart_news_desk_sum']['5']


    # In[41]:


    df_news_desk_count_overall = df_news_desk_count_overall.rename(columns={"Category":"newsdesk", "total_recommendations":"engagement"}) 
    df_news_desk_count_2021 = df_news_desk_count_2021.rename(columns={"Category":"newsdesk", "total_recommendations":"engagement"}) 
    df_news_desk_count_2020 = df_news_desk_count_2020.rename(columns={"Category":"newsdesk", "total_recommendations":"engagement"}) 
    df_news_desk_count_2019 = df_news_desk_count_2019.rename(columns={"Category":"newsdesk", "total_recommendations":"engagement"}) 
    df_news_desk_count_2018 = df_news_desk_count_2018.rename(columns={"Category":"newsdesk", "total_recommendations":"engagement"}) 
    df_news_desk_count_2017 = df_news_desk_count_2017.rename(columns={"Category":"newsdesk", "total_recommendations":"engagement"}) 


    # In[42]:


    df_news_desk_count_overall = df_news_desk_count_overall.replace('OpEd', 'Editorial Opinion')
    df_news_desk_count_2021 = df_news_desk_count_2021.replace('OpEd', 'Editorial Opinion')
    df_news_desk_count_2020 = df_news_desk_count_2020.replace('OpEd', 'Editorial Opinion')
    df_news_desk_count_2019 = df_news_desk_count_2019.replace('OpEd', 'Editorial Opinion')
    df_news_desk_count_2018 = df_news_desk_count_2018.replace('OpEd', 'Editorial Opinion')
    df_news_desk_count_2017 = df_news_desk_count_2017.replace('OpEd', 'Editorial Opinion')


    # In[ ]:


    """df_news_desk_count_overall = df_news_desk_count_overall.iloc[1: , :]"""
    """
    df_news_desk_count_2021 = df_news_desk_count_2021.iloc[1: , :]
    df_news_desk_count_2020 = df_news_desk_count_2020.iloc[1: , :]
    df_news_desk_count_2019 = df_news_desk_count_2019.iloc[1: , :]
    df_news_desk_count_2018 = df_news_desk_count_2018.iloc[1: , :]
    df_news_desk_count_2017 = df_news_desk_count_2017.iloc[1: , :]
    """


    # In[46]:


    #Graph-2 MOST ENGAGING ARTICLES BY EDITORIAL HOUSE (NEWS DESK)"

    #Plotting
    fig2 = go.Figure(data=[go.Pie(
        name='Overall',
        labels=df_news_desk_count_overall['newsdesk'],
        values=df_news_desk_count_overall['engagement'],
        pull=[0.2, 0, 0, 0, 0, 0, 0, 0],
    ),

    go.Pie(
        name='2021',
        labels=df_news_desk_count_2021['newsdesk'],
        values=df_news_desk_count_2021['engagement'],
        pull=[0.2, 0, 0, 0, 0, 0, 0, 0],
        visible=False,
    ),
    go.Pie(
        name='2020',
        labels=df_news_desk_count_2020['newsdesk'],
        values=df_news_desk_count_2020['engagement'],
        pull=[0.2, 0, 0, 0, 0, 0, 0, 0],
        visible=False, 
    ),
    go.Pie(
        name='2019',
        labels=df_news_desk_count_2019['newsdesk'],
        values=df_news_desk_count_2019['engagement'],
        pull=[0.2, 0, 0, 0, 0, 0, 0, 0],
        visible=False,
    ),
    go.Pie(
        name='2018',
        labels=df_news_desk_count_2018['newsdesk'],
        values=df_news_desk_count_2018['engagement'],
        pull=[0.2, 0, 0, 0, 0, 0, 0, 0],
        visible=False, 
    ),
    go.Pie(
        name='2017',
        labels=df_news_desk_count_2017['newsdesk'],
        values=df_news_desk_count_2017['engagement'],
        pull=[0.2, 0, 0, 0, 0, 0, 0, 0],
        visible=False,
    ),                        
    ])
    

    # Add dropdown
    fig2.update_layout(
        updatemenus=[ 
            dict(
                #direction='down',
                showactive= False,
                x=0.11,
                y = 1,
                active=0,
                buttons=list([
                    dict(label="Overall",
                        method="update",
                        args=[{"visible": [True, False, False, False, False, False]}
                            ]),
                    dict(label="2021",
                        method="update",
                        args=[{"visible": [False, True, False, False, False, False]}
                            ]),
                    dict(label="2020",
                        method="update",
                        args=[{"visible": [False, False, True, False, False, False]}
                                ]),
                    dict(label="2019",
                        method="update",
                        args=[{"visible": [False, False, False, True, False, False]}]),
                    dict(label="2018",
                        method="update",
                        args=[{"visible": [False, False, False, False, True, False]}]),
                    dict(label="2017",
                        method="update",
                        args=[{"visible": [False, False, False, False, False, True]}]),
                ]),
            )

        ])


    fig2.update_layout(template='plotly_dark', height = 600,)
        #legend_title="Legend Title",

    fig2.update_traces(textposition = "outside")
    
    #fig2.show()


    # In[11]:


    #Graph-3: BUBBLE CHART COMMENTS (MOST NUMBER OF COMMENTS BASED ON AUTHORS & CATEGORIES) // 
    pd_df_bubble_comments_overall = files_dict['bubble_comments']['0']
    pd_df_bubble_comments_2021 = files_dict['bubble_comments']['1']
    pd_df_bubble_comments_2020 = files_dict['bubble_comments']['2']
    pd_df_bubble_comments_2019 = files_dict['bubble_comments']['3']
    pd_df_bubble_comments_2018 = files_dict['bubble_comments']['4']
    pd_df_bubble_comments_2017 = files_dict['bubble_comments']['5']


    pd_df_bubble_comments_overall = pd_df_bubble_comments_overall.iloc[:25]
    pd_df_bubble_comments_2021 = pd_df_bubble_comments_2021.iloc[:25]
    pd_df_bubble_comments_2020 = pd_df_bubble_comments_2020.iloc[:25]
    pd_df_bubble_comments_2019 = pd_df_bubble_comments_2019.iloc[:25]
    pd_df_bubble_comments_2018 = pd_df_bubble_comments_2018.iloc[:25]
    pd_df_bubble_comments_2017 = pd_df_bubble_comments_2017.iloc[:25]


    # In[12]:


    #Graph-3: BUBBLE CHART COMMENTS (MOST NUMBER OF COMMENTS BASED ON AUTHORS & CATEGORIES)

    fig3 = go.Figure(data=[go.Scatter(
        name='Overall',
        x=pd_df_bubble_comments_overall['author'],
        y=pd_df_bubble_comments_overall['section_name'],
        mode='markers',
        hovertext=pd_df_bubble_comments_overall['avg_comments'],
        marker=dict(
            size = pd_df_bubble_comments_overall['avg_comments'],
            showscale=True,
            sizemode='area',
            sizeref=pd_df_bubble_comments_overall['avg_comments'].max() / 40 ** 2,
            color=pd_df_bubble_comments_overall['avg_comments'],
            colorscale=px.colors.sequential.Tealgrn
        )
    ),

    go.Scatter(
        name='2021',
        x=pd_df_bubble_comments_2021['author'],
        y=pd_df_bubble_comments_2021['section_name'],
        mode='markers', visible=False,
        hovertext=pd_df_bubble_comments_2021['avg_comments'],
        marker=dict(
            size = pd_df_bubble_comments_2021['avg_comments'],
            showscale=True,
            sizemode='area',
            sizeref=pd_df_bubble_comments_2021['avg_comments'].max() / 40 ** 2,
            color=pd_df_bubble_comments_2021['avg_comments'],
            colorscale=px.colors.sequential.Tealgrn
        )
    ),
    go.Scatter(
        name='2020',
        x=pd_df_bubble_comments_2020['author'],
        y=pd_df_bubble_comments_2020['section_name'],
        mode='markers', visible=False,
        hovertext=pd_df_bubble_comments_2020['avg_comments'],
        marker=dict(
            size = pd_df_bubble_comments_2020['avg_comments'],
            showscale=True,
            sizemode='area',
            sizeref=pd_df_bubble_comments_2020['avg_comments'].max() / 40 ** 2,
            color=pd_df_bubble_comments_2020['avg_comments'],
            colorscale=px.colors.sequential.Tealgrn
        )
    ),
    go.Scatter(
        name='2019',
        x=pd_df_bubble_comments_2019['author'],
        y=pd_df_bubble_comments_2019['section_name'],
        mode='markers', visible=False,
        hovertext=pd_df_bubble_comments_2019['avg_comments'],
        marker=dict(
            size = pd_df_bubble_comments_2019['avg_comments'],
            showscale=True,
            sizemode='area',
            sizeref=pd_df_bubble_comments_2019['avg_comments'].max() / 40 ** 2,
            color=pd_df_bubble_comments_2019['avg_comments'],
            colorscale=px.colors.sequential.Tealgrn
        )
    ),
    go.Scatter(
        name='2018',
        x=pd_df_bubble_comments_2018['author'],
        y=pd_df_bubble_comments_2018['section_name'],
        mode='markers', visible=False,
        hovertext=pd_df_bubble_comments_2018['avg_comments'],
        marker=dict(
            size = pd_df_bubble_comments_2018['avg_comments'],
            showscale=True,
            sizemode='area',
            sizeref=pd_df_bubble_comments_2018['avg_comments'].max() / 40 ** 2,
            color=pd_df_bubble_comments_2018['avg_comments'],
            colorscale=px.colors.sequential.Tealgrn
        )
    ),
    go.Scatter(
        name='2017',
        x=pd_df_bubble_comments_2017['author'],
        y=pd_df_bubble_comments_2017['section_name'],
        mode='markers', visible=False,
        hovertext=pd_df_bubble_comments_2017['avg_comments'],
        marker=dict(
            size = pd_df_bubble_comments_2017['avg_comments'],
            showscale=True,
            sizemode='area',
            sizeref=pd_df_bubble_comments_2017['avg_comments'].max() / 40 ** 2,
            color=pd_df_bubble_comments_2017['avg_comments'],
            colorscale=px.colors.sequential.Tealgrn
        )

    ),                       
    ])

    # Add dropdown
    fig3.update_layout(
        updatemenus=[ 
            dict(
                direction='down',
                showactive= True,
                active=0,
                x=0.1, y = 1.13,
                buttons=list([
                    dict(label="Overall",
                        method="restyle",
                        args=[{"visible": [True, False, False, False, False, False]}]),
                    dict(label="2021",
                        method="restyle",
                        args=[{"visible": [False, True, False, False, False, False]}
                            ]),
                    dict(label="2020",
                        method="restyle",
                        args=[{"visible": [False, False, True, False, False, False]}]),
                    dict(label="2019",
                        method="restyle",
                        args=[{"visible": [False, False, False, True, False, False]}]),
                    dict(label="2018",
                        method="restyle",
                        args=[{"visible": [False, False, False, False, True, False]}]),
                    dict(label="2017",
                        method="restyle",
                        args=[{"visible": [False, False, False, False, False, True]}]),
                ]),
            )

        ])
        
    fig3.update_layout(xaxis_title="Authors",yaxis_title="Categories",title_x=0.5,title_y=0.95, template='plotly_dark', height=600,)

    #fig3.show()


    # In[13]:


    #Graph-4: TOP 5 PUBLISHING AUTHORS - BY YEAR
    df_author_count_overall = files_dict['author_count']['0']
    df_author_count_2021 = files_dict['author_count']['1']
    df_author_count_2020 = files_dict['author_count']['2']
    df_author_count_2019 = files_dict['author_count']['3']
    df_author_count_2018 = files_dict['author_count']['4']
    df_author_count_2017 = files_dict['author_count']['5']

    df_author_count_overall = df_author_count_overall.iloc[::-1]
    df_author_count_2021 = df_author_count_2021.iloc[::-1]
    df_author_count_2020 = df_author_count_2020.iloc[::-1]
    df_author_count_2019 = df_author_count_2019.iloc[::-1]
    df_author_count_2018 = df_author_count_2018.iloc[::-1]
    df_author_count_2017 = df_author_count_2017.iloc[::-1]


    # In[14]:


    #Graph - 4 TOP 5 PUBLISHING AUTHORS - BY YEAR

    fig4 = go.Figure(data=[go.Bar(
        name='Overall',
        x=df_author_count_overall['count'],
        y=df_author_count_overall['author'],
        marker_color=df_author_count_overall['count'],text=df_author_count_overall['count'],orientation = 'h',
        marker_colorscale = px.colors.sequential.Sunsetdark,
    ),
        go.Bar(
        name='2021',
        x=df_author_count_2021['count'],
        y=df_author_count_2021['author'],
        marker_color=df_author_count_2021['count'],text=df_author_count_2021['count'],orientation = 'h',
        marker_colorscale = px.colors.sequential.Sunsetdark,visible=False,
    ),
        go.Bar(
        name='2020',
        x=df_author_count_2020['count'],
        y=df_author_count_2020['author'],
        marker_color=df_author_count_2020['count'],text = df_author_count_2020['count'],orientation = 'h',
        marker_colorscale = px.colors.sequential.Sunsetdark,visible=False,
    ),  
        go.Bar(
        name='2019',
        x=df_author_count_2019['count'],
        y=df_author_count_2019['author'],
        marker_color=df_author_count_2019['count'],text = df_author_count_2019['count'],orientation = 'h',
        marker_colorscale = px.colors.sequential.Sunsetdark,visible=False,
    ),  
    
        go.Bar(
        name='2018',
        x=df_author_count_2018['count'],
        y=df_author_count_2018['author'],
        marker_color=df_author_count_2018['count'],text = df_author_count_2018['count'],orientation = 'h',
        marker_colorscale = px.colors.sequential.Sunsetdark,visible=False,
    ), 

        go.Bar(
        name='2017',
        x=df_author_count_2017['count'],
        y=df_author_count_2017['author'],
        marker_color=df_author_count_2017['count'],text = df_author_count_2017['count'],orientation = 'h',
        marker_colorscale = px.colors.sequential.Sunsetdark,visible=False,
    )]) 
                        
    # Add dropdown
    fig4.update_layout(
        updatemenus=[ 
            dict(
                direction='down',
                showactive= True,
                active=0,
                x=0.1, y = 1.13,
                buttons=list([
                    dict(label="Overall",
                        method="restyle",
                        args=[{"visible": [True, False, False, False, False, False]}]),
                    dict(label="2021",
                        method="restyle",
                        args=[{"visible": [False, True, False, False, False, False]}
                            ]),
                    dict(label="2020",
                        method="restyle",
                        args=[{"visible": [False, False, True, False, False, False]}]),
                    dict(label="2019",
                        method="restyle",
                        args=[{"visible": [False, False, False, True, False, False]}]),
                    dict(label="2018",
                        method="restyle",
                        args=[{"visible": [False, False, False, False, True, False]}]),
                    dict(label="2017",
                        method="restyle",
                        args=[{"visible": [False, False, False, False, False, True]}]),
                ]),
            )

        ])

    fig4.update_layout(
        #title_text='TOP 5 PUBLISHING AUTHORS - BY YEAR', title_x=0.4,title_y=0.88,
        xaxis_title="Number of Articles",
        yaxis_title="Author",
        height=600,
        template='plotly_dark',
        xaxis=dict(showspikes=True, linecolor="#FFFFFF",
            spikethickness=2,
            spikedash="dash",
            spikecolor="#EEEEEE",
            spikemode="across",
        )
    )


    fig4.update_traces(textposition = "outside")#, template='plotly_dark')
    
    #fig4.show()


    # In[15]:


    #Graph - 5: TOP COUNTRY MENTIONS
    df_covid_country_line_2021 = files_dict['covid_country_line_chart']['1']
    df_covid_country_line_2020 = files_dict['covid_country_line_chart']['0']
    df_covid_country_line_2021 = df_covid_country_line_2021.rename(columns={"sum(india)": "india", "sum(germany)": "germany", "sum(uk)": "uk", "sum(us)":"us", "sum(russia)":"russia","sum(italy)":"italy","sum(canada)":"canada","sum(china)":"china", "sum(japan)":"japan", "sum(france)":"france"})
    df_covid_country_line_2020 = df_covid_country_line_2020.rename(columns={"sum(india)": "india", "sum(germany)": "germany", "sum(uk)": "uk", "sum(us)":"us", "sum(russia)":"russia","sum(italy)":"italy","sum(canada)":"canada","sum(china)":"china", "sum(japan)":"japan", "sum(france)":"france"})


    # In[16]:


    df_covid_country_line_2021 = df_covid_country_line_2021.sort_values(['month'])
    df_covid_country_line_2020 = df_covid_country_line_2020.sort_values(['month'])


    # In[17]:


    import calendar
    df_covid_country_line_2021['month'] = df_covid_country_line_2021['month'].apply(lambda x: calendar.month_abbr[x])
    df_covid_country_line_2020['month'] = df_covid_country_line_2020['month'].apply(lambda x: calendar.month_abbr[x])


    # In[19]:


    fig5 = go.Figure(data=[
        go.Scatter(
        name='India',
        x=df_covid_country_line_2021['month'],
        y=df_covid_country_line_2021['india'],
        ),
        go.Scatter(
        name='China',
        x=df_covid_country_line_2021['month'],
        y=df_covid_country_line_2021['china'],
        ),
        go.Scatter(
        name='Canada',
        x=df_covid_country_line_2021['month'],
        y=df_covid_country_line_2021['canada'],
        ),
        go.Scatter(
        name='USA',
        x=df_covid_country_line_2021['month'],
        y=df_covid_country_line_2021['us'],
        ),
        go.Scatter(
        name='UK',
        x=df_covid_country_line_2021['month'],
        y=df_covid_country_line_2021['uk'],
        ),
         go.Scatter(
        name='Italy',
        x=df_covid_country_line_2021['month'],
        y=df_covid_country_line_2021['italy'],
        ),
        go.Scatter(
        name='India',
        x=df_covid_country_line_2020['month'],
        y=df_covid_country_line_2020['india'],
            visible=False,
        ),
        go.Scatter(
        name='China',
        x=df_covid_country_line_2020['month'],
        y=df_covid_country_line_2020['china'],
            visible=False,
        ),
        go.Scatter(
        name='Canada',
        x=df_covid_country_line_2020['month'],
        y=df_covid_country_line_2020['canada'],
            visible=False,
        ),
        go.Scatter(
        name='USA',
        x=df_covid_country_line_2020['month'],
        y=df_covid_country_line_2020['us'],
            visible=False,
        ),
        go.Scatter(
        name='UK',
        x=df_covid_country_line_2020['month'],
        y=df_covid_country_line_2020['uk'],
            visible=False,
        ),
        go.Scatter(
        name='Italy',
        x=df_covid_country_line_2020['month'],
        y=df_covid_country_line_2020['italy'],
        visible=False,
        ),
        
    ])


    # Add dropdown
    fig5.update_layout(
        updatemenus=[ 
            dict(
                direction='down',
                showactive= True,
                active=0,
                x=0.1, y = 1.13,
                buttons=list([
                    dict(label="2021",
                        method="restyle",
                        args=[{"visible": [True, True, True, True, True,True, False,False,False,False,False,False ]}]),
                    dict(label="2020",
                        method="restyle",
                        args=[{"visible": [False, False, False, False, False,False, True, True, True, True, True,True]}
                            ])]))])


    fig5.update_layout(
        #title_text='COVID MENTIONS BASED ON COUNTRY', title_x=0.4,title_y=0.88,
        xaxis_title="Months",
        yaxis_title="Mentions",
        height=600,
        template='plotly_dark',
        )



    #fig5.show()


    # In[20]:


    #Graph - 6: EMOTIONS
    df_emotions = files_dict['emotions']
    df_emotions = df_emotions.sort_values(by = ['year'])
    df_emotions = df_emotions.rename(columns={"sum(emotion)": "emotion", "sum(query)": "query", "sum(excitement)": "excitement", "sum(confusion)":"confusion"})


    # In[21]:


    #Graph - 6: EMOTIONS MENTIONS

    fig6 = go.Figure(data=[
        go.Bar(
        name='Excitement',
        x=df_emotions['year'],
        y=df_emotions['excitement'],
        text=df_emotions['excitement'],
    ),
        go.Bar(
        name='Confusion',
        x=df_emotions['year'],
        y=df_emotions['confusion'],
        text=df_emotions['confusion'],
    )])

    fig6.update_layout(barmode='group',height=600,
                    template='plotly_dark',
                    xaxis_title='Sentiments',yaxis_title='Instances',
                    #title_text='JUST GIVE IT A NAME', title_x=0.5,
                    yaxis=dict(showspikes=True, linecolor="#FFFFFF", 
                    spikethickness=2,
                    spikedash="dash",
                    spikecolor="#EEEEEE",
                    spikemode="across",
        ))

    fig6.update_traces(textposition='outside')

    #fig6.show()


    # In[22]:


    # GRAPH 7: bubble_recommendations/

    df_author_engagement_overall = files_dict['bubble_recommendations']['0']
    df_author_engagement_2021 = files_dict['bubble_recommendations']['1']
    df_author_engagement_2020 = files_dict['bubble_recommendations']['2']
    df_author_engagement_2019 = files_dict['bubble_recommendations']['3']
    df_author_engagement_2018 = files_dict['bubble_recommendations']['4']
    df_author_engagement_2017 = files_dict['bubble_recommendations']['5']


    df_author_engagement_overall = df_author_engagement_overall.iloc[:25]
    df_author_engagement_2021 = df_author_engagement_2021.iloc[:25]
    df_author_engagement_2020 = df_author_engagement_2020.iloc[:25]
    df_author_engagement_2019 = df_author_engagement_2019.iloc[:25]
    df_author_engagement_2018 = df_author_engagement_2018.iloc[:25]
    df_author_engagement_2017 = df_author_engagement_2017.iloc[:25]


    # In[23]:


    df_author_engagement_overall.head()


    # In[24]:


    #Plotting

    fig7 = go.Figure(data=[
        go.Scatter(
        name='Overall',
        x=df_author_engagement_overall['author'],
        y=df_author_engagement_overall['section_name'],
        mode='markers', #visible=False,
        hovertext=df_author_engagement_overall['avg_recommendations'],
        marker=dict(
            size = df_author_engagement_overall['avg_recommendations'],
            showscale=True,
            sizemode='area',
            sizeref=df_author_engagement_overall['avg_recommendations'].max() / 40 ** 2,
            color=df_author_engagement_overall['avg_recommendations'],
            colorscale=px.colors.sequential.Oryel
        )
    ), 
        go.Scatter(
        name='2021',
        x=df_author_engagement_2021['author'],
        y=df_author_engagement_2021['section_name'],
        mode='markers', visible=False,
        hovertext=df_author_engagement_2021['avg_recommendations'],
        marker=dict(
            size = df_author_engagement_2021['avg_recommendations'],
            showscale=True,
            sizemode='area',
            sizeref=df_author_engagement_overall['avg_recommendations'].max() / 40 ** 2,
            color=df_author_engagement_overall['avg_recommendations'],
            colorscale=px.colors.sequential.Oryel
        )
    ),
        
        go.Scatter(
        name='2020',
        x=df_author_engagement_2020['author'],
        y=df_author_engagement_2020['section_name'],
        mode='markers', visible=False,
        hovertext=df_author_engagement_2020['avg_recommendations'],
        marker=dict(
            size = df_author_engagement_2020['avg_recommendations'],
            showscale=True,
            sizemode='area',
            sizeref=df_author_engagement_2020['avg_recommendations'].max() / 40 ** 2,
            color=df_author_engagement_2020['avg_recommendations'],
            colorscale=px.colors.sequential.Oryel
        )
    ),
    
        go.Scatter(
        name='2019',
        x=df_author_engagement_2019['author'],
        y=df_author_engagement_2019['section_name'],
        mode='markers', visible=False,
        hovertext=df_author_engagement_2019['avg_recommendations'],
        marker=dict(
            size = df_author_engagement_2019['avg_recommendations'],
            showscale=True,
            sizemode='area',
            sizeref=df_author_engagement_2019['avg_recommendations'].max() / 40 ** 2,
            color=df_author_engagement_2019['avg_recommendations'],
            colorscale=px.colors.sequential.Oryel
        )
    ),
        
        go.Scatter(
        name='2018',
        x=df_author_engagement_2018['author'],
        y=df_author_engagement_2018['section_name'],
        mode='markers', visible=False,
        hovertext=df_author_engagement_2018['avg_recommendations'],
        marker=dict(
            size = df_author_engagement_2018['avg_recommendations'],
            showscale=True,
            sizemode='area',
            sizeref=df_author_engagement_2018['avg_recommendations'].max() / 40 ** 2,
            color=df_author_engagement_2018['avg_recommendations'],
            colorscale=px.colors.sequential.Oryel
        )
    ), 

        go.Scatter(
        name='2017',
        x=df_author_engagement_2017['author'],
        y=df_author_engagement_2017['section_name'],
        mode='markers', visible=False,
        hovertext=df_author_engagement_2017['avg_recommendations'],
        marker=dict(
            size = df_author_engagement_2017['avg_recommendations'],
            showscale=True,
            sizemode='area',
            sizeref=df_author_engagement_2017['avg_recommendations'].max() / 40 ** 2,
            color=df_author_engagement_2017['avg_recommendations'],
            colorscale=px.colors.sequential.Oryel
        )
    ), 
                                            
    ])
                                            

    # Add dropdown
    fig7.update_layout(
        updatemenus=[ 
            dict(
                direction='down',
                showactive= True,
                active=0,
                x=0.1, y = 1.13,
                buttons=list([
                    dict(label="Overall",
                        method="restyle",
                        args=[{"visible": [True, False, False, False, False, False]}]),
                    dict(label="2021",
                        method="restyle",
                        args=[{"visible": [False, True, False, False, False, False]}
                            ]),
                    dict(label="2020",
                        method="restyle",
                        args=[{"visible": [False, False, True, False, False, False]}]),
                    dict(label="2019",
                        method="restyle",
                        args=[{"visible": [False, False, False, True, False, False]}]),
                    dict(label="2018",
                        method="restyle",
                        args=[{"visible": [False, False, False, False, True, False]}]),
                    dict(label="2017",
                        method="restyle",
                        args=[{"visible": [False, False, False, False, False, True]}]),
                ]),
            )

        ])
        
    fig7.update_layout(#title_text='MOST ENGAGEMENT BASED ON AUTHORS & CATEGORIES',
        xaxis_title="Authors",yaxis_title="Categories",title_x=0.5, template='plotly_dark', height =600,)

    #fig7.show()


    # In[25]:


    #Graph - 8: USA MAP

    df_userlocation_2021 = files_dict['heatmap_usa']['0']
    df_userlocation_2020 = files_dict['heatmap_usa']['1']
    df_userlocation_2019 = files_dict['heatmap_usa']['2']
    df_userlocation_2018 = files_dict['heatmap_usa']['3']
    df_userlocation_2017 = files_dict['heatmap_usa']['4']


    # In[26]:


    df_userlocation_2021 = df_userlocation_2021.rename(columns={"correct_userlocation": "location","count(correct_userlocation)":"count" })
    df_userlocation_2020 = df_userlocation_2020.rename(columns={"correct_userlocation": "location","count(correct_userlocation)":"count" })
    df_userlocation_2019 = df_userlocation_2019.rename(columns={"correct_userlocation": "location","count(correct_userlocation)":"count" })
    df_userlocation_2018 = df_userlocation_2018.rename(columns={"correct_userlocation": "location","count(correct_userlocation)":"count" })
    df_userlocation_2017 = df_userlocation_2017.rename(columns={"correct_userlocation": "location","count(correct_userlocation)":"count" })


    # In[47]:


    fig8 = go.Figure(data=[
        go.Choropleth(
        locations= df_userlocation_2021['location'], # Spatial coordinates
        text = 'Commenters',
        z = df_userlocation_2021['count'], # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale=px.colors.sequential.Agsunset,
        reversescale=True,
        colorbar_title = "Count",
    ),
        go.Choropleth(
        locations= df_userlocation_2020['location'], # Spatial coordinates
        text = 'Commenters',
        z = df_userlocation_2020['count'], # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale=px.colors.sequential.Agsunset,
        reversescale=True,visible=False,
        colorbar_title = "Count",
    ),
        go.Choropleth(
        locations= df_userlocation_2019['location'], # Spatial coordinates
        text = 'Commenters',
        z = df_userlocation_2019['count'], # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale=px.colors.sequential.Agsunset,
        reversescale=True,visible=False,
        colorbar_title = "Count",
    ),
        go.Choropleth(
        locations= df_userlocation_2018['location'], # Spatial coordinates
        text = 'Commenters',
        z = df_userlocation_2018['count'], # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale=px.colors.sequential.Agsunset,
        reversescale=True,visible=False,
        colorbar_title = "Count",
    ),
        go.Choropleth(
        locations= df_userlocation_2017['location'], # Spatial coordinates
        text = 'Commenters',
        z = df_userlocation_2017['count'], # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale=px.colors.sequential.Agsunset,
        reversescale=True,visible=False,
        colorbar_title = "Count",
            
        
    )])

    fig8.add_scattergeo(
        locations=df_userlocation_2021['location'],    ###codes for states,
        locationmode='USA-states',
        text=df_userlocation_2021['location'],
        hoverinfo='skip',
        textfont_color='#000000',
        textfont_size=8,
        mode='text')

    # Add dropdown
    fig8.update_layout(
        updatemenus=[ 
            dict(
                direction='down',
                showactive= True,
                #active=0,
                x=0.1, y = 1,
                buttons=list([
                    dict(label="2021",
                        method="restyle",
                        args=[{"visible": [True, False, False, False, False, True]},
                            ]),
                    dict(label="2020",
                        method="restyle",
                        args=[{"visible": [False, True, False, False, False, True]}]),
                    dict(label="2019",
                        method="restyle",
                        args=[{"visible": [False, False, True, False, False, True]}]),
                    dict(label="2018",
                        method="restyle",
                        args=[{"visible": [False, False, False, True, False, True]}]),
                    dict(label="2017",
                        method="restyle",
                        args=[{"visible": [False, False, False, False, True, True]}])
                ])
            )

        ])

    fig8.update_layout(
        #title_text = 'LOCATION OF COMMENTERS',title_x=0.5,
        geo_scope='usa', # limite map scope to USA
        template='plotly_dark',height=600,
    )

    #fig8.show()
    #figs = [fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8]
    figs = [fig8, fig4, fig2, fig1, fig3, fig7, fig5, fig6]
    return figs