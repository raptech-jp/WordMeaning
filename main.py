import sqlite3
import gpt

filepath = "test.sqlite"
conn = sqlite3.connect(filepath)

cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
table_exists = cur.fetchone()

if not table_exists:
    cur.execute("""CREATE TABLE items(
        word TEXT PRIMARY KEY,
        meaning TEXT,
        example_english_sentence TEXT,
        part_of_speech TEXT
    )""")
    conn.commit()

word = input("Enter a word: ")
translated = gpt.Word(word)

cur.execute("SELECT word FROM items WHERE word=?", (translated.get_word(),))
existing_word = cur.fetchone()

if not existing_word:
    cur.execute("INSERT INTO items VALUES(?, ?, ?, ?)",(translated.get_word(), translated.get_meaning(), translated.get_example_english_sentence(), translated.get_part_of_speech()))
    conn.commit()
else:
    print(f"The word '{translated.get_word()}' already exists in the database.")

print(translated.get_word())

cur = conn.cursor()
cur.execute("SELECT word, meaning, example_english_sentence, part_of_speech FROM items")
items_list = cur.fetchall()
for fr in items_list:
    print(fr)

conn.close()