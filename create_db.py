import sqlite3

def create_database():
    conn = sqlite3.connect('geoguessr_db.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL UNIQUE,
            driving_side TEXT,
            hemisphere TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_id INTEGER,
            category TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (country_id) REFERENCES countries(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visual_embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clue_id INTEGER,
            embedding BLOB NOT NULL,
            image_path TEXT,
            FOREIGN KEY (clue_id) REFERENCES clues(id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print('Database geoguessr_db.sqlite created successfully.')

