from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai
import spacy

load_dotenv()
openai.api_key = os.getenv("OPEN_API_KEY")

print(openai.api_key)

from spacy.lang.en import English
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
CORS(app)
context = ""

def need_to_reset_context(history):
  chunks = [[]]
  chunk_total_words = 0

  sentences = nlp(history)

  for sentence in sentences.sents:
    chunk_total_words += len(sentence.text.split(" "))

  if chunk_total_words > 2700:
    return True    
  else:
    return False

@app.route("/", methods=['GET', 'POST'])
def index():
  global context
  if request.method == 'GET':
    return "Hello from AI!"
  else:
    content = request.json
    prompt = content['prompt']
    print(prompt)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=context + "\n\n"+ prompt,
        max_tokens=1000,
        temperature=0.9,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        #stop=["\n"] maybe not used or bug
    )
    print(response.choices[0].text + "\n")
    if need_to_reset_context(context):
      context = ""
    context += "\n".join([context, prompt, response.choices[0].text])
    return jsonify(bot = response.choices[0].text)

if __name__ == "__main__":
  app.run()
