from rembg import remove
from PIL import Image

input_path = '../images/lisa.png'
output_path = '../images/lisa-bg-removed.png'
input = Image.open(input_path)
output = remove(input)
output.save(output_path)