from PIL import Image
from pytesser import *

from SimpleCV import Color,Camera,Display
import vlc
import time

display = Display()
camera = Camera()

cam = camera
#prevBarcode = None
audio = vlc.MediaPlayer('')

def getText(image):
    bg = Image.new("RGB", image.size, (255,255,255))
    bg.paste(image)
    text = image_to_string(bg)
    return text

k = 0

while display.isNotDone():
    img = cam.getImage() #gets image from the camera
    pilImage = img.getPIL()
    print(getText(pilImage))
    img.show()

    k += 1
    print(k)
    
    #time.sleep(0.5)
    
