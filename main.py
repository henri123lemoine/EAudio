from Helper.get_text import Text
from Helper.get_audio import Audio


def main():
    url = "https://astralcodexten.substack.com/p/even-more-bay-area-house-party"
    save_path = "data"
    text = Text(url)
    Audio(text, save_path, voice=1, speed=300)
    print("Audio saved successfully")

if __name__ == "__main__":
    main()
