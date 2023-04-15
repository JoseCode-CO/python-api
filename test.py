from flask import Flask, request, jsonify
from textblob import TextBlob
from better_profanity import profanity

app = Flask(__name__)

def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity
    if polaridad > 0:
        return "Positivo"
    elif polaridad < 0:
        return "Negativo"
    else:
        return "Neutral"

def analizar_malas_palabras(texto):
    palabras_ofensivas_espanol = ["marica", "pendejo", "cabrón"]
    profanity.load_censor_words()
    profanity.add_censor_words(palabras_ofensivas_espanol)
    
    contiene_malas_palabras = profanity.contains_profanity(texto)
    if contiene_malas_palabras:
        return "Contiene malas palabras"
    else:
        return "No contiene malas palabras"

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.get_json(force=True)
    texto = data.get('texto', '')

    resultado_sentimiento = analizar_sentimiento(texto)
    resultado_malas_palabras = analizar_malas_palabras(texto)

    response = {
        'sentimiento': resultado_sentimiento,
        'malas_palabras': resultado_malas_palabras
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
