import requests
import json

GOOGLE_MAPS_API_KEY = "AIzaSyD8oBKEh6DWCrCdOauP9gwG7u55tL28gwk" # Substitua pela sua chave de API real

def geocode_address(address):
    """Converte um endereço em coordenadas geográficas (latitude, longitude)."""
    if not GOOGLE_MAPS_API_KEY or GOOGLE_MAPS_API_KEY == "YOUR_GOOGLE_MAPS_API_KEY":
        print("Erro: Chave de API do Google Maps não configurada.")
        return None, None, None

    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        data = response.json()

        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            place_id = data["results"][0]["place_id"]
            print(f"Endereço 	{address}	 geocodificado para: {location['lat']}, {location['lng']}")
            return location["lat"], location["lng"], place_id
        else:
            print(f"Erro ao geocodificar endereço 	{address}	: {data['status']}")
            return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição ao geocodificar endereço: {e}")
        return None, None, None

def reverse_geocode_coordinates(latitude, longitude):
    """Converte coordenadas geográficas (latitude, longitude) em um endereço legível."""
    if not GOOGLE_MAPS_API_KEY or GOOGLE_MAPS_API_KEY == "YOUR_GOOGLE_MAPS_API_KEY":
        print("Erro: Chave de API do Google Maps não configurada.")
        return None

    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{latitude},{longitude}",
        "key": GOOGLE_MAPS_API_KEY
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        data = response.json()

        if data["status"] == "OK":
            address = data["results"][0]["formatted_address"]
            print(f"Coordenadas ({latitude}, {longitude}) geocodificadas inversamente para: {address}")
            return address
        else:
            print(f"Erro ao geocodificar inversamente coordenadas ({latitude}, {longitude}): {data['status']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição ao geocodificar inversamente coordenadas: {e}")
        return None

def get_place_details(place_id):
    """Obtém detalhes de um local usando a Places API."""
    if not GOOGLE_MAPS_API_KEY or GOOGLE_MAPS_API_KEY == "YOUR_GOOGLE_MAPS_API_KEY":
        print("Erro: Chave de API do Google Maps não configurada.")
        return None

    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": GOOGLE_MAPS_API_KEY
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        data = response.json()

        if data["status"] == "OK":
            print(f"Detalhes do local para Place ID {place_id}: {data['result']['name']}")
            return data["result"]
        else:
            print(f"Erro ao obter detalhes do local para Place ID {place_id}: {data['status']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição ao obter detalhes do local: {e}")
        return None

def snap_to_roads(path_points):
    """Ajusta um conjunto de pontos a estradas usando a Roads API."""
    if not GOOGLE_MAPS_API_KEY or GOOGLE_MAPS_API_KEY == "YOUR_GOOGLE_MAPS_API_KEY":
        print("Erro: Chave de API do Google Maps não configurada.")
        return None

    base_url = "https://roads.googleapis.com/v1/snapToRoads"
    # path_points deve ser uma string de lat,lng|lat,lng|...
    path_string = "|".join([f"{lat},{lng}" for lat, lng in path_points])
    params = {
        "path": path_string,
        "interpolate": "true", # Opcional: interpola pontos ao longo da estrada
        "key": GOOGLE_MAPS_API_KEY
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        data = response.json()

        if "snappedPoints" in data:
            print(f"Pontos ajustados a estradas: {len(data['snappedPoints'])} pontos.")
            return data["snappedPoints"]
        else:
            print(f"Erro ao ajustar pontos a estradas: {data.get('error', {}).get('message', 'Erro desconhecido')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição ao ajustar pontos a estradas: {e}")
        return None

def get_street_view_image_url(latitude, longitude, size="600x300", heading=0, fov=90, pitch=0):
    """Gera uma URL para uma imagem do Street View Static API."""
    if not GOOGLE_MAPS_API_KEY or GOOGLE_MAPS_API_KEY == "YOUR_GOOGLE_MAPS_API_KEY":
        print("Erro: Chave de API do Google Maps não configurada.")
        return None

    base_url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        "size": size,
        "location": f"{latitude},{longitude}",
        "heading": heading,
        "fov": fov,
        "pitch": pitch,
        "key": GOOGLE_MAPS_API_KEY
    }
    # requests.Request para construir a URL sem fazer a requisição imediatamente
    req = requests.Request("GET", base_url, params=params)
    prepped = req.prepare()
    print(f"URL da imagem do Street View gerada para ({latitude}, {longitude}): {prepped.url}")
    return prepped.url

def nominatim_search(query):
    """Realiza uma busca no Nominatim (OpenStreetMap) para geocodificação."""
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "GeoGuessrAI/1.0 (seu_email@exemplo.com)" # É importante fornecer um User-Agent
    }
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            print(f"Nominatim search for \'{query}\': {data[0]['lat']}, {data[0]['lon']}")
            return data[0]
        else:
            print(f"Nenhum resultado encontrado para \'{query}\' no Nominatim.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição ao Nominatim: {e}")
        return None

def mapillary_search_images(latitude, longitude, radius=100):
    """Busca imagens no Mapillary próximas a uma coordenada."""
    # A Mapillary API v4 requer autenticação com um Client Token.
    # Para este exemplo, vamos simular a URL de busca de imagens sem autenticação real.
    # Em um ambiente de produção, você precisaria de um token de cliente válido.
    print("Atenção: A Mapillary API v4 requer autenticação. Esta função apenas simula a URL de busca.")
    base_url = "https://graph.mapillary.com/images"
    # Esta é uma URL de exemplo, a API real é mais complexa e requer um token de acesso.
    # Exemplo de como seria uma query real (simplificada):
    # https://graph.mapillary.com/images?access_token=YOUR_MAPILLARY_ACCESS_TOKEN&bbox=lon,lat,lon,lat
    
    # Para fins de demonstração, vamos apenas retornar uma URL base informativa.
    mock_url = f"https://www.mapillary.com/app/?lat={latitude}&lng={longitude}&radius={radius}"
    print(f"URL de busca de imagens no Mapillary para ({latitude}, {longitude}): {mock_url}")
    return mock_url

if __name__ == '__main__':
    # Teste de geocodificação e Places API
    lat, lng, place_id = geocode_address("Praça da Sé, São Paulo, Brasil")
    if lat and lng and place_id:
        print(f"Latitude: {lat}, Longitude: {lng}, Place ID: {place_id}")

        # Teste da Places API
        place_details = get_place_details(place_id)
        if place_details:
            print(f"Nome do local: {place_details.get('name')}")
            print(f"Endereço: {place_details.get('formatted_address')}")

    # Teste da Roads API
    path_for_roads = [
        (-23.550520, -46.633308),
        (-23.550620, -46.633408),
        (-23.550720, -46.633508)
    ]
    snapped_points = snap_to_roads(path_for_roads)
    if snapped_points:
        for point in snapped_points:
            print(f"Ponto ajustado: {point['location']['latitude']}, {point['location']['longitude']}")

    # Teste da Street View Static API
    street_view_url = get_street_view_image_url(-23.550520, -46.633308)
    if street_view_url:
        print(f"URL do Street View: {street_view_url}")

    # Teste Nominatim (OpenStreetMap)
    nominatim_result = nominatim_search("Eiffel Tower, Paris")
    if nominatim_result:
        print(f"Resultado Nominatim: {nominatim_result}")

    # Teste Mapillary
    mapillary_url = mapillary_search_images(48.858370, 2.294481)
    if mapillary_url:
        print(f"URL Mapillary: {mapillary_url}")


