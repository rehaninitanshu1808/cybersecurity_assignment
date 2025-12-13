import string
import base64
import sys

def inverse_of_step_1(s):
    # Symmetric swap: applying the same translation table reverses it.
    input_seq = "zyxwvutsrqponZYXWVUTSRQPONmlkjihgfedcbaMLKJIHGFEDCBA"
    output_seq = "mlkjihgfedcbaMLKJIHGFEDCBAzyxwvutsrqponZYXWVUTSRQPON"
    return s.translate(str.maketrans(input_seq, output_seq))

def inverse_of_step_2(s):
    # Base64 decode
    return base64.b64decode(s).decode('utf-8')

def inverse_of_step_3(s):
    # Reverse shift: -4
    lower = string.ascii_lowercase
    shift = 4
    shifted = lower[shift:] + lower[:shift]
    return s.translate(str.maketrans(shifted, lower))

def solve():
    try:
        with open('intercepted.txt', 'r') as f:
            data = f.read().strip()
    except FileNotFoundError:
        print("Error: 'intercepted.txt' not found. Please make sure the file is in the same directory.")
        return

    layer = 1
    print(f"--- Starting Decryption (Initial Length: {len(data)}) ---\n")

    while True:
        indicator = data[0]
        content = data[1:]
        
        method_used = ""
        
        # Termination check: If the header isn't a valid step number, we have hit the plaintext.
        if indicator not in ('1', '2', '3'):
            print(f"-" * 60)
            print(f"[+] End of Encryption Reached at Layer {layer}")
            print(f"-" * 60)
            print(f"FINAL RECOVERED MESSAGE:\n{data}")
            return data
        
        # Apply the inverse operations based on the indicator
        if indicator == '1':
            data = inverse_of_step_1(content)
            method_used = "Step 1 (Reverse Transposition)"
        elif indicator == '2':
            data = inverse_of_step_2(content)
            method_used = "Step 2 (Base64 Decode)"
        elif indicator == '3':
            data = inverse_of_step_3(content)
            method_used = "Step 3 (Reverse Caesar Shift)"
        
        # Logging the step
        # We limit the print to 100 chars to keep the output readable
        preview = data[:100] + "..." if len(data) > 100 else data
        print(f"Layer {layer:02d} | Used: {method_used}")
        print(f"         Result: {preview}\n")

        layer += 1

if __name__ == "__main__":
    solve()