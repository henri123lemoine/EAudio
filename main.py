from Helper.get_text import Text
from Helper.get_audio import Audio


def main():
    # Give a url to get audio for the url, give path to a txt file to get audio for the text in the file
    url = None # "https://astralcodexten.substack.com/p/even-more-bay-area-house-party"
    path_to_txt = None # "data/Input.txt"
    save_path = "data"
    text = Text(url, path_to_txt)
    Audio(text, save_path, voice=1, speed=300)
    print("Audio saved successfully")

if __name__ == "__main__":
    main()
