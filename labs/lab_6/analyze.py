import os

# --- Configuration ---
BLOCK_SIZE = 16       # AES block size is 16 bytes
HEADER_OFFSET = 64    # Skip the 64-byte garbled header
INPUT_FILE = "aes.bmp.enc" # The encrypted file

# --- Analysis Logic ---

def analyze_file(filename):
    """Analyzes the encrypted file and returns metadata about it."""
    
    print(f"Analyzing file: {filename}")
    print("=" * 50)
    
    # Read the binary file
    with open(filename, "rb") as f:
        f.seek(HEADER_OFFSET) # Skip the header
        data = f.read()
    
    # Get file information
    file_size = len(data)
    print(f"File data size (after header): {file_size} bytes")
        
    # Process binary data into blocks
    blocks = []
    for i in range(0, file_size, BLOCK_SIZE):
        block = data[i:i+BLOCK_SIZE]
        # Stop if we have a partial block at the end
        if len(block) < BLOCK_SIZE:
            break
        blocks.append(block)
    
    num_blocks = len(blocks)
    print(f"Total blocks processed: {num_blocks}")
    
    # Find possible widths (factors)
    print("\nCalculating possible image dimensions...")
    possible_widths = []
    for width in range(1, int(num_blocks**0.5) + 1):
        if num_blocks % width == 0:
            height = num_blocks // width
            if width == 1 or height == 1:
                continue
            possible_widths.append((width, height))
    
    possible_widths = sorted(list(set(possible_widths)))
    
    print(f"\nTotal pixels (blocks): {num_blocks}")
    print("\nPossible image dimensions:")
    print("-" * 50)    
    for width, height in possible_widths:
        print(f"  {width} × {height}")
    print("-" * 50)
    print("\nUse visualize.py with one of these widths to create the image.")

if __name__ == "__main__":
    # Check if file exists
    if not os.path.exists(INPUT_FILE):
        print(f"Error: File '{INPUT_FILE}' not found!")
        exit(1)
    
    analyze_file(INPUT_FILE)

