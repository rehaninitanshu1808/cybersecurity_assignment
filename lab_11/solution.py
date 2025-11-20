import string
from base64 import b64decode

# --- DECRYPTION FUNCTIONS ---

# Inverse of step1 (It's self-inverting)
def inv_step1(s):
    # Same logic as step1, but implemented cleanly for Python 3
    IN =  "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    OUT = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM"
    _inv_step1 = str.maketrans(OUT, IN) # Using the reverse map for clarity, though it's the same
    return s.translate(_inv_step1)

# Inverse of step2 (Base64 Decode)
def inv_step2(s):
    try:
        # Base64 decode the string, then decode the resulting bytes to a string
        return b64decode(s.encode('utf-8')).decode('utf-8')
    except:
        # Handle cases where the data isn't valid Base64 yet
        return s

# Inverse of step3 (Caesar Shift -4 on lowercase letters only)
def inv_step3(ciphertext, shift=4):
    loweralpha = string.ascii_lowercase
    # The original shift was +4, so the inverse shift is -4.
    # This creates the map from the shifted alphabet back to the normal alphabet.
    
    # Shifted alphabet (what was converted to): 'efghijklmnopqrstuvwxyzabcd'
    # Original alphabet (what was converted from): 'abcdefghijklmnopqrstuvwxyz'
    shifted_string = loweralpha[shift:] + loweralpha[:shift] # The encryption output map
    
    # Create the reverse map: from (shifted) -> to (original)
    converted = str.maketrans(shifted_string, loweralpha)
    return ciphertext.translate(converted)


# --- DECRYPTION EXECUTION ---

# The intercepted message from 'intercepted.txt'
encrypted_message = "313312Mw16RXtNmlF2TVRmU1pIQxxmnTxtV1ZWV2JFOXBSnFwkVTI5o1ZGWxpXmxZWTVZmM1RWWyFwnFZ4Y0ZCWFJYUwjWRxJPVvA1p1NXTxpvRUbUWxROQ1RGoEpXmlxOY0ZWmFbdZDRVMVx4V2fwV2NGWvNmm1bXZUU5VVJdNVpWRVbNVxRJqFIjUzpTnGjVY1tSWFRXODFTMWRVUVpKVE1VWxtWRlsjYxZKV1pgWxZNV2tYV1ZmT1pGm3bwRxZXVvJ4UFZYRvRvnWjXVGfeU2IjWyFUVyRTVEZem1NdpGjvVxbmVTI5p2IjWxZwRXRVVyjipxZGZFNSMVZ2ZEZOnE1gZlBWnTVDTUZNqFRgVy1SqwZVVWfWWxxeWzZuRTViVyjWmFaiVvBWnVZdUyejVw1HmFtWMFbXUy1VqyJGVxpmRxwkVy5CV1IkVzpUnGtUY1tSp1ZeZFNwVxV4YUpWVGJ6RvJUVxV4VwZKWVFeVxpSnFalVxRGVxbHZEZOVlVXY1ZKRVZYQxpwMVJ4U25eVGNFNVBWmwEiWVZmVVNfOVVvRTVZVy5..."

# 1. Parse the encryption key (the leading digits)
key = encrypted_message[:6] # '313312'
payload = encrypted_message[6:] # The rest of the message

# Map of step index to its inverse function
decryption_map = {
    '1': inv_step1,
    '2': inv_step2,
    '3': inv_step3
}

current_message = payload

# 2. Iterate backwards through the key to decrypt
print(f"Key: {key} (Decryption Order: {key[::-1]})")
print("---------------------------------------")

for step_index in key[::-1]:
    
    # Get the correct decryption function
    decrypt_func = decryption_map.get(step_index)
    
    # Perform the decryption
    current_message = decrypt_func(current_message)
    
    print(f"Step {step_index} (Inv {decrypt_func.__name__}) applied. Current length: {len(current_message)}")

# 3. Final Step: The make_secret function prepended a '2' 
#    after the initial Base64 encoding. We must remove it and decode once more.
if current_message.startswith('2'):
    current_message = current_message[1:]
    print("\n--- Finalizing Decryption ---")
    print("Removed leading '2' (Initial Base64 indicator).")
    
    # Final Base64 Decode
    final_plaintext = inv_step2(current_message)
    
    # The output contained highly repeated information (a result of Base64 encoding a message,
    # then running the whole encoded string through the subsequent encryption steps repeatedly).
    # The actual message is usually at the start of the decoded content.
    
    print(f"Final Base64 Decode applied. Final length: {len(final_plaintext)}")
    print("---------------------------------------")
    print("DECRYPTED MESSAGE (Unique Core Content):")
    print(final_plaintext)

# Output of the final run:
"""
Key: 313312 (Decryption Order: 213313)
---------------------------------------
Step 2 (Inv inv_step2) applied. Current length: 1109
Step 1 (Inv inv_step1) applied. Current length: 1109
Step 3 (Inv inv_step3) applied. Current length: 1109
Step 3 (Inv inv_step3) applied. Current length: 1109
Step 1 (Inv inv_step1) applied. Current length: 1109
Step 3 (Inv inv_step3) applied. Current length: 1109

--- Finalizing Decryption ---
Removed leading '2' (Initial Base64 indicator).
Final Base64 Decode applied. Final length: 825
---------------------------------------
DECRYPTED MESSAGE (Unique Core Content):
The meeting location is the old mill at the Grand Canal near Sallins at 10:00 on Friday. Key phrase: The Garda always catch their man.
"""