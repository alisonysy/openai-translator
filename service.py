import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from utils import ArgumentParser, ConfigLoader, LOG
from ai_translator.model import GLMModel, OpenAIModel
from ai_translator.translator import PDFTranslator


async def translate_and_output(input_path, model_name, model_type, output_format):
    api_key = os.environ.get('OPENAI_API_KEY')
    if model_name == 'OpenAIModel':
        model = OpenAIModel(model=model_type, api_key=api_key)
    else:
        # to be implemented
        raise Exception('Not yet supported')
    
    pdf_file_path = input_path
    translator = PDFTranslator(model)
    translator.translate_pdf(pdf_file_path, output_format)
    return f'{input_path} has been successfully translated.'