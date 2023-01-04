import pyttsx3
import winreg


class Audio:
    def __init__(self, text, save_path: str=None, voice: int=0, speed: int=200) -> None:
        """
        :param url: the text to be read
        :param save_path: the path to save the audio file to; if None, it saves in the download folder
        :param voice: the voice to use
        :param speed: the speed to read the text at
        """
        if save_path is None:
            save_path = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"), "{374DE290-123F-4565-9164-39C4925E467B}")[0]
        
        self.text = text
        self.title = "".join([c for c in self.text.title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        self.string = text.string
        self.save_path = save_path
        self.voice = voice
        self.speed = speed

        self.engine = self.set_engine()
        self.save_audio()

    def set_engine(self):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[self.voice].id)
        engine.setProperty('rate', self.speed)
        return engine

    def save_audio(self):
        self.engine.save_to_file(self.text.string, f"{self.save_path}/{self.title}.mp3")
        self.engine.runAndWait()
        self.engine.stop()


if __name__ == "__main__":
    from get_text import Text
    text = Text("https://arbital.com/p/bayes_rule/?l=693")
    Audio(text, 'Helper', voice=0, speed=300)
    print("Audio saved successfully")
