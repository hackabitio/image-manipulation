from PIL import Image
import pytesseract
import numpy as np
import cv2 as cv


def read_image(image, args):
    img = np.array(Image.open(image))
    # Do some processing on the image
    norm_img = np.zeros((img.shape[0], img.shape[1]))
    img = cv.normalize(img, norm_img, args.alpha, args.beta, cv.NORM_MINMAX)
    img = cv.threshold(img, args.threshold_value, args.max_value, cv.THRESH_BINARY)[1]
    img = cv.GaussianBlur(img, (args.blur_value, args.blur_value), args.sigma_x)
    text = pytesseract.image_to_string(img)
    print(text)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple Python script for compressing and resizing images")
    parser.add_argument("image", help="Target image to compress and/or resize")
    parser.add_argument("-a", "--alpha", type=int, help="OpenCV normalize alpha", default=0)
    parser.add_argument("-b", "--beta", type=int, help="OpenCV normalize beta", default=255)
    parser.add_argument("-tv", "--threshold-value", type=int, help="OpenCV threshold Threshold Value", default=100)
    parser.add_argument("-mv", "--max-value", type=int, help="OpenCV threshold Max Value", default=255)
    parser.add_argument("-bl", "--blur-value", type=int, help="Value for GaussianBlur. Note that this must be odd number only", default=1)
    parser.add_argument("-sx", "--sigma-x", type=int, help="Gaussian kernel standard deviation in X direction.", default=0)
    args = parser.parse_args()

    print("="*50)
    read_image(args.image, args)
