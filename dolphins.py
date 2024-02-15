import plotly.offline as pyo
import branca
from dash import dash, dcc,html
from xyzservices.lib import TileProvider
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from dash import Dash
import datetime
import plotly.express as px
import folium
from folium.plugins import MarkerCluster,BeautifyIcon
# ovo je primer pocetak*****************
import numpy as np
import plotly.subplots as sp



barCODTableA = pd.read_csv('barCODTableA.csv')
barCODTableB = pd.read_csv('barCODTableB.csv')
byCenterGraphData = pd.read_csv('speciesByCenter.csv')
dataMap  = pd.read_csv('dashTable.csv')
dataFolium = pd.read_csv('foliumPopUp.csv')
# labels = ['code']

generalData =pd.read_csv('dropdownDate.csv',encoding='latin1',parse_dates=['originDate','entryDate','statusDate'])
dateBeg =generalData.loc[~generalData['birthYear'].isna()]

boolValue = dateBeg !=-2147483648
dateBeg =dateBeg[boolValue]





# dateBeg =dateBeg.birthYear.unique()



# PROBA
dateBeg.loc[dateBeg.birthYear=='1990s','birthYear'] = 1990
dateBeg.birthYear =dateBeg.birthYear.astype('int64',errors='raise')

listDates5 = []
for x in dateBeg.birthYear.unique():
    if x % 5==0:
        listDates5.append(x)

firstDate = []
secondDate = []
for x in sorted(listDates5):
    if x % 2!=0:
        secondDate.append(str(x))
        
for x in sorted(listDates5):
    if x % 2==0:
        firstDate.append(str(x))
        
secondDate.insert(1,'1955')    

    
listStringBoth = []    
for s in zip(firstDate,secondDate):
    string = s[0]+ '-' + s[1]
    listStringBoth.append(string)


# for n,s in enumerate(resJ3):
#     if n % 8==0: 
#       print(s)


    












dataMap.drop(columns='Unnamed: 0',inplace=True)
byCenterGraphData.drop(columns='Unnamed: 0',inplace=True)


# ***********FOLIUM***************
tableDashLocations = pd.read_csv('tableDashLocations.csv',index_col=False)
provider = TileProvider.from_qms("Google Maps (Alternative rendering)")
m = folium.Map(location=[37.8283, -97.5795],zoom_start=4,tiles=provider,attr='ff')
line_group = folium.FeatureGroup()
icon_image_path = 'delfinSlicica.png'
for row in dataFolium.iterrows():
      
      htmlConvert=f"""
       
           <div style='margin-top:0px; padding:0px;text-align:center;'>
    
        
                  <ul style='list-style-type:none;inline-block;text-align:center; padding-left: 0;'>
                      <li>Center name:{row[1].iloc[0]}</li>
                      <li>Average year:{round(row[1].iloc[1],2)}</li>
                      <li>Backcross:{row[1].iloc[4]}</li>
                      <li>Beluga:{row[1].iloc[5]}</li>
                      <li>Bottlenose:{row[1].iloc[6]}</li>
                      <li>Commerson 's:{row[1].iloc[7]}</li>
                      <li>Hybrid:{row[1].iloc[8]}</li>
                      <li>Killer Whale; Orca:{row[1].iloc[9]}</li>
                      <li>Pilot, Short-fin:{row[1].iloc[10]}</li>
                      <li>Rough-toothed:{row[1].iloc[11]}</li>
                      <li>Spotted, Atlantic:{row[1].iloc[12]}</li>
                      <li>White-sided, Pacific:{row[1].iloc[13]}</li>
                      <li>Number in center:{row[1].iloc[14]}</li>
                      
                  </ul>
           </div>
        
     
          """
      iframe = folium.IFrame(html=htmlConvert, width=250, height=250)
      popup = folium.Popup(iframe,max_width=256)
      custom_icon = folium.CustomIcon(
                  icon_image_path,
                  icon_size=(50, 75),  # Set the size of your custom icon
                  # icon_anchor=(anchor_x, anchor_y)  # Set the anchor point (relative to the top-left corner)
        )
      
#  <i class="fa-solid fa-fish-fins"></i>
      folium.Marker(
                        
                        location=[row[1].iloc[2],row[1].iloc[3]],
                        icon=custom_icon,
                        popup=popup,
                        # icon=folium.plugins.BeautifyIcon(icon="fish-fins",
                        #                                 icon_shape='circle',
                        #                                 radius=10,                        
                        #                                 background_color='#40C4FF',
                        #                                 # inner_icon_style='font-size:30px;',
                                                        
                        #                                 border_color='black',
                        #                       )

        ).add_to(m)
        

line_group.add_to(m)

m.save("map.html")


app = Dash(__name__)
server = app.server


colorscale2= [
'#ffffe5',
'#f7fcb9',
'#d9f0a3',
'#addd8e',
'#78c679',
'#41ab5d',
'#238443',
'#006837',
'#004529'
]



colors_red = [
'#a6cee3',
'#1f78b4',
'#b2df8a',
'#33a02c',
'#fb9a99',
'#e31a1c',
'#fdbf6f',
'#ff7f00',
'#cab2d6'
]

# fig = px.choropleth( 
#   dataMap,
#   color_continuous_scale=colorscale2,
#   # color_continuous_scale=px.colors.sequential.Plasma,
#   fitbounds='locations',
#   locationmode="USA-states",
#   locations=dataMap['code'],color=dataMap['allDol'],
#   hover_data=['states'],
#   labels={'states':'States','allDol':'in center'},
  
#   )


# colors_red.reverse()
fig2 = px.bar(byCenterGraphData, x=byCenterGraphData["currently"], y=byCenterGraphData["spec"], color=byCenterGraphData["species"], title="Dolphins and whales in Centers by species",color_discrete_sequence=colors_red)
fig3 = px.bar(
    
    
    barCODTableA, x=barCODTableA["COD"], y=barCODTableA["Bottlenose"],color_continuous_scale='#01caf1', title="Most common death by diseases to  from 1952 to 1984",
    
    labels={
                    "COD": "Cause of death",
                    "Bottlenose": "died",
                    
                },
    )
fig4 = px.bar(
    barCODTableB, x=barCODTableB["COD"], y=barCODTableB["Bottlenose"],color_continuous_scale='#01caf1', title="Most common death by diseases from 1984 to 2016",
    labels={
                    "COD": "Cause of death",
                    "Bottlenose": "died",
                    
                },
    
    
    )
   
    
  # 

app.layout = html.Div([

    html.H1('Dolphins and whales population in captivity US coast from 1938 to 2016 ',style={'margin-top':'4%','margin-left':'4%'}),
    # html.P("Select a candidate:"),
            html.Div([
                html.Div([
                    # dcc.Graph(figure=m._repr_html_(),responsive=True)
                    # dcc.Markdown(html_map),
                    
                    html.Iframe(srcDoc=open("map.html", "r").read(), width="100%", height="600")
                    ],className='grid-item'),
                html.Div([
                    html.P('The graph shows dolphins and whales population living in captivity during last status update(2016) year'
                            ' in the American states acrros USA. Many aquariums and marine parks argue that keeping dolphins and whales in captivity provides an opportunity for education and public awareness about marine life, conservation, and environmental issues. Visitors can learn about these animals up close and develop an appreciation for ocean ecosystems and the need for conservation efforts.'
                            'Dolphins and whales in captivity offer researchers and scientists the opportunity to study these animals in controlled environments. Researchers can study their behavior, physiology, communication, cognition, and other aspects that are difficult to observe in the wild. This research contributes to scientific knowledge about marine mammals and can inform conservation efforts.'
                            'The largest number of dolphins is in the possession of the U.S. navy base. This group of dolphins is trained daily for the needs of the army and emergency situations.Additionally,'
                            ' the Navy also uses marine mammals for tasks such as locating lost equipment and divers, as well as assisting with search and rescue operations. These animals are also capable of detecting intruders and swimmers in restricted areas, which can help enhance the security of Navy installations and other critical infrastructure.')
                   
                    ],className='grid-item',id='foliumStyle'),
                
                
               
                
                ],className='grid-container'),
          
          
              
              
      
          
          ################# Bar graph ################
                html.Div([
                    html.Div([
                        # html.P('The graph shows the current state of the dolphin population living in captivity in the American states acrros USA, which are diffrent in color due to the different number of dolphins in each of those states.The largest number of dolphins is in the possession of the U.S. navy base. This group of dolphins is trained daily for the needs of the army and emergency situations.Additionally, the Navy also uses marine mammals for tasks such as locating lost equipment and divers, as well as assisting with search and rescue operations. These animals are also capable of detecting intruders and swimmers in restricted areas, which can help enhance the security of Navy installations and other critical infrastructure.')
                        dcc.Graph(figure=fig3,responsive=True),
                        dcc.Graph(figure=fig4,responsive=True)
                        ],className='grid-item'),
                  
                    html.Div([
                        
                        
                        # defaultni graph
                        dcc.Graph(id='barMortality'),
                        dcc.Dropdown(
                            id='dateOne',
                            options=[{'label': i, 'value':i} for i in listStringBoth],
                            value=listStringBoth[0],
                            clearable=False,
                            style={'width': '100%', 'color': 'black', 'backgroundColor': 'white', 'fontSize': '22px'}
                      ),
                       #   dcc.Dropdown(
                       #       id='dateTwo',
                       #       options=[{'label':i, 'value': i} for i in sorted(dateBeg)],
                       #       value=max(dateBeg),
                       #       clearable=False,
                       #       style={'width': '100%', 'color': 'black', 'backgroundColor': 'white', 'fontSize': '22px'}
                       # )
                       
                       
                        ],className='grid-item')
                   
                   
                   
                   
                    ],className='grid-container'),
                ################# Bar graph ################
                      html.Div([
                        
                           dcc.Graph(figure=fig2),
                         
                         
                         
                          ],className='grid-container'),
             
                    
              
])
             
             
                   
                
                
            
               
               


# fig.update_layout(
       
#             {
#             'plot_bgcolor': '#000',
#             'paper_bgcolor': '#000',
#           },
            
#             margin=dict(l=60, r=60, t=50, b=50), 
#             # yaxis=dict(
#             #     automargin=True
#             # ),
#             # plot_bgcolor='#000',
#             width=1000,
#             geo = dict(
#             landcolor = '#00b8ea',
#             showland = True,
#             showcountries = True,
#             bgcolor='black',
#             countrywidth = 0.5,),
#             xaxis_tickfont_color='#fff',
#             yaxis_tickfont_color='#fff',
#             font_color='#fff'
#     )

# ################### graph Bar 2 #################


fig2.update_layout(
        {'paper_bgcolor': '#000'},
        margin=dict(l=60, r=60, t=150, b=150),
        height=700,
        title_font=dict(color='#fff'),
        plot_bgcolor='#fff',
        xaxis_tickfont_color='#fff',
        yaxis_tickfont_color='#fff',
        font_color='#fff',
        xaxis_tickangle=45,
      
      )



fig3.update_layout(
        {'paper_bgcolor': '#fff'},
        margin=dict(l=60, r=60, t=150, b=50), 
        height=700,
        title_font=dict(color='black'),
        plot_bgcolor='#fff',
        xaxis_tickfont_color='#000',
        yaxis_tickfont_color='#000',
        font_color='#000'
            
    )
fig4.update_layout(
        {'paper_bgcolor': '#fff'},
        margin=dict(l=60, r=60, t=150, b=50), 
        height=700,
        title_font=dict(color='black'),
        plot_bgcolor='#fff',
        xaxis_tickfont_color='#000',
        yaxis_tickfont_color='#000',
        font_color='#000'
    )
# fig2.update_xaxes(tickangle=90)

# ################### graph Bar 2 end #################
@app.callback(
    Output('barMortality', 'figure'),
    [Input('dateOne', 'value')]
)
def mortality_func(date1):
        date = date1.split('-')
        # global dateValue1,dateValue2
        dateValue1 = date[0]
        dateValue2 = date[1]
        periodData  = generalData.loc[generalData.birthYear.between(dateValue1,dateValue2)]
        maxBirthYear = periodData.birthYear.max()
        DiedPeriod = periodData.loc[~(periodData.statusDate >maxBirthYear)&(~periodData.statusDate.isna())]
        periodLive =  periodData.loc[(periodData.statusDate >maxBirthYear)&(~periodData.statusDate.isna())]
        periodLive.loc[:,'status'] = 'Alive'
        table5 = pd.concat([DiedPeriod,periodLive],axis=0)
        # svrAlive =table5.loc[table5.status=='Alive']
        # svrDied =table5.loc[table5.status=='Died']
        # svrAlive = svrAlive.status.count()
        # svrDied = svrDied.status.count()
        # resSVR=(svrAlive/svrDied)
        fig5Uizradi =px.histogram(table5, x='status')
        fig5Uizradi.update_layout(
                
                {'paper_bgcolor': '#fff'},
                xaxis_tickfont_color='#000',
                yaxis_tickfont_color='#000',
                font_color='#000',
                # title_font=dict(color='#e6f5e6'),
                plot_bgcolor='#fff',
                margin=dict(l=60, r=60, t=150, b=50), 
                height=700,
                # xaxis_title='From {} to {} mortality rate percent:<b>{}</b>'.format(str(date1),str(date2),str(resSVR)),
        )
        # fig5Uizradi = px.bar(DiedPeriod, x=DiedPeriod["originDate"], y=DiedPeriod["status"],  title="Dolphins and whales in Centers by species")
        return fig5Uizradi
       
     

# print(mortality_func('1945-1955'))
if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    


            
    







    
