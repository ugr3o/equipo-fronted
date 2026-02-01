from flask import Flask, render_template
from flask_cors import CORS
import requests
import folium

app = Flask(__name__)
CORS(app) # HABILITAR CORS EN TODAS LAS RUTAS   

# --- CONFIGURACIÓN ---
OCM_API_KEY = 'f10c79d2-e68d-423c-ac00-d318a2845c78'  # Tu key de OpenChargeMap

@app.route('/')
def ver_mapa():

    # Crear mapa centrado en Asunción
    m = folium.Map(location=(-25.2867,-57.6470), zoom_start=10)
    
    # Traer estaciones de carga
    url = "https://api.openchargemap.io/v3/poi/"
    params = {
        "output": "json",
        "countrycode": "PY",
        "distance": 200,
        "distanceunit": "KM",
        "maxresults": 100,
        "compact": False,
        "verbose": False,
        "key": OCM_API_KEY
    }
    headers = {'User-Agent': 'MiAppVehiculosEV/1.0'}

    try:
        response = requests.get(url, params=params, headers=headers)
        estaciones = response.json()

        # Agregar marcadores al mapa
        for e in estaciones:
            if 'AddressInfo' in e:
                lat = e['AddressInfo'].get('Latitude')
                lon = e['AddressInfo'].get('Longitude')
                name = e['AddressInfo'].get('Title', 'Sin nombre')
                if lat and lon:
                    folium.Marker([lat, lon], popup=name).add_to(m)
    except Exception as ex:
        print("Error al traer estaciones:", ex)

    # Convertir a HTML
    mapa_html = m._repr_html_()
    return render_template('index.html', mapa_html=mapa_html)

if __name__ == '__main__':
    print("Arrancando Flask en http://127.0.0.1:5000/")
    app.run(debug=True)