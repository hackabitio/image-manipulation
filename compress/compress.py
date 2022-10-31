import os
from PIL import Image

def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format for printing results only
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

def compress_img(image_name, new_size_ratio=9.0, quality=90, width=None, height=None, to_jpg=False, to_webp=False, convert=None, dpi=None, toMM=False):
    # load the image to memory
    img = Image.open(image_name)
    # print the original image shape
    print("[*] Image shape:", img.size)
    # get the original image size in bytes
    image_size = os.path.getsize(image_name)
    # print the size before compression/resizing
    print("[*] Size before compression:", get_size_format(image_size))
    if toMM and dpi:
        if width and height:
            width = int((dpi / 25.4) * width)
            height = int((dpi / 25.4) * height)
        else:
            width = int((dpi / 25.4) * img.size[0])
            height = int((dpi / 25.4) * img.size[1])
    if new_size_ratio < 1.0:
        # if resizing ratio is below 1.0, then multiply width & height with this ratio to reduce image size
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
        # print new image shape
        print("[+] New Image shape:", img.size)
    elif width and height:
        # if width and height are set, resize with them instead
        img = img.resize((width, height), Image.ANTIALIAS)
        # print new image shape
        print("[+] New Image shape:", img.size)
    # split the filename and extension
    filename, ext = os.path.splitext(image_name)
    # make new filename appending _compressed to the original file name
    if to_jpg:
        # change the extension to JPEG
        new_filename = f"{filename}_compressed.jpg"
    elif to_webp:
        new_filename = f"{filename}.webp"
    else:
        # retain the same extension of the original image
        new_filename = f"{filename}_compressed{ext}"
    # If convert provided, try to convery the image
    if convert:
        print("[*] Images original mode:", img.mode)
        img = img.convert(convert, palette=Image.Palette.WEB, colors=256)
    try:
        # save the image with the corresponding quality and optimize set to True
        if dpi:
            img.save(new_filename, quality=quality, optimize=True, dpi=(dpi,dpi))
        else:
            img.save(new_filename, quality=quality, optimize=True)
    except OSError:
        # convert the image to RGB mode first
        img = img.convert("RGB")
        # save the image with the corresponding quality and optimize set to True
        img.save(new_filename, quality=quality, optimize=True)
    print("[+] New file saved:", new_filename)
    # get the new image size in bytes
    new_image_size = os.path.getsize(new_filename)
    # print the new size in a good format
    print("[+] Size after compression:", get_size_format(new_image_size))
    # calculate the saving bytes
    saving_diff = new_image_size - image_size
    # print the saving percentage
    print(f"[+] Image size change: {saving_diff/image_size*100:.2f}% of the original image size.")

def scan_dir(path, args):
    images = os.listdir(path)
    for image in images:
        if image != '.DS_Store':
            image_path = path + image
            print("-"*50)
            compress_img(image_path, args.resize_ratio, args.quality, args.width, args.height, args.to_jpg, args.to_webp, args.convert, args.dpi, args.mm)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple Python script for compressing and resizing images")
    parser.add_argument("image", help="Target image to compress and/or resize")
    parser.add_argument("-j", "--to-jpg", action="store_true", help="Whether to convert the image to the JPEG format")
    parser.add_argument("-p", "--to-webp", action="store_true", help="Whether to convert the image to the webp format")
    parser.add_argument("-d", "--directory", action="store_true", help="Whether scan directory or single image")
    parser.add_argument("-q", "--quality", type=int, help="Quality ranging from a minimum of 0 (worst) to a maximum of 95 (best). Default is 90", default=90)
    parser.add_argument("-r", "--resize-ratio", type=float, help="Resizing ratio from 0 to 1, setting to 0.5 will multiply width & height of the image by 0.5. Default is 1.0", default=1.0)
    parser.add_argument("-w", "--width", type=int, help="The new width image, make sure to set it with the `height` parameter")
    parser.add_argument("-hi", "--height", type=int, help="The new height for the image, make sure to set it with the `width` parameter")
    parser.add_argument("-dpi", "--dpi", type=int, help="New Image DPI (Dots per inch)")
    parser.add_argument("-mm", "--mm", action="store_true", help="Set width and height as MM instead of pixels")
    parser.add_argument("-c", "--convert", type=str, help="Whether to convert the PNG mode or not. Possible values are: `1`, `L`, `LA`, `P`, `PA`, `RGB`, `RGBA`, `CMYK`")
    args = parser.parse_args()
    # print the passed arguments
    print("="*50)
    if args.directory:
        print("[*] Directory:", args.image)
    else:
        print("[*] Image:", args.image)
    print("[*] To JPEG:", args.to_jpg)
    print("[*] To webp:", args.to_webp)
    print("[*] Quality:", args.quality)
    print("[*] Resizing ratio:", args.resize_ratio)
    if args.width and args.height:
        print("[*] Width:", args.width)
        print("[*] Height:", args.height)
    print("="*50)
    # compress the image
    if args.directory:
        scan_dir(args.image, args)
    else:
        compress_img(args.image, args.resize_ratio, args.quality, args.width, args.height, args.to_jpg, args.to_webp, args.convert, args.dpi, args.mm)