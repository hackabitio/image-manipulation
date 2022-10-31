# Compress Images in Python

To run this:
- `pip3 install -r requirements.txt`
- `python compress.py --help`

Boolean options:
- `-j`: Convert image to JPEG format
- `-p`: Convert image to webp format
- `-d`: Convert/compress all images within a directory
- `-mm`: Set width and height as millimeter insted of pixels. This is expecially useful if you want precise print dimensions

Options with value:
- `-q`: Quality from minimum of 0 and maximum of 95
- `-r`: Resizing by a ratio, values form 0 to 1
- `-w`: Width to resize to. Make sure to set with height
- `-hi`: Height to resize to. Make sure to set with width
- `-dpi`: Change image DPI (dopts per inch)
- `-c`: Convert image color space. Some possible values are; `1`, `L`, `LA`, `P`, `PA`, `RGB`, `RGBA`, `CMYK`


**credit**: https://github.com/x4nth055/pythoncode-tutorials/tree/master/python-for-multimedia/compress-image