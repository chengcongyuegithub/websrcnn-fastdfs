import numpy as np
import cv2 as cv
import scipy.misc
import scipy.ndimage

def modcrop_small(image):
    padding2 = 6
    if len(image.shape) == 3:
        h, w, _ = image.shape
        temp = h - 33 + 1
        if temp % 21 == 0:
            h = temp + padding2
        else:
            h = (h - 33 + 1) // 21 * 21 + 21 + padding2
        temp = w - 33 + 1
        if temp % 21 == 0:
            w = temp + padding2
        else:
            w = (w - 33 + 1) // 21 * 21 + 21 + padding2
        image1 = image[padding2:h, padding2:w, :]
    else:
        h, w = image.shape
        temp = h - 33 + 1
        if temp % 21 == 0:
            h = temp + padding2
        else:
            h = (h - 33 + 1) // 21 * 21 + 21 + padding2
        temp = w - 33 + 1
        if temp % 21 == 0:
            w = temp + padding2
        else:
            w = (w - 33 + 1) // 21 * 21 + 21 + padding2
        image1 = image[padding2:h, padding2:w]
    return image1

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


def merge(images, size):
    h, w = images.shape[1], images.shape[2]
    img = np.zeros((h * size[0], w * size[1], 1))
    for idx, image in enumerate(images):
        i = idx % size[1]
        j = idx // size[1]
        img[j * h:j * h + h, i * w:i * w + w, :] = image
    return img


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
    label_ = label_[:, :, 0]
    label_ = scipy.ndimage.interpolation.zoom(label_, (1. / 1), prefilter=False)
    label_ = scipy.ndimage.interpolation.zoom(label_, (1 / 1.), prefilter=False)
    color_small = modcrop_small(color_base[:, :, 1:3])
    return label_, color_small


def parpare_for_superresolution(sess, img):
    sub_input_sequence = []
    label_, color = preprocess_for_superresolution(img)
    if len(label_.shape) == 3:
        h, w, _ = label_.shape
    else:
        h, w = label_.shape
    nx = 0
    ny = 0
    for x in range(0, h - 33 + 1, 21):
        nx += 1
        ny = 0
        for y in range(0, w - 33 + 1, 21):
            ny += 1
            sub_input = label_[x:x + 33, y:y + 33]
            sub_input = sub_input.reshape([33, 33, 1])
            sub_input_sequence.append(sub_input)
    color = np.array(color)
    data = np.asarray(sub_input_sequence)
    return data, color, nx, ny


def preprocess_for__upscaling(img, scale):
    im = np.array(img)
    size = im.shape
    im = scipy.misc.imresize(im, [size[0] * scale, size[1] * scale], interp='bicubic')
    im = cv.cvtColor(im, cv.COLOR_BGR2YCR_CB)
    img = im2double(im)
    label_ = modcrop(img, scale=scale)
    color_base = modcrop(im, scale=scale)
    label_ = label_[:, :, 0]
    color_small = modcrop_small(color_base[:, :, 1:3])
    return label_, color_small


def parpare_for_upscaling(sess, img, scale):
    sub_input_sequence = []
    sub_label_sequence = []
    label_, color = preprocess_for__upscaling(img, scale)
    if len(label_.shape) == 3:
        h, w, _ = label_.shape
    else:
        h, w = label_.shape
    nx = 0
    ny = 0
    for x in range(0, h - 33 + 1, 21):
        nx += 1
        ny = 0
        for y in range(0, w - 33 + 1, 21):
            ny += 1
            sub_input = label_[x:x + 33, y:y + 33]
            sub_label = label_[x + 6:x + 6 + 21,
                        y + 6:y + 6 + 21]
            sub_input = sub_input.reshape([33, 33, 1])
            sub_label = sub_label.reshape([21, 21, 1])
            sub_input_sequence.append(sub_input)
            sub_label_sequence.append(sub_label)
    color = np.array(color)
    data = np.asarray(sub_input_sequence)
    label = np.asarray(sub_label_sequence)
    return data, label, color, nx, ny
