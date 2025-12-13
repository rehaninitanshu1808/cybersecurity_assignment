LFSR1_SIZE = 12
LFSR1_TAPS = [5, 10]
LFSR2_SIZE = 19  
LFSR2_TAPS = [8, 14]

def lfsr_clock_byte(state, size, taps):
    # Clock the LFSR 8 times and return the output byte along with the new state.
    output = 0
    mask = (1 << size) - 1
    
    for i in range(8):
        output_bit = state & 1
        output |= output_bit << i
        
        feedback = 0
        for tap in taps:
            feedback ^= (state >> tap) & 1
        
        state = ((state >> 1) | (feedback << (size - 1))) & mask
    
    return output, state

def css_attack(known_keystream):
    # Recover both LFSR initial states using known keystream bytes (CSS-style attack).
    for reg1_state in range(1, 2**LFSR1_SIZE):
        out1_bytes = []
        state = reg1_state
        for _ in range(8):
            out, state = lfsr_clock_byte(state, LFSR1_SIZE, LFSR1_TAPS)
            out1_bytes.append(out)
        
        required_out2 = [(known_keystream[i] - out1_bytes[i]) % 255 for i in range(8)]
        
        reg2_candidate = 0
        bit_idx = 0
        for byte_val in required_out2:
            for b in range(8):
                if bit_idx < LFSR2_SIZE:
                    reg2_candidate |= ((byte_val >> b) & 1) << bit_idx
                    bit_idx += 1
        
        if reg2_candidate == 0:
            continue
            
        out2_bytes = []
        state = reg2_candidate
        for _ in range(8):
            out, state = lfsr_clock_byte(state, LFSR2_SIZE, LFSR2_TAPS)
            out2_bytes.append(out)
        
        if out2_bytes == required_out2:
            return reg1_state, reg2_candidate
    
    return None, None

def generate_keystream(reg1, reg2, length):
    # Generate the full keystream by combining outputs from both LFSRs.
    keystream = []
    r1, r2 = reg1, reg2
    for _ in range(length):
        o1, r1 = lfsr_clock_byte(r1, LFSR1_SIZE, LFSR1_TAPS)
        o2, r2 = lfsr_clock_byte(r2, LFSR2_SIZE, LFSR2_TAPS)
        keystream.append((o1 + o2) % 255)
    return keystream

def main():
    with open('flag.enc', 'rb') as f:
        encrypted = f.read()
    
    png_header = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
    known_keystream = [encrypted[i] ^ png_header[i] for i in range(8)]
    
    reg1, reg2 = css_attack(known_keystream)
    
    if reg1 is None:
        return
    
    keystream = generate_keystream(reg1, reg2, len(encrypted))
    decrypted = bytes([encrypted[i] ^ keystream[i] for i in range(len(encrypted))])
    
    with open('flag.png', 'wb') as f:
        f.write(decrypted)
    print("flag.png created successfully")

if __name__ == "__main__":
    main()
