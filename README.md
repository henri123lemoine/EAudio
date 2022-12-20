# EAudio
This project has as goal to make simple the audio-listening of TTS for the EA Forum, Lesswrong, and the Alignment Forum.

The non-linear library already does something like this, but only for a minority of posts on each site, and they don't let you download the files. This is a problem.
Moreover, even on the best podcast apps you have limited control over the listening experience; you have no say over which voice is reading for you, at precisely what speed, etc. This project is my attempt at solving those issues, and I intend to add functionalities over time.

## Example result 😍 A few clicks away..
![image](https://user-images.githubusercontent.com/42588535/208750191-bc200108-d85c-460e-aa6a-a1cb7cce248f.png)

## Features
Save text file or TTS audio file for your favorite EAF/LW/AF posts. Control voice speed and accent.

## Requirements
You will need to install pyttsx3, requests, and beautifulsoup4 => pip install pyttsx3 requests beautifulsoup4

## How to Use?
After having installed the required libraries and the repository itself:
1. Go on main.py
2. You then have multiple options:
    - url: the url you want text/audio of. Currently accepts urls from the EA Forum, Lesswrong or the Alignment Forum. It is not very robust at the moment, so make sure to have full links.
    - save_path_text: the path to which the text file containing the contents of your url will be saved. If this is None, no text file will be created.
    - print_bool: whether or not to print the text to the console.
    - save_path_audio: same as save_path_text, but for the audio mp3 file.
    - play_audio: whether or not to play the audio directly.
    - voice: the voice # that the program uses to generate the audio. Your voices can be found in your Windows Settings in Time&Language > Speech > Installed Voice Packages. I don't know how things work on other machines. If you prefer, you can leave voice to None in order for the program to show you your options.
    - speed: the speed of the voice. "Standard" speed is 100, but I suggest you try around to see what's best for you.
3. Run the program.

## Contribute
This project is only in its infancy. If there are bugs or issues, or if you have ideas for improvements, please tell me. 
My main future plans are to make this work on a public easy-to-use website, and add some functionalities. 
DM me @HenriLemoine13 if you want to help!
