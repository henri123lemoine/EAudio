import pyttsx3


def tts(text: str, save_path: str=None, play_audio: bool=False, voice: int=None, speed: int=100) -> None:
    """
    :param text: the text to be read
    :param save_path: the path to save the audio file to; if None, it won't save the audio file
    :param play_audio: whether to play the audio file
    :param voice: the voice to use (enter an int if you know which to use, and manually in the terminal if you don't)
    :param speed: the speed to read the text at (100 is standard)
    """

    title = text.split("\n")[0]

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    if voice is not None:
        engine.setProperty('voice', voices[voice-1].id)
    else:
        print(f"Which voice would you like to use out of the following? (enter the associated integer)\n")
        for i, voice in enumerate(voices):
            print(f"{i+1}: {voice.name}")
        engine.setProperty('voice', voices[int(input())-1].id)
    
    engine.setProperty('rate', speed)

    if save_path is not None:
        engine.save_to_file(text, f"{save_path}/{title}.mp3")

    if play_audio:
        engine.say(text)

    engine.runAndWait()
    engine.stop()