import skimage as ski
from skimage.metrics import structural_similarity
from skimage.metrics import mean_squared_error
import cv2
import numpy as np


def ssim(img1, img2):
    # Compute SSIM between the two images
    (score, diff) = structural_similarity(img1, img2, full=True)

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type in the range [0,1]
    # so we must convert the array to 8-bit unsigned integers in the range
    # [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")
    return score, diff

def mse(img1, img2):
    # Compute MSE between the two images
    mse = mean_squared_error(img1, img2)
    return mse

if __name__ == '__main__':
    # Load images
    img1 = cv2.imread('../OpenCV/Pics/desk1.JPG')
    img2 = cv2.imread('../OpenCV/Pics/desk2.JPG')

    # Convert images to grayscale
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    (score, diff) = ssim(img1_gray, img2_gray)
    print("Image Similarity: {:.4f}%".format(score * 100))

    # Threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    diff_box = cv2.merge([diff, diff, diff])
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(img1.shape, dtype='uint8')
    filled_after = img2.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img1, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.rectangle(img2, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.rectangle(diff_box, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.drawContours(mask, [c], 0, (255, 255, 255), -1)
            cv2.drawContours(filled_after, [c], 0, (0, 255, 0), -1)

    # cv2.imshow('before', img1)
    # cv2.imshow('after', img2)
    # cv2.imshow('diff', diff)
    # cv2.imshow('diff_box', diff_box)
    # cv2.imshow('mask', mask)
    cv2.imshow('filled after', filled_after)
    cv2.waitKey()





