import sys
from PIL import Image

# Source file and output
if (len(sys.argv) != 3):
    print("Provide command line arguments: createImage.py INPUTFILE OUTPUTFILE")
    sys.exit(1)
file_path = sys.argv[1]
file_out = sys.argv[2]

# Read image data
with open(file_path, 'rb') as file:
    data = file.read()
    words = data.split()

# Date processing
img_format = words[0].decode("utf-8")
width = int(words[1])
height = int(words[2])
pixels = words[3:]
if (img_format == "HS8" or img_format == "HS16"):
    pixels = [item for sublist in pixels for item in sublist]

# Get the RGB colour values in (255,255,255) format
def get_colour_values(pixels):
    if (img_format == "HSHEX"):
        return [(int(pixels[i], 16) >> 8, int(pixels[i+1], 16) >> 8, int(pixels[i+2], 16) >> 8) for i in range(0, len(pixels), 3)]
    elif (img_format == "HSDEC" or img_format == "HS8"):
        return [(int(pixels[i]), int(pixels[i+1]), int(pixels[i+2])) for i in range(0, len(pixels), 3)]
    elif (img_format == "HS16"):
        return [((pixels[i] << 8 | pixels[i+1]) >> 8, (pixels[i+2] << 8 | pixels[i+3]) >> 8, (pixels[i+4] << 8 | pixels[i+5]) >> 8) for i in range(0, len(pixels), 6) if i + 5 < len(pixels)]


# Setup the image and pixel data
image = Image.new('RGB', (width, height), (0, 0, 0))
rgb_values = get_colour_values(pixels)
pixel_rows = [rgb_values[i*width:(i+1)*width] for i in range(height)]

# Put pixel data into the image en masse
image.putdata([pixel for row in pixel_rows for pixel in row])

# Save the image to a file
image.save(file_out)
