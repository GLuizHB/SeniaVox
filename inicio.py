from gtts import gTTS
from flask import Flask, request, render_template
import speech_recognition as sr
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_path = None
    texto = None

    if request.method == 'POST':
        recognizer = sr.Recognizer()
        
        # Verificar se o microfone foi ativado
        if 'microfone' in request.form:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Diga algo...")
                audio_data = recognizer.listen(source)
                
                try:
                    texto = recognizer.recognize_google(audio_data, language='pt-BR')
                except sr.UnknownValueError:
                    texto = "Não consegui entender o áudio."
                except sr.RequestError as e:
                    texto = f"Erro ao solicitar resultados do serviço de reconhecimento de voz; {e}"

        # Se o usuário digitar texto, usar o texto digitado
        elif 'texto' in request.form:
            texto = request.form['texto']

        # Converter o texto (digitado ou reconhecido) em áudio
        if texto:
            idioma = request.form['idioma']
            tts = gTTS(text=texto, lang=idioma)
            audio_path = 'static/audio_exemplo.mp3'
            tts.save(audio_path)
    
    return render_template('index.html', audio_path=audio_path, texto=texto)

if __name__ == '__main__':
    app.run(debug=True)
