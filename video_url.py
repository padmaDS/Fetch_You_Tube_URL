import pywhatkit
import requests

name = input("enter the name of the video: ")

y = pywhatkit.playonyt(name, open_video = False)
url = requests.get(y).url

print(url)


### Reference

https://www.youtube.com/watch?v=noecHp7uZrY&t=201s
