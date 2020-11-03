from PIL import Image

# this script manipulates the waterfall to emphasize the center

def modifiedImage(imagePath):
    im = Image.open(imagePath)
    width, height = im.size

    left = 67
    top = 0
    right = width - 137
    bottom = height

    im1 = im.crop((left, top, right, bottom))

    center = (right - left) / 2

    left = left + center - 26
    top = 0
    right = right - center + 25
    bottom = height

    im2 = im.crop((left, top, right, bottom))
    width, height = im2.size
    im2 = im2.resize((width*4, height))

    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))

    width, height = dst.size

    #dst.show()
    return dst

if __name__ == "__main__":
    print('hello')
    dst = modifiedImage('img/good/2904901.png')
    dst.show()
