import sqlite3
import re

def populate_database():
    conn = sqlite3.connect('geoguessr_db.sqlite')
    cursor = conn.cursor()

    # Populate from plonkit_guide_info.md
    with open('plonkit_guide_info.md', 'r') as f:
        content = f.read()
        countries = re.findall(r'\*\s(.*?)\s\((.*?)\)\s-\s(.*?)\n', content)
        for country in countries:
            name, code, _ = country
            cursor.execute("INSERT OR IGNORE INTO countries (name, code) VALUES (?, ?)", (name.strip(), code.strip()))

    # Populate from geotips_info.md
    with open('geotips_info.md', 'r') as f:
        content = f.read()
        # This file has general tips, not easily parsable into the current DB structure.
        # We will add them as general clues.
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)", 
                       (None, 'General', 'Meta', content))

    # Populate from geomastr_info.md
    with open('geomastr_info.md', 'r') as f:
        content = f.read()
        # This file has general tips, not easily parsable into the current DB structure.
        # We will add them as general clues.
        cursor.execute("INSERT INTO clues (country_id, category, type, description) VALUES (?, ?, ?, ?)", 
                       (None, 'General', 'Meta', content))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    populate_database()
    print('Database populated successfully.')


