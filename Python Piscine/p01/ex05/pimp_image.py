import numpy as np
from PIL import Image


def ft_invert(array):
    """
    Inverts the color of the image received.
    """
    image = 255 - array
    Image.fromarray(image).show()


def ft_red(array):
    """
    Keeps only the red color channel of the image.
    """
    red_channel = array[:, :, 0]
    image = np.zeros_like(array)
    image[:, :, 0] = red_channel
    Image.fromarray(image).show()


def ft_green(array):
    """
    Keeps only the green color channel of the image.
    """
    green_channel = array[:, :, 1]
    image = np.zeros_like(array)
    image[:, :, 1] = green_channel
    Image.fromarray(image).show()


def ft_blue(array):
    """
    Keeps only the blue color channel of the image.
    """
    blue_channel = array[:, :, 2]
    image = np.zeros_like(array)
    image[:, :, 2] = blue_channel
    Image.fromarray(image).show()


def ft_grey(array):
    """
    Converts the image to grayscale.
    """
    red_channel = array[:, :, 0] / 3
    green_channel = array[:, :, 1] / 3
    blue_channel = array[:, :, 2] / 3
    grey_channel = red_channel + green_channel + blue_channel
    grey_image = np.stack([grey_channel, grey_channel, grey_channel], axis=2)
    Image.fromarray(grey_image.astype(np.uint8)).show()
