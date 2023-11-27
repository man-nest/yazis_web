import pyttsx3


def speechGenerate(text: str, rate:int = 200, volume:float = 1.0, voice:str = 'ZIRA_EN'):
    engine = pyttsx3.init()
    
    """RATE"""
    engine.setProperty('rate', rate)
    
    """VOLUME"""
    engine.setProperty('volume', volume)
    
    """VOICE"""
    voices = engine.getProperty('voices')
    
    if voice == 'ZIRA_EN':
        engine.setProperty('voice', voices[1].id)
    elif voice == 'IRINA_RU':
        engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()