import faiss
import numpy as np
import sqlite3

def create_faiss_index(dimension):
    """Cria um índice FAISS para embeddings visuais."""
    index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity search
    print(f"Índice FAISS criado com dimensão {dimension}.")
    return index

def add_embeddings_to_index(index, embeddings, clue_ids):
    """Adiciona embeddings e seus IDs de pista correspondentes ao índice FAISS e ao banco de dados."""
    # Ensure embeddings are float32 as required by FAISS
    embeddings = embeddings.astype("float32")
    
    # Check dimension before adding
    if embeddings.shape[1] != index.d:
        raise ValueError(f"Dimensão do embedding ({embeddings.shape[1]}) não corresponde à dimensão do índice FAISS ({index.d}).")

    index.add(embeddings)
    print(f"Adicionados {len(embeddings)} embeddings ao índice FAISS.")

    conn = sqlite3.connect("geoguessr_db.sqlite")
    cursor = conn.cursor()
    for i, clue_id in enumerate(clue_ids):
        # Update the faiss_index_id for the corresponding visual_embedding entry
        # The faiss_index_id is the internal index of the FAISS database
        cursor.execute("UPDATE visual_embeddings SET faiss_index_id = ? WHERE id = ?", (index.ntotal - len(embeddings) + i, clue_id))
    conn.commit()
    conn.close()
    print("IDs de pista atualizados no banco de dados.")

def search_faiss_index(index, query_embedding, k=5):
    """Pesquisa no índice FAISS pelos k vizinhos mais próximos."""
    query_embedding = query_embedding.astype("float32").reshape(1, -1)
    distances, indices = index.search(query_embedding, k)  # D: distances, I: indices
    print(f"Pesquisa FAISS concluída. Distâncias: {distances}, Índices: {indices}")
    return distances, indices

if __name__ == '__main__':
    embedding_dimension = 768  # DINOv2 base model output dimension is 768
    faiss_index = create_faiss_index(embedding_dimension)

    conn = sqlite3.connect("geoguessr_db.sqlite")
    cursor = conn.cursor()

    # Add faiss_index_id column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE visual_embeddings ADD COLUMN faiss_index_id INTEGER")
        print("Coluna faiss_index_id adicionada à tabela visual_embeddings.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Coluna faiss_index_id já existe.")
        else:
            raise e

    # Clear existing dummy embeddings to avoid conflicts during re-run
    cursor.execute("DELETE FROM visual_embeddings WHERE image_path LIKE 'dummy_image_%.png'")
    conn.commit()
    print("Embeddings dummy existentes limpos.")

    # Criar alguns embeddings dummy e IDs de pista
    dummy_embeddings = np.random.rand(10, embedding_dimension).astype(np.float32) # Ensure this matches embedding_dimension and is float32
    # Inserir embeddings dummy no banco de dados primeiro para ter clue_ids reais
    dummy_clue_ids = []
    for i, emb in enumerate(dummy_embeddings):
        embedding_bytes = emb.tobytes()
        cursor.execute("INSERT INTO visual_embeddings (clue_id, embedding, image_path) VALUES (?, ?, ?)",
                       (i + 1, embedding_bytes, f"dummy_image_{i}.png")) # Using i+1 as dummy clue_id
        dummy_clue_ids.append(cursor.lastrowid) # Get the actual ID from the DB
    conn.commit()
    print("Embeddings dummy inseridos no banco de dados.")

    # Agora, adicione os embeddings do banco de dados ao índice FAISS
    cursor.execute("SELECT id, embedding FROM visual_embeddings WHERE image_path LIKE 'dummy_image_%.png'")
    db_embeddings_data = cursor.fetchall()

    db_clue_ids_for_faiss = [row[0] for row in db_embeddings_data]
    db_embeddings_for_faiss = np.array([np.frombuffer(row[1], dtype=np.float32) for row in db_embeddings_data])

    if len(db_embeddings_for_faiss) > 0:
        add_embeddings_to_index(faiss_index, db_embeddings_for_faiss, db_clue_ids_for_faiss)

    # Exemplo de pesquisa
    query_emb = np.random.rand(embedding_dimension).astype(np.float32) # Ensure query embedding is also float32
    distances, indices = search_faiss_index(faiss_index, query_emb)

    # Recuperar informações das pistas com base nos índices retornados
    for idx in indices[0]:
        cursor.execute("SELECT clue_id FROM visual_embeddings WHERE faiss_index_id = ?", (idx,))
        result = cursor.fetchone()
        if result:
            clue_id = result[0]
            cursor.execute("SELECT description FROM clues WHERE id = ?", (clue_id,))
            clue_description = cursor.fetchone()
            print(f"Pista encontrada (clue_id: {clue_id}): {clue_description[0] if clue_description else 'N/A'}")
    conn.close()


