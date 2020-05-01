#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
np.__version__


# In[2]:


import pandas as pd
pd.__version__


# In[3]:
#crsmex_seq_2020MAR27.out

# location file
loc_fi = "crsmex_seq_2020MAR27.out"


# In[4]:


# read file
df_loc = pd.read_csv(loc_fi,   
                sep=" ",names=["seqid", "lat", "lon", "dep", "mag","eq_num"],header=None)


# In[5]:


import folium
folium.__version__


# In[6]:



m = folium.Map(location=[16.00, -99.0], zoom_start=8.0, tiles='Stamen Terrain') 


#style = {'fillColor': '#00000000', 'color': '#00000000'}
# black
#style = {'fillColor': '#000000', 'color': '#000000'}
# orangered
#ff4500
style = {'fillColor': '#ff4500', 'color': '#ff4500'}


# json file for fault trace
#geojson = r'Fault_Traces.json'
#folium.GeoJson(
#    geojson,
#    name='geojson',
#    style_function=lambda x: style
#).add_to(m)




# plot location with circles
for i in range(len(df_loc)):
    folium.CircleMarker(
        #location=[45.5215, -122.6261],
        location=[df_loc['lat'][i], df_loc['lon'][i]],
        radius=5,
        popup="<b>"+df_loc['seqid'][i]+"</b><br>"+"EQnum: "+str(df_loc['eq_num'][i]) 
        +"<br>"+"Mag: "+str(round(df_loc['mag'][i],2)) 
        +"<br>"+"Latitude: "+str(round(df_loc['lat'][i],4))
        +"<br>"+"Longitude: "+str(round(df_loc['lon'][i],4))
        +"<br>"+"Depth: "+str(round(df_loc['dep'][i],3)),
        color='#3186cc',
        fill=True,
        fill_color='#3186cc'
    ).add_to(m)

    


# In[7]:


# save map in .html file
m.save('CRSMEX_map.html')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




