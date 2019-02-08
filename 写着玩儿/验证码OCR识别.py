import tesserocr
from PIL import Image

image = Image.open('C:/Users/ZhangWP/Desktop/code.jpg')
image = image.convert('L')
threshold = 50
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
image = image.point(table, '1')
image.show()
print(tesserocr.image_to_text(image))