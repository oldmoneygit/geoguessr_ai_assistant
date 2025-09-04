import sqlite3

def ingest_country_data(name, code, driving_side=None, hemisphere=None):
    conn = sqlite3.connect("geoguessr_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO countries (name, code, driving_side, hemisphere) VALUES (?, ?, ?, ?)",
                   (name, code, driving_side, hemisphere))
    conn.commit()
    conn.close()
    print(f"Country {name} ingested/updated.")

def ingest_clue_data(country_name, category, type, description):
    conn = sqlite3.connect("geoguessr_db.sqlite")
    cursor = conn.cursor()
    country_id = None
    if country_name:
        cursor.execute("SELECT id FROM countries WHERE name = ?", (country_name,))
        result = cursor.fetchone()
        if result:
            country_id = result[0]
        else:
            print(f"Warning: Country {country_name} not found. Clue will be added without country_id.")

    cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)",
                   (country_id, category, type, description))
    conn.commit()
    conn.close()
    print(f"Clue for {country_name if country_name else 'general'} ingested.")

def ingest_visual_embedding(clue_id, embedding, image_path):
    conn = sqlite3.connect("geoguessr_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO visual_embeddings (clue_id, embedding, image_path) VALUES (?, ?, ?)",
                   (clue_id, embedding, image_path))
    conn.commit()
    conn.close()
    print(f"Visual embedding for clue_id {clue_id} ingested.")

if __name__ == '__main__':
    # Example usage (can be called from other scripts or manually)
    # ingest_country_data("Brazil", "br", "right", "southern")
    # ingest_clue_data("Brazil", "Road", "Sign", "Placas de trânsito verdes.")
    print("Data ingestion script ready. Use functions to ingest data.")


