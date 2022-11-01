import os
from rembg import remove
from PIL import Image
import cv2 as cv
import numpy as np

def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened

def remove_bg (image, alpha_matting = False, alpha_matting_erode = 15, brightness_alpha = 1.0, contrast_beta = 1, sharpen_kernel = 5, sharpen_sigma = 1.0, sharpen_amount = 1.0, sharpen_threshold = 0, save_image = False):
    print('Image source', alpha_matting)
    img = cv.imread(image)
    # im_arr = np.fromstring(img, np.uint8)
    # img = cv.imdecode(img, flags=cv.IMREAD_COLOR)
    img = cv.convertScaleAbs(img, alpha=brightness_alpha, beta=contrast_beta)
    img = unsharp_mask(img, sigma=float(sharpen_sigma), kernel_size=(int(sharpen_kernel), int(sharpen_kernel)), amount=float(sharpen_amount), threshold=int(sharpen_threshold))
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    output = remove(img, alpha_matting = alpha_matting, alpha_matting_erode_size = alpha_matting_erode)
    if save_image:
        cv.imwrite(image, output)
        cv.destroyAllWindows()
    else:
        img.show()
        output.show('Result')
        # cv.imshow("Original", img)
        # cv.imshow("Result", output)
        # cv.waitKey(0)
        # output.show()
        # cv.imshow("Result image", output)

def scan_dir(path, args):
    images = os.listdir(path)
    for image in images:
        if image != '.DS_Store':
            image_path = path + image
            print("-"*50)
            remove_bg (image_path, args.alpha_matting, args.alpha_matting_erode, args.brightness_alpha, args.contrast_beta, args.sharpen_kernel, args.sharpen_sigma, args.sharpen_amount, args.sharpen_threshold, args.save)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple Python script for compressing and resizing images")
    parser.add_argument("image", help="Target image to compress and/or resize")
    parser.add_argument("-am", "--alpha-matting", action="store_true", help="Enable alpha matting. This will result in better edges")
    parser.add_argument("-d", "--directory", action="store_true", help="If you want to apply to images in a directory")
    parser.add_argument("-s", "--save", action="store_true", help="Save result image instead of just showing it")
    parser.add_argument("-ame", "--alpha-matting-erode", type=int, help="Alpha matting erode size", default=15)
    parser.add_argument("-ba", "--brightness-alpha", type=float, help="Brighten image. Use a small number", default=1.0)
    parser.add_argument("-cb", "--contrast-beta", type=float, help="Contrast beta. Between 1.0 and 100", default=1.0)
    parser.add_argument("-sk", "--sharpen-kernel", type=int, help="Sharpenning kernel size. Note that it needs to be an odd number", default=5)
    parser.add_argument("-ss", "--sharpen-sigma", type=int, help="Sharpenning sigma value", default=1)
    parser.add_argument("-sa", "--sharpen-amount", type=float, help="Sharpenning amount. Between 0 and 20", default=1.0)
    parser.add_argument("-st", "--sharpen-threshold", type=float, help="Sharpenning threshold. Between 0 and 20", default=0)
    args = parser.parse_args()
    # print the passed arguments
    print("="*50)
    if args.directory:
        print("[*] Directory:", args.image)
    else:
        print("[*] Image:", args.image)

    print("[*] Alpha matting:", args.alpha_matting)
    print("[*] Apha matting erode size:", args.alpha_matting_erode)
    print("[*] Brightness alpha:", args.brightness_alpha)
    print("[*] Contrast beta:", args.contrast_beta)
    print("[*] Sharpenning kernal size:", args.sharpen_kernel)
    print("[*] Sharpenning sigma:", args.sharpen_sigma)
    print("[*] Shapenning amount:", args.sharpen_amount)
    print("[*] Sharpenning threshold:", args.sharpen_threshold)
    print("="*50)
    # compress the image
    if args.directory:
        scan_dir(args.image, args)
    else:
        remove_bg (args.image, args.alpha_matting, args.alpha_matting_erode, args.brightness_alpha, args.contrast_beta, args.sharpen_kernel, args.sharpen_sigma, args.sharpen_amount, args.sharpen_threshold, args.save)