import folium
import pandas

map = folium.Map(location=[34.07250424561512, -118.27718161498242], zoom_start=6, tiles = "Stamen Terrain")

data = pandas.read_csv("Volcanoes.txt")
lon = list(data["LON"])
lat = list(data["LAT"])
elev = list(data["ELEV"])
name = list(data["NAME"])
location = list(data["LOCATION"])
status = list(data["STATUS"])

def color_prod(elevation):
    if elevation<1000:
        return 'green'
    elif 1000<=elevation<3000:
        return 'orange'
    else:
        return 'red'


html ="""<h4> Volcano Information: </h4> Name: %s Location: %s Height: %s m <br> Status: %s<br>  """

fgv = folium.FeatureGroup(name= "Volcanoes")

for lt,ln,elev,nm,lon,st in zip(lat,lon,elev,name,location,status):
    iframe = folium.IFrame(html = html % (nm,lon, str(elev), st), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt,ln], radius= 6, popup=folium.Popup(iframe) , fill_color=color_prod(elev),color='gray',fill=True ,fill_opacity = 1))

fgp = folium.FeatureGroup(name= "Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
        style_function=lambda x: {'fillColor': 'yellow' if x["properties"]["POP2005"] < 10000000
        else "orange" if 10000000 <= x["properties"]["POP2005"] < 20000000
        else "red" }))


map.add_child(fgp)
map.add_child(fgv)
map.add_child(folium.LayerControl())
map.save("Map.html")