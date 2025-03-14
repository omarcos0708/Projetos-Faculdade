from flask import Flask, request, jsonify
from textblob import TextBlob
import nltk
nltk.download('punkt')

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    sentiment = analyze_sentiment(user_message)
    
    if sentiment == 'positive':
        response = "I'm glad you're feeling well! How can I help?"
    elif sentiment == 'negative':
        response = "It looks like you're feeling unwell. Is there anything I can do to help?"
    else:
        response = "Conte-me mais sobre isso."
    
    return jsonify({'response': response})

def analyze_sentiment(message):
    blob = TextBlob(message)
    if blob.sentiment.polarity > 0:
        return 'positive'
    elif blob.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'

if __name__ == '__main__':
    app.run(debug=True)


# Rode isto no Terminal, o modelo deve retornar a resposta correta com base no sentimento da frase escolhida:
# curl -X POST -H "Content-Type: application/json" -d '{"message": "I am happy today"}' http://127.0.0.1:5000/chat
