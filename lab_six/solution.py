from PIL import Image
import numpy as np

data = open("aes.bmp.enc", "rb").read()

width, height = 512, 512   # matches your BMP header and analysis
arr = np.frombuffer(data[:width*height*3], dtype=np.uint8)
arr = arr.reshape((height, width, 3))

img = Image.fromarray(arr, "RGB")
img = img.transpose(Image.FLIP_TOP_BOTTOM)  # optional flip if upside-down
img.show()
img.save("unscrambled_guess.png")
print("Saved unscrambled_guess.png")


sizes = [(512,512), (640,480), (800,600), (1024,768)]
for w,h in sizes:
    try:
        arr = np.frombuffer(data[:w*h*3], dtype=np.uint8).reshape((h,w,3))
        img = Image.fromarray(arr, "RGB").transpose(Image.FLIP_TOP_BOTTOM)
        img.save(f"trial_{w}x{h}.png")
        print(f"Saved trial_{w}x{h}.png")
    except Exception as e:
        print(f"Failed {w}x{h}: {e}")