import os
import json
import openai
from dotenv import load_dotenv

load_dotenv(verbose=True)

openai.api_key = os.getenv("OPENAI_API_KEY")

class Word:
    def __init__(self, target):
        self.target = target
        self.meaning = None
        self.example_english_sentence = None
        self.part_of_speech = None
        self.get_word_info(target) 

    def get_word_info(self, target):
        prompt = [{'role': 'user', 'content': f"Translate the English word '{target}' to Japanese and provide an example sentence and part of speech."}]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            temperature=0.5,
            functions=[
                {
                    "name": "create_translation",
                    "description": f"Translate the English word '{target}' to Japanese and provide an example sentence and part of speech.",
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
        res = response["choices"][0]["message"]["function_call"]["arguments"]
        data = json.loads(res)

        self.meaning = data["meaning"]
        self.example_english_sentence = data["example_english_sentence"]
        self.part_of_speech = data["part_of_speech"]
        
    def get_word(self):
        return self.target

    def get_meaning(self):
        return self.meaning

    def get_example_english_sentence(self):
        return self.example_english_sentence

    def get_part_of_speech(self):
        return self.part_of_speech