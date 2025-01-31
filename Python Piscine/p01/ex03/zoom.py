from load_image import ft_load
from load_image import print_rows_first_elem
from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt


def main():
    """
    A program which takes an image and displays the cropped image.
    """
    try:
        path = "animal.jpeg"
        if not path.lower().endswith(("jpg", "jpeg")):
            raise AssertionError("Only JPG or JPEG formats are supported.")
        if not os.path.exists(path):
            raise AssertionError("File not found", path)
        image = Image.open(path)
        if image is None:
            raise AssertionError("Failed to load image.")
        ft_load(path)

        zoomedImg = image.crop((400, 200, 800, 600))
        print(f"\nNew shape after cropping: {zoomedImg.size}")
        print_rows_first_elem(np.array(zoomedImg), 1)
        plt.imshow(zoomedImg.convert('L'), cmap='gray')
        plt.title("Zoomed Image")
        plt.axis('on')
        plt.show()
    except AssertionError as error:
        print(AssertionError.__name__ + ":", error)


if __name__ == '__main__':
    main()
