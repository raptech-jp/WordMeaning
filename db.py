import os
import gpt
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"),
    port='3306',
    charset='utf8'
)

cur = conn.cursor()

name = input("Your name: ")

cur.execute("SHOW TABLES LIKE 'word'")
table_exists = cur.fetchone()

if not table_exists:
    cur.execute("""
        CREATE TABLE word (
            name VARCHAR(255) PRIMARY KEY,
            word VARCHAR(255) NOT NULL,
            meaning TEXT NOT NULL,
            example_english_sentence TEXT NOT NULL,
            part_of_speech TEXT NOT NULL
        )
    """)
    conn.commit()

word = input("Enter a word: ")
translated = gpt.Word(word)

cur.execute("SELECT word FROM word WHERE word=%s", (translated.get_word(),))
existing_word = cur.fetchone()

if not existing_word:
    cur.execute("INSERT INTO word (name, word, meaning, example_english_sentence, part_of_speech) VALUES (%s,%s, %s, %s, %s)",
                (name, translated.get_word(), translated.get_meaning(), translated.get_example_english_sentence(), translated.get_part_of_speech()))
    conn.commit()
else:
    print(f"The word '{translated.get_word()}' already exists in the database.")

print(translated.get_word())

cur.execute("SELECT word, meaning, example_english_sentence, part_of_speech FROM word where name=%s", (name,))
items_list = cur.fetchall()
for fr in items_list:
    print(fr)

conn.close()