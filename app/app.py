from flask import Flask, render_template, request
from restcountries import RestCountryApiV2 as rapi
import requests

# Configura la app Flask
app = Flask(__name__)

# Tu API Key para ExchangeRates
API_KEY = "10be7bf61eb85c404164413a6fc888c7"
BASE_URL = "http://api.exchangeratesapi.io/v1/"

# Función para obtener datos de un país
def obtener_datos_pais(nombre_pais):
    try:
        country_list = rapi.get_countries_by_name(nombre_pais)
        if country_list:
            return country_list[0]
    except requests.exceptions.InvalidURL:
        return None
    except requests.exceptions.RequestException as e:
        return None

# Función para obtener la tasa de cambio
def obtener_tasa_de_cambio(currency_code):
    try:
        endpoint = f"{BASE_URL}latest"
        params = {
            "access_key": API_KEY,
            "symbols": currency_code
        }
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            datos = response.json()
            return datos['rates'].get(currency_code, "No disponible")
        else:
            return "No disponible"
    except requests.exceptions.RequestException as e:
        return "No disponible"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pais1 = request.form["pais1"]
        pais2 = request.form["pais2"]
        datos_pais1 = obtener_datos_pais(pais1)
        datos_pais2 = obtener_datos_pais(pais2)
        if datos_pais1 and datos_pais2:
            tasa_cambio_pais1 = obtener_tasa_de_cambio(datos_pais1.currencies[0]['code'])
            tasa_cambio_pais2 = obtener_tasa_de_cambio(datos_pais2.currencies[0]['code'])
            data = [
                ["Nombre", datos_pais1.name, datos_pais2.name],
                ["Nombre nativo", datos_pais1.native_name, datos_pais2.native_name],
                ["Dominio de nivel superior", ', '.join(datos_pais1.top_level_domain), ', '.join(datos_pais2.top_level_domain)],
                ["Código alpha-2", datos_pais1.alpha2_code, datos_pais2.alpha2_code],
                ["Código alpha-3", datos_pais1.alpha3_code, datos_pais2.alpha3_code],
                ["Capital", datos_pais1.capital, datos_pais2.capital],
                ["Código de llamada", ', '.join(datos_pais1.calling_codes), ', '.join(datos_pais2.calling_codes)],
                ["Variantes del nombre", ', '.join(datos_pais1.alt_spellings), ', '.join(datos_pais2.alt_spellings)],
                ["Región", datos_pais1.region, datos_pais2.region],
                ["Subregión", datos_pais1.subregion, datos_pais2.subregion],
                ["Población", datos_pais1.population, datos_pais2.population],
                ["Área (km²)", datos_pais1.area, datos_pais2.area],
                ["Gini", datos_pais1.gini, datos_pais2.gini],
                ["Idiomas", ', '.join([lang['name'] for lang in datos_pais1.languages]), ', '.join([lang['name'] for lang in datos_pais2.languages])],
                ["Monedas", ', '.join([currency['name'] for currency in datos_pais1.currencies]), ', '.join([currency['name'] for currency in datos_pais2.currencies])],
                ["Currency Value €", tasa_cambio_pais1, tasa_cambio_pais2],
                ["Bandera", f'<img src="{datos_pais1.flag}" alt="Bandera de {datos_pais1.name}" width="100">', 
                f'<img src="{datos_pais2.flag}" alt="Bandera de {datos_pais2.name}" width="100">'],
                ["Bloques regionales", ', '.join([bloc['name'] for bloc in datos_pais1.regional_blocs]) if datos_pais1.regional_blocs else "N/A",
                 ', '.join([bloc['name'] for bloc in datos_pais2.regional_blocs]) if datos_pais2.regional_blocs else "N/A"]
            ]
            return render_template("index.html", data=data, pais1=pais1, pais2=pais2)
        else:
            error = "No se pudieron obtener los datos de uno o ambos países."
            return render_template("index.html", error=error)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
