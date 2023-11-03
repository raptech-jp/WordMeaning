import os
import openai
from dotenv import load_dotenv

load_dotenv(verbose=True)

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_word_info(word):
    prompt = [{'role': 'user', 'content': f"Translate the English word '{word}' to Japanese and provide an example sentence and part of speech."}]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0.5,
        functions=[
            {
                "name": "create_translation",
                "description": "Translate the English word 'word' to Japanese and provide an example sentence and part of speech.",
                "parameters": { 
                    "type": "object",
                    "properties": {
                        "meaning": {
                            "type": "string",
                            "description": "Translated into Japanese."
                        },
                        "example_english_sentence": {
                            "type": "string",
                            "description": "Example English sentence."
                        },
                        "part_of_speech": {
                            "type": "string",
                            "description": "Part of speech."
                        }
                    }
                }
            }
        ]
    )
    
    return response["choices"][0]["message"]["function_call"]["arguments"]
