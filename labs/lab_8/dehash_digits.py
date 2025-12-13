import hashlib
import time

def crack_digit_passwords():
    """
    Attempts to crack the 5-7 digit passwords from the lab.
    """
    # The salt identified from the case files [cite: 16, 17, 19]
    salt = "www.exploringsecurity.com"
    
    # Target hashes for users modified BEFORE May 2010
    # security: fafa4483874ec051989d53e1e432ba3a6c6b9143 
    # Tomtom:   06f6fe0f73c6e197ee43eff4e5f7d10fb9e438b2 
    targets = {
        "fafa4483874ec051989d53e1e432ba3a6c6b9143": "security",
        "06f6fe0f73c6e197ee43eff4e5f7d10fb9e438b2": "Tomtom"
    }

    print(f"[*] Starting attack...")
    print(f"[*] Salt: {salt}")
    print(f"[*] Policy: 5-7 digits only ")
    print(f"[*] Targets: {list(targets.values())}\n")
    
    start_time = time.time()

    # Loop through all numbers from 10000 (5 digits) to 9999999 (7 digits)
    for num in range(10000, 10000000):
        
        password_guess = str(num)
        
        # 1. Format: CommonHash($salt,$pass) 
        salted_pass_str = salt + password_guess
        
        # 2. Encode to bytes for hashing
        salted_pass_bytes = salted_pass_str.encode('utf-8')
        
        # 3. Hash using SHA-1 (implied by 40-char length and MySQL [cite: 18, 24])
        hash_obj = hashlib.sha1(salted_pass_bytes)
        calculated_hash = hash_obj.hexdigest()
        
        # 4. Check if the hash matches any of our targets
        if calculated_hash in targets:
            user = targets[calculated_hash]
            print(f"\n[+] SUCCESS!")
            print(f"  User:     {user}")
            print(f"  Password: {password_guess}")
            print(f"  Hash:     {calculated_hash}\n")
            
            # Remove from dict so we don't keep checking
            del targets[calculated_hash]

        # Stop if we've found all targets in this group
        if not targets:
            break
            
    end_time = time.time()
    print(f"[*] Attack finished in {end_time - start_time:.2f} seconds.")

# Run the function
crack_digit_passwords()