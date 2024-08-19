from restcountries import RestCountryApiV2 as rapi
import requests

def obtener_datos_pais(nombre_pais):
    try:
        country_list = rapi.get_countries_by_name(nombre_pais)
        if country_list:
            return country_list[0]
    except requests.exceptions.InvalidURL:
        print("Se ha producido un error debido a un nombre de país no válido. Por favor, verifica el nombre e inténtalo de nuevo.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Se ha producido un error en la solicitud: {e}")
        return None
