from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPEN_API_KEY")

print(openai.api_key)

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return "Hello from AI!"
  else:
    content = request.json
    prompt = content['prompt']
    print(prompt)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.9,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )
    return jsonify(bot = response.choices[0].text)

if __name__ == "__main__":
  app.run()