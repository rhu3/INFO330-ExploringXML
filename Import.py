import sqlite3
import sys
import xml.etree.ElementTree as ET

# Read pokemon XML file name from command-line
if len(sys.argv) < 2:
    print("You must pass at least one XML file name containing Pokemon to insert")
    sys.exit(1)

# Connect to the SQLite database
conn = sqlite3.connect('pokemon.sqlite')
c = conn.cursor()

for i, arg in enumerate(sys.argv):
    # Skip if this is the Python filename (argv[0])
    if i == 0:
        continue

    # Parse the XML file
    tree = ET.parse(arg)
    root = tree.getroot()

    # Extract the necessary fields from the XML
    pokedex = root.get('pokedex')
    classification = root.get('classification')
    generation = root.get('generation')
    name = root.find('name').text
    hp = root.find('hp').text
    attack = root.find('attack').text
    defense = root.find('defense').text
    speed = root.find('speed').text
    sp_attack = root.find('sp_attack').text
    sp_defense = root.find('sp_defense').text
    height = root.find('height/m').text
    weight = root.find('weight/kg').text
    types = [type_node.text for type_node in root.findall('type')]
    abilities = [ability_node.text for ability_node in root.findall('abilities/ability')]

    # Check if the Pokemon already exists in the database
    c.execute("SELECT * FROM pokemon WHERE pokedex=?", (pokedex,))
    if c.fetchone():
        print(f"Pokemon with Pokedex number {pokedex} already exists in the database.")
        continue

    # Insert the Pokemon into the database
    c.execute("INSERT INTO pokemon (pokedex, classification, generation, name, hp, attack, defense, speed, sp_attack, sp_defense, height, weight) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (pokedex, classification, generation, name, hp, attack, defense, speed, sp_attack, sp_defense, height, weight))
    pokemon_id = c.lastrowid

    # Insert the types and abilities
    for type in types:
        c.execute("INSERT INTO types (pokemon_id, type) VALUES (?, ?)", (pokemon_id, type))
    for ability in abilities:
        c.execute("INSERT INTO abilities (pokemon_id, ability) VALUES (?, ?)", (pokemon_id, ability))

    print(f"Inserted Pokemon {name} into the database.")

# Commit the changes and close the connection
conn.commit()
conn.close()

