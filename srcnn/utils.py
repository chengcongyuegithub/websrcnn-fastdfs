import numpy as np
import cv2 as cv
import scipy.misc
import scipy.ndimage


def modcrop(image, scale=3):
    if len(image.shape) == 3:
        h, w, _ = image.shape
        h = h - np.mod(h, scale)
        w = w - np.mod(w, scale)
        image = image[0:h, 0:w, :]
    else:
        h, w = image.shape
        h = h - np.mod(h, scale)
        w = w - np.mod(w, scale)
        image = image[0:h, 0:w]
    return image


# 归一化和还原
def im2double(im):
    info = np.iinfo(im.dtype)
    return im.astype(np.float) / info.max


def revert(im):
    im = im * 255
    im[im > 255] = 255
    im[im < 0] = 0
    return im.astype(np.uint8)


def preprocess_for_superresolution(img):
    img = np.array(img)
    im = cv.cvtColor(img, cv.COLOR_BGR2YCR_CB)
    img = im2double(im)
    label_ = modcrop(img, scale=1)
    color_base = modcrop(im, scale=1)
    color_base = color_base[:, :, 1:3]
    label_ = label_[:, :, 0]
    label_ = scipy.ndimage.interpolation.zoom(label_, (1. / 1), prefilter=False)
    label_ = scipy.ndimage.interpolation.zoom(label_, (1 / 1.), prefilter=False)
    data = np.array(label_).reshape([1, img.shape[0], img.shape[1], 1])
    color = np.array(color_base).reshape([1, img.shape[0], img.shape[1], 2])
    return data, color


def preprocess_for__upscaling(img, scale):
    im = np.array(img)
    size = im.shape
    im = scipy.misc.imresize(im, [size[0] * scale, size[1] * scale], interp='bicubic')
    im = cv.cvtColor(im, cv.COLOR_BGR2YCR_CB)
    img = im2double(im)
    label_ = modcrop(img, scale=1)
    color_base = modcrop(im, scale=1)
    color_base = color_base[:, :, 1:3]
    label_ = label_[:, :, 0]
    data = np.array(label_).reshape([1, im.shape[0], im.shape[1], 1])
    color = np.array(color_base).reshape([1, im.shape[0], im.shape[1], 2])
    return data, color
