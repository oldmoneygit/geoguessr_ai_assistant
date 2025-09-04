import sqlite3
import re

def extract_and_populate_clues():
    conn = sqlite3.connect("geoguessr_db.sqlite")
    cursor = conn.cursor()

    # Helper to get country_id
    def get_country_id(country_name):
        cursor.execute("SELECT id FROM countries WHERE name = ?", (country_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None

    # Process plonkit_guide_info.md
    with open("plonkit_guide_info.md", "r") as f:
        content = f.read()
        # Extract countries and update driving side/hemisphere if available (not explicitly in plonkit, but good to have)
        country_matches = re.findall(r"\*\s(.*?)\s\((.*?)\)\s-\s(.*?)\n", content)
        for name, code, _ in country_matches:
            cursor.execute("INSERT OR IGNORE INTO countries (name, code) VALUES (?, ?)", (name.strip(), code.strip()))
            # For now, driving_side and hemisphere are not in plonkit, will be added from other sources

        # Extract general structure clues from plonkit
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Structure", "O guia inclui apenas países com cobertura oficial do Google Street View. Fotosferas e cobertura Ari não serão incluídas."))
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Structure", "Cada página consiste em três seções: Identificando o país, Pistas regionais e específicas de subdivisão, Destaque: pistas muito específicas."))

    # Process geotips_info.md
    with open("geotips_info.md", "r") as f:
        content = f.read()
        # General tips from GeoTips
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Meta", "Qualidade da câmera do Google Street View: Existem 4 gerações de câmeras, e a qualidade da imagem pode indicar o ano da captura e, consequentemente, a região."))
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Meta", "Carro do Google Street View: Detalhes sobre o veículo de captura, como barras no teto, racks, antenas ou a cor do carro, variam por país."))
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Environmental", "Direção do Sol: A posição do sol (norte no Hemisfério Norte, sul no Hemisfério Sul) é uma pista fundamental para determinar o hemisfério."))
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Road", "Lado da Direção: Se o tráfego é pela direita ou pela esquerda da estrada. Esta é uma das pistas mais fortes para eliminar um grande número de países."))
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Strategy", "Ir na direção oposta à do carro do Google: O carro do Google sempre foi da estrada principal para cobrir estradas pequenas."))
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Strategy", "Ir ladeira abaixo: A maioria dos assentamentos está situada nos vales e não nas montanhas."))
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Strategy", "Encontrar 3 coisas principais: país/estado/região, número da estrada e nome do assentamento."))
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Strategy", "Usar a orientação da estrada: Aponte a câmera para o norte e veja a direção da estrada."))

    # Process geomastr_info.md
    with open("geomastr_info.md", "r") as f:
        content = f.read()
        # Extract and update driving side for countries (example, need to parse more)
        # This part would require more sophisticated parsing of geomastr to extract country-specific driving sides
        # For now, let's add general clues from geomastr
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Cultural", "Alfabetos e idiomas: Familiarizar-se com os alfabetos e idiomas usados em diferentes países pode fornecer dicas significativas."))
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Cultural", "Moedas: Cada país tem sua própria moeda, e saber qual moeda está em uso pode ser fundamental."))
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Cultural", "Prefixos telefônicos: Códigos numéricos exclusivos atribuídos a cada país."))
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Technical", "Nomes de domínio: Representam os endereços de internet de sites e variam por país."))
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Road", "Linhas de estrada, balizadores, empresas de postos de gasolina, placas de veículos, caixas de correio e sinais de rua: exibem características e estilos únicos."))
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                       (None, "General", "Cultural", "Placas de veículos: Servem como identificadores distintos de veículos em diferentes países."))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    extract_and_populate_clues()
    print("Clues extracted and populated successfully.")


