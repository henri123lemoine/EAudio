# EAudio
This project has as goal to make simple the audio-listening of TTS for the EA Forum, Lesswrong, the Alignment Forum, Gwern.net, Substack, and Arbital. Give the program a URL to any post on these websites and an audio version will be generated.

The Nonlinear Library already does something like this for the EA Forum and for Lesswrong, but only for a minority of posts (the most upvoted ones) on each site, and they don't let you download the files. This is a problem.
Moreover, even on the best podcast apps you have limited control over the listening experience; you have no say over which voice is reading for you, at precisely what speed, etc. This project is my attempt at solving those issues, and I intend to add functionalities over time.

## Example result 😍 A few clicks away..
![image](https://user-images.githubusercontent.com/42588535/208750191-bc200108-d85c-460e-aa6a-a1cb7cce248f.png)

## Features
Save text file or TTS audio file for your favorite EAF/LW/AF/etc posts. Control voice speed and accent (using your Windows voices).

## Requirements
You will need to install pyttsx3, requests, and beautifulsoup4 => pip install pyttsx3 requests beautifulsoup4

## How to Use?
After having installed the required libraries and the repository itself:
1. Go on main.py
2. You then have multiple options:
    - url: the url you want text/audio of. Currently accepts urls from the EA Forum, Lesswrong, the Alignment Forum, Gwern.net, and Substack. It is not very robust at the moment, so make sure to have full links.
    - save_path: the path to which the audio file is saved.
    - voice: the voice # that the program uses to generate the audio. Your voices can be found in your Windows Settings in Time&Language > Speech > Installed Voice Packages. I don't know how things work on other machines.
    - speed: the speed of the voice. "Standard" speed is 100, but I suggest you try around to see what's best for you.
3. Run the program.

## Contribute
This project is only in its infancy. If there are bugs or issues, or if you have ideas for improvements, please tell me. 
My main future plans are to make this work on a public easy-to-use website, and add some functionalities. 
DM me @HenriLemoine13 if you want to help!

## TODO
- add a live speed controller (separate sentences)
- change tone of TTS for bold text (louder) and italic text (slower)
- for LW/EAF/AF, if the url to a sequence is given, the full sequence's audio should be downloaded in save_path
- set up the text extraction for Arbital (this will be significantly harder than for other sites)