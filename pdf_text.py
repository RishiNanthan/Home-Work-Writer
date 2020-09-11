import pytesseract as pt
from PIL import Image

s = pt.image_to_string(Image.open("D:\\sample.jpg", "r"))
print(s)
