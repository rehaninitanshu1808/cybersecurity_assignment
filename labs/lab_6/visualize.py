from PIL import Image
import random

# --- Configuration ---
BLOCK_SIZE = 16       # AES block size is 16 bytes
HEADER_OFFSET = 64    # Skip the 64-byte garbled header
INPUT_FILE = "aes.bmp.enc"
WIDTH = 241           # Image width from analyze.py
HEIGHT = 239          # Image height from analyze.py
OUTPUT_FILE = "unscrambled.png"

# --- Main Logic ---

print(f"Reading file: {INPUT_FILE}")

# Read the binary file
with open(INPUT_FILE, "rb") as f:
    f.seek(HEADER_OFFSET)
    data = f.read()

# Process binary data into blocks
blocks = []
for i in range(0, len(data), BLOCK_SIZE):
    block = data[i:i+BLOCK_SIZE]
    if len(block) < BLOCK_SIZE:
        break
    blocks.append(block)

num_blocks = len(blocks)

print(f"Total blocks: {num_blocks}")
print(f"Creating image: {WIDTH} × {HEIGHT}")

# Create a mapping of unique blocks to color indices
unique_blocks = {}
color_index = 0
for block in blocks:
    if block not in unique_blocks:
        unique_blocks[block] = color_index
        color_index += 1

# Create a palette with random RGB colors
random.seed(42)
palette = []
for i in range(max(256, len(unique_blocks))):
    palette.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

# Map each block to its corresponding color
pixel_colors = []
for block in blocks:
    index = unique_blocks[block]
    pixel_colors.append(palette[index])

# Create and save the image
img = Image.new('RGB', (WIDTH, HEIGHT))
img.putdata(pixel_colors)
img.save(OUTPUT_FILE)

print(f"✓ Image saved as: {OUTPUT_FILE}")

