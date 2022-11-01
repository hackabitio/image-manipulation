# Remove object background

Install dependencies:
- `pip3 install -r requirements.txt`

Remove background with [rembg](https://github.com/danielgatis/rembg) which is simple to use and quite powerfull and pillow:
`python remove-pil.py`

### With some options:
#### Boolean
- `-am`: Enable alpha matting. This usually result in better edges.
- `-d`:If you want to apply to images in a directory.
- `-s`: Save result image instead of just showing it.

#### non-boolean
- `-ame`: int, Alpha matting erode size, default=15
- `-ba`: float, Brighten image. Use a small number", default=1.0
- `-cb`: float, Contrast beta. Between 1.0 and 100", default=1.0
- `-sk`: int, Sharpenning kernel size. Note that it needs to be an odd number", default=5
- `-ss`: int, Sharpenning sigma value", default=1
- `-sa`: float, Sharpenning amount. Between 0 and 20", default=1.0
- `-st`: float, Sharpenning threshold. Between 0 and 20", default=0


Alternatively, using opencv. This method doesn't always work as intended though.
`python remove-cv.py`