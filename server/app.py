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
context = ""

def need_to_reset_context(history):
  if (len(history) > 10000): # 4097 token limit(-1000 completion token) * 4 : 1 token = 4 chars in english
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
    if need_to_reset_context(context):
      context = ""
      context_updated = prompt
    else:
      context_updated = context + "\n"+ prompt
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=context_updated,
        max_tokens=1000,
        temperature=0.9,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        #stop=["\n"] maybe not used or bug
    )
    print(response.choices[0].text + "\n")
    context += "\n".join([context, prompt, response.choices[0].text])
    return jsonify(bot = response.choices[0].text)

if __name__ == "__main__":
  app.run()
