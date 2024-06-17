# my own code
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from googletrans import Translator

# app =Flask(__name__)
# CORS(app)

# @app.route('/predict',methods=['POST'])
# def predict():
#     try:
#         # translator=Translator()
#         data=request.get_json()
#         input_data=data.get('txt',[])

#         for i in input_data[0:25]:
#             # i['text']=translator.translate(i['text']).text
#             i['text']="Translated Text"

#         return jsonify({"result": input_data}), 200
#     except Exception as e:
#         print(f"Something went wrong: {str(e)}")
#         return jsonify({"error": "Internal Server Error"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)








#ai code

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

app = Flask(__name__)
CORS(app)

# Load the model and tokenizer when the Flask app starts
model_name = 'facebook/nllb-200-distilled-600M'
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def translate(texts, model, tokenizer, src_lang="tam_Taml", tgt_lang="eng_Latn"):
    tokenizer.src_lang = src_lang
    encoded_texts = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    generated_tokens = model.generate(**encoded_texts, forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang])
    translated_texts = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return translated_texts

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_data = data.get('txt', [])
        
        # Extract texts to translate
        tamil_texts = [item['text'] for item in input_data[0:25]]

        start_time = time.time()
        english_translations = translate(tamil_texts, model, tokenizer)
        end_time = time.time()

        # Replace original Tamil texts with English translations
        for i, translation in enumerate(english_translations):
            input_data[i]['text'] = translation

        print(f"Time taken to process {len(tamil_texts)} texts: {end_time - start_time} seconds")
        
        return jsonify({"result": input_data}), 200
    except Exception as e:
        print(f"Something went wrong: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)






