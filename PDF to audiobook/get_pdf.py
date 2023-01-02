import pdfplumber
import os
import re

# pdf_file = 'TTS_Project\PDF to audiobook\l_insoutenable.pdf'
# txt_file = 'TTS_Project\PDF to audiobook\l_insoutenable2.txt'

# pdf = pdfplumber.open(pdf_file)
# pages = pdf.pages
# text_pages = []
# for page in pages:
#     page_txt = page.extract_text()
#     page_txt = " ".join(page_txt.split("\n")[:-2])
#     text_pages.append(page_txt)

# book = re.sub(r'\b\d{1,2}\b', '\nChapter \g<0>\n', " ".join(text_pages[7:394]))

# with open(txt_file, 'w', encoding='utf-8') as f:
#     f.write(book)

from gtts import gTTS

with open('TTS_Project\PDF to audiobook\l_insoutenable.txt', 'r', encoding='utf-8') as f:
    text = f.read()

tts = gTTS(text, lang='fr')
tts.save('TTS_Project\PDF to audiobook\l_insoutenable.mp3')




# import pyttsx3
# from pydub import AudioSegment

# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)  # French female voice

# with open('TTS_Project\PDF to audiobook\l_insoutenable2.txt', 'r') as f:
#     text = f.read()

# audio = AudioSegment.from_speech(text, engine=engine, speech_speed=0.9)
# audio.export('TTS_Project\PDF to audiobook\l_insoutenable.mp3', format='mp3')