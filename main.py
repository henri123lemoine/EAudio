from Helper.tts import tts
from Helper.get_text import get_text

url = "https://forum.effectivealtruism.org/posts/jk7A3NMdbxp65kcJJ/500-million-but-not-a-single-one-more"
save_path_text = "Files"
print_bool = False
save_path_audio = "Files"
play_audio = False
voice = None
speed = 300

text = get_text(url, save_path=save_path_text, print_bool=print_bool)
tts(text, save_path=save_path_audio, play_audio=play_audio, voice=voice, speed=speed)
