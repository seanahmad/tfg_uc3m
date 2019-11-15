from PIL import Image

test_image = "dayClip1--00000.jpg"
original = Image.open(test_image)
#original.show()

width, height = original.size   # Get dimensions
left = 698
top = 333
right = 710
bottom = 358
cropped_example = original.crop((left, top, right, bottom))

cropped_example.show()