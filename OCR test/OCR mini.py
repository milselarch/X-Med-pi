from PIL import Image
from pytesser import *

from SimpleCV import Color,Camera,Display
import vlc
 
image_file = '2017-03-27.png'
#https://stackoverflow.com/questions/20020206/cannot-write-mode-rgba-as-bmp-pytesser
#RGBA to RGB something somethign problems
im = Image.open(image_file)
bg = Image.new("RGB", im.size, (255,255,255))
bg.paste(im,im)
text = image_to_string(bg)

text = image_file_to_string(image_file)
text = image_file_to_string(image_file, graceful_errors=True)
print "=====output=======\n"
print text
