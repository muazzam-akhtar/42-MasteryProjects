from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt
from load_image import ft_load


def print_rows_first_elem(arr, int):
    """
    A function that reads and prints the first element of each row.
    """
    count = 0
    for row in arr:
        count += 1
    length = count
    count = 0
    for row in arr:
        if count == 0:
            print("[[[" if int == 1 else "[[", row[0], "]", sep="")
        if count > 0 and count < 3 or count > length - 4:
            if int == 1:
                if count == length - 1:
                    print("  [", row[0], "]]]", sep="")
                elif count < length - 1:
                    print("  [", row[0], "]", sep="")
            else:
                print("  ", row[0], "]]" if count == (length - 1)
                      else "", sep="")
        if count == 2:
            print(" ...")
        count += 1


def cropImage(image: Image) -> Image:
    """
    A function that takes an image and returns the cropped size of
    the image in square.
    """
    cropSize = min(image.width, image.height)
    cropLeft = (image.width - cropSize) // 2
    cropTop = (image.height - cropSize) // 2
    cropRight = cropLeft + cropSize
    cropBottom = cropTop + cropSize
    return image.crop((cropLeft, cropTop, cropRight, cropBottom))


def transposeImage(image: Image) -> Image:
    """
    A function which takes an image and returns the transposed image.
    """
    width, height = image.size
    transposedImage = Image.new("RGB", (height, width))
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            transposedImage.putpixel((y, x), pixel)
    return transposedImage


def main():
    """
    A program to take an image and displays the image in right rotation.
    """
    try:
        path = 'animal.jpeg'
        if not path.lower().endswith(('jpg', 'jpeg')):
            raise AssertionError("Only JPG and JPEG formats are supported.")
        if not os.path.exists(path):
            raise AssertionError("File not found:", path)
        image = Image.open(path)
        if image is None:
            raise AssertionError("Failed to load image.")
        transposedImage = transposeImage(cropImage(image.crop((400, 100,
                                                               800, 600))))
        image = ft_load(path)
        print_rows_first_elem(np.array(image), 1)
        print(f"\nNew shape after cropping: {transposedImage.size}")
        print_rows_first_elem(np.array(transposedImage), 1)
        plt.imshow(transposedImage.convert('L'), cmap='gray')
        plt.title("Rotate Image")
        plt.axis('on')
        plt.show()
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == '__main__':
    main()
