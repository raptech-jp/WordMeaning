import os
import sys
import mysql.connector
from gpt import Word

def create_database_connection():
    return mysql.connector.connect(
        host='localhost',
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        port='3306',
        charset='utf8'
    )

def create_word_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS word (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            word VARCHAR(255) NOT NULL,
            meaning TEXT NOT NULL,
            example_english_sentence TEXT NOT NULL,
            part_of_speech TEXT NOT NULL
        )
    """)

def table_exists(cursor):
    cursor.execute("SHOW TABLES LIKE 'word'")
    return cursor.fetchone() is not None

def insert_word(cursor, translated, name):
    cursor.execute("SELECT word FROM word WHERE word=%s", (translated.get_word(),))
    existing_word = cursor.fetchone()

    if not existing_word:
        cursor.execute("""
            INSERT INTO word (name, word, meaning, example_english_sentence, part_of_speech)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, translated.get_word(), translated.get_meaning(), translated.get_example_english_sentence(), translated.get_part_of_speech()))
    else:
        print(f"The word '{translated.get_word()}' already exists in the database.")

def main():
    try:
        name = input("Your name: ")
        conn = create_database_connection()
        cur = conn.cursor()

        if not table_exists(cur):
            create_word_table(cur)
            conn.commit()

        while True:
            word = input("\nEnter a word (press Ctrl+C to exit): ")

            if not word:
                continue

            translated = Word(word)
            insert_word(cur, translated, name)
            
    except KeyboardInterrupt:
        print("Program terminated.")
        sys.exit()

    finally:
        cur.close()
        conn.commit()
        conn.close()

if __name__ == "__main__":
    main()
