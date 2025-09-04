import faiss
import numpy as np
import sqlite3
from image_analysis import generate_visual_embedding, extract_text_from_image, detect_objects
from api_integration import geocode_address, reverse_geocode_coordinates, get_place_details, snap_to_roads, get_street_view_image_url, nominatim_search, mapillary_search_images
import cv2

def load_faiss_index(index_path):
    """Carrega um índice FAISS de um arquivo."""
    index = faiss.read_index(index_path)
    print(f"Índice FAISS carregado de {index_path}.")
    return index

def compare_image_with_database(image_path, faiss_index, embedding_dimension=768, k=5):
    """Compara a imagem de entrada com a base de dados usando embeddings visuais, OCR e detecção de objetos."""
    query_embedding = generate_visual_embedding(image_path)
    if query_embedding is None:
        return None, "Não foi possível gerar o embedding visual da imagem."

    distances, indices = faiss_index.search(query_embedding.astype("float32").reshape(1, -1), k)
    
    extracted_text = extract_text_from_image(image_path)
    detected_objects = detect_objects(image_path)

    conn = sqlite3.connect("geoguessr_db.sqlite")
    cursor = conn.cursor()
    results = []
    for i, idx in enumerate(indices[0]):
        cursor.execute("SELECT clue_id FROM visual_embeddings WHERE faiss_index_id = ?", (int(idx),))
        result = cursor.fetchone()
        if result:
            clue_id = result[0]
            cursor.execute("SELECT description, category, type, country_id FROM clues WHERE id = ?", (clue_id,))
            clue_info = cursor.fetchone()
            if clue_info:
                description, category, type, country_id = clue_info
                country_name = "N/A"
                if country_id:
                    cursor.execute("SELECT name FROM countries WHERE id = ?", (country_id,))
                    country_result = cursor.fetchone()
                    if country_result:
                        country_name = country_result[0]
                results.append({
                    "distance": distances[0][i],
                    "clue_id": clue_id,
                    "description": description,
                    "category": category,
                    "type": type,
                    "country": country_name
                })
    conn.close()

    return results, {"text": extracted_text, "objects": detected_objects}

def predict_location(comparison_results, additional_info):
    """Combina os resultados da comparação, OCR e detecção de objetos para prever a localização."""
    prediction = {
        "coordinates": "Ainda não disponível",
        "confidence": "Baixa",
        "justification": []
    }

    justifications = []
    potential_coordinates = []

    # Analisar resultados da comparação visual
    if comparison_results:
        best_match = comparison_results[0] # O primeiro é o mais próximo
        prediction["confidence"] = "Média" # Aumenta a confiança se houver um bom match visual
        description_match = best_match["description"][:100]
        country_match = best_match["country"]
        distance_match = best_match["distance"]
        justification_text = f"Pista visual mais próxima: {description_match} (País: {country_match}). Distância: {distance_match:.4f}."
        justifications.append(justification_text)
        
        # Se o país for identificado com alta confiança, podemos usar isso
        if best_match["country"] != "N/A":
            prediction["confidence"] = "Média-Alta"
            justifications.append(f"O país mais provável com base em pistas visuais é: {best_match['country']}.")

    # Analisar texto extraído por OCR e usar Geocoding API
    if additional_info and additional_info["text"]:
        text = additional_info["text"].strip()
        if text:
            justifications.append(f"Texto detectado (OCR): \'{text}\' (pode indicar idioma, nomes de cidades/ruas).")
            # Tentar geocodificar o texto extraído
            lat, lng, place_id = geocode_address(text)
            if lat and lng:
                potential_coordinates.append((lat, lng))
                justifications.append(f"Coordenadas sugeridas por OCR/Geocoding: ({lat}, {lng}).")
                if place_id:
                    place_details = get_place_details(place_id)
                    if place_details:
                        place_name = place_details.get("name")
                        formatted_address = place_details.get("formatted_address")
                        justifications.append(f"Detalhes do local (Places API): {place_name}, {formatted_address}.")

    # Analisar objetos detectados e usar Roads API (exemplo simplificado)
    if additional_info and additional_info["objects"]:
        objects = additional_info["objects"]
        if objects:
            objects_str = ", ".join(objects)
            justifications.append(f"Objetos detectados: {objects_str} (podem indicar tipo de estrada, infraestrutura, vegetação).")
            # Se tivermos coordenadas potenciais, podemos tentar usar a Roads API
            if potential_coordinates:
                # A Roads API precisa de múltiplos pontos para ser eficaz, aqui é um exemplo
                # realístico seria usar pontos de uma trajetória ou de detecções múltiplas
                if len(potential_coordinates) >= 2:
                    snapped_points = snap_to_roads(potential_coordinates[:2]) # Pega os 2 primeiros para exemplo
                    if snapped_points:
                        justifications.append(f"Pontos ajustados a estradas (Roads API): {len(snapped_points)} pontos.")

    # Usar OpenStreetMap (Nominatim) para validação ou alternativa
    if additional_info and additional_info["text"]:
        text = additional_info["text"].strip()
        if text:
            nominatim_result = nominatim_search(text)
            if nominatim_result:
                lat_osm = nominatim_result.get("lat")
                lon_osm = nominatim_result.get("lon")
                if lat_osm and lon_osm:
                    potential_coordinates.append((float(lat_osm), float(lon_osm)))
                    justifications.append(f"Coordenadas sugeridas por OpenStreetMap (Nominatim): ({lat_osm}, {lon_osm}).")

    # Determinar as coordenadas finais (lógica simplificada: média das coordenadas potenciais)
    if potential_coordinates:
        avg_lat = sum([coord[0] for coord in potential_coordinates]) / len(potential_coordinates)
        avg_lng = sum([coord[1] for coord in potential_coordinates]) / len(potential_coordinates)
        prediction["coordinates"] = f"({avg_lat:.6f}, {avg_lng:.6f})"
        prediction["confidence"] = "Alta" # Aumenta a confiança se houver coordenadas concretas

    prediction["justification"] = justifications
    return prediction

if __name__ == "__main__":
    # Exemplo de uso
    # Primeiro, certifique-se de que o índice FAISS foi salvo (executando vector_index.py)
    # e que há um test_image.png disponível.
    
    # Salvar um índice FAISS de exemplo para teste
    embedding_dimension = 768
    faiss_index_test = faiss.IndexFlatL2(embedding_dimension)
    # Adicionar um vetor de exemplo para evitar erro de índice vazio
    faiss_index_test.add(np.random.rand(1, embedding_dimension).astype("float32"))
    faiss.write_index(faiss_index_test, "test_faiss_index.bin")

    # Criar uma imagem de teste com texto e um objeto simulado
    test_image = "test_image.png"
    cv2.imwrite(test_image, cv2.cvtColor(
        cv2.putText(cv2.UMat(200, 400, cv2.CV_8UC3), "Rua Augusta, São Paulo", 
                    (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2),
        cv2.COLOR_BGR2RGB))

    # Simular resultados de OCR e detecção de objetos para o teste
    # Estes seriam os resultados reais das funções extract_text_from_image e detect_objects
    # Para este teste, vamos sobrescrever para simular um cenário com dados úteis
    simulated_extracted_text = "Rua Augusta, São Paulo"
    simulated_detected_objects = ["placa de rua", "poste de luz"]

    # Carregar o índice e comparar
    loaded_index = load_faiss_index("test_faiss_index.bin")
    if loaded_index:
        # Chamar compare_image_with_database para obter os resultados visuais
        comparison_results, _ = compare_image_with_database(test_image, loaded_index)
        
        # Criar o dicionário additional_info com os dados simulados
        simulated_additional_info = {
            "text": simulated_extracted_text,
            "objects": simulated_detected_objects
        }

        if comparison_results:
            print("Resultados da comparação:")
            for res in comparison_results:
                print(f"  Distância: {res['distance']:.4f}, Pista: {res['description'][:50]}..., País: {res['country']}")
            print("Informações adicionais (simuladas):")
            print(f"  Texto extraído: {simulated_additional_info['text']}")
            print(f"  Objetos detectados: {simulated_additional_info['objects']}")
            
            # Prever localização com os resultados simulados
            location_prediction = predict_location(comparison_results, simulated_additional_info)
            print("\nPrevisão de Localização:")
            print(f"  Coordenadas: {location_prediction['coordinates']}")
            print(f"  Confiança: {location_prediction['confidence']}")
            print("  Justificativas:")
            for justification in location_prediction['justification']:
                print(f"    - {justification}")
        else:
            # Mesmo sem resultados visuais, tentar prever com base em OCR e objetos
            print("Nenhum resultado de comparação visual encontrado. Tentando prever com outras informações...")
            location_prediction = predict_location([], simulated_additional_info)
            print("\nPrevisão de Localização:")
            print(f"  Coordenadas: {location_prediction['coordinates']}")
            print(f"  Confiança: {location_prediction['confidence']}")
            print("  Justificativas:")
            for justification in location_prediction['justification']:
                print(f"    - {justification}")
    else:
        print("Erro ao carregar o índice FAISS.")


