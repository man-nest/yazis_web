import speech_recognition


def speechRecognition(language: str = 'en-En', stopWord: str = 'stop speech'):
    recognizer = speech_recognition.Recognizer()

    text = ''
    while True:

        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                
                text = recognizer.recognize_google(audio, language=language)
                text = text.lower()
                
                print(f"Recognized {text}")
                
                if stopWord in text:
                    return text
                
        except:
            recognizer = speech_recognition.Recognizer()
            continue