import numpy as np
import sqlite3

conn = sqlite3.connect("geoguessr_db.sqlite")
cursor = conn.cursor()

cursor.execute("SELECT embedding FROM visual_embeddings LIMIT 1;")
result = cursor.fetchone()

if result:
    embedding_bytes = result[0]
    embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
    print(f"Dimensão do embedding no DB: {embedding.shape}")
else:
    print("Nenhum embedding encontrado no banco de dados.")

conn.close()
