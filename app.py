

from flask import Flask, request, jsonify, make_response
import openai
from flask_expects_json import expects_json
from jsonschema import ValidationError


app = Flask(__name__)

schema = {
    "type": "object",
    "properties": {
        "author": {"type": "string"},
        "language": {"type": "string"},
        "token": {"type": "string"},
        "num": {"type": "string"},
        "category": {"type": "string"}
    },
    "additionalProperties": False

}

openai.api_key = "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"


def generate_quote(num_quotes, category, language, token, author):
    quotes = []
    # for i in range(num_quotes):
    while len(quotes) < num_quotes:
        response = openai.Completion.create(engine="text-davinci-002",
                                            prompt=f"Hello, ChatGPT! Show me  unique quote of {category} in {language} by {author} within {token} words",
                                            max_tokens=token, temperature=0.5)
        quote = response.choices[0].text
        if quote not in quotes:
            quotes.append(quote)
    return quotes


@app.route('/qapi', methods=['POST', 'GET'])
@expects_json(schema)
def get_responses():
    try:
        data = request.get_json()
        if "num" not in data or not data["num"]:
            num = 1

        else:
            num = int(data['num'])
        if 'category' not in data or not data['category']:
            cat = 'Random'
        else:
            cat = data['category']
        if 'language' not in data or not data['language']:
            lang = 'English'
        else:
            lang = data['language']
        if 'author' not in data or not data['author']:
            aut = 'Anonymous'
        else:
            aut = data['author']
        if 'token' not in data or not data['token']:
            tok = 50
        else:
            tok = int(data['token'])
        quotes = generate_quote(
            num_quotes=num, category=cat, language=lang, token=tok, author=aut)
        quotes_list = [quote.replace("\n", "") for quote in quotes]
        quotes_lists = [quote.replace(f"\"", "") for quote in quotes_list]
        return jsonify(quotes_lists)
        # return{"quotes":quotes}
        # return "\n\n".join(quotes)
    except Exception as e:
        print(e)
        return {"Message": "Something went wrong"}


@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message}), 400)

if __name__ == '__main__':
    app.run(debug=True)
        



if __name__ == '__main__':
    app.run(debug=True)
