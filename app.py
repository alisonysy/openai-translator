from quart import Quart, request
from service import translate_and_output

app = Quart(__name__)

@app.route("/")
async def index():
    return {"status": "OK"}

@app.post("/api/translate")
async def translate_output():
    data = await request.get_json()
    book = data.get('input_path', None)
    if not book:
        raise Exception('Please provide the path for the book to be translated')
    model_type = data.get('model_type', 'OpenAIModel')
    openai_model = data.get('openai_model', 'gpt-3.5-turbo')
    output_format = data.get('output_format', 'pdf')
    re = await translate_and_output(book, model_type, openai_model, output_format)
    return re