from flask import Flask,request,render_template, jsonify

from flask_cors import CORS
import folium

app = Flask(__name__)
CORS(app) # HABILITAR CORS EN TODAS LAS RUTAS   

m = folium.Map(location=(45.5236, -122.6750))

mapa_html = m._repr_html_()

@app.route("/")
def index():
    return render_template("index.html", mapa_html= mapa_html)
