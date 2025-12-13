#!/usr/bin/env python3
"""
Hashcat-based password cracker for Lab 8
Uses GPU acceleration for much faster cracking than pure Python
"""

import subprocess
import os
import sys
import hashlib

def verify_hash(salt, password, expected_hash):
    """Verify that a password produces the expected hash."""
    salted = salt + password
    computed_hash = hashlib.sha1(salted.encode('utf-8')).hexdigest()
    return computed_hash == expected_hash

def check_hashcat_installed():
    """Check if hashcat is installed and accessible."""
    try:
        result = subprocess.run(
            ["hashcat", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            print(f"[*] Hashcat found: {version}\n")
            return True
        else:
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def create_hash_file(targets, salt, filename="hashes_to_crack.txt"):
    """Create hash file in format: hash:salt"""
    try:
        with open(filename, "w") as f:
            for hash_val in targets:
                f.write(f"{hash_val}:{salt}\n")
        print(f"[+] Created hash file: {filename}")
        print(f"    Format: hash:salt")
        print(f"    Entries: {len(targets)}\n")
        return True
    except IOError as e:
        print(f"[!] Error creating hash file: {e}")
        return False

def run_hashcat_attack(hash_file, potfile, lengths=[5, 6, 7]):
    """
    Run hashcat attack for specified password lengths.
    
    Mode 120: sha1($salt.$pass)
    Attack mode 3: Brute-force (mask attack)
    Charset ?l?u?d: lowercase + uppercase + digits (62 chars)
    """
    
    print("[*] Hashcat Configuration:")
    print(f"    Mode: 120 (sha1($salt.$pass))")
    print(f"    Attack: 3 (brute-force/mask)")
    print(f"    Charset: ?l?u?d (a-z, A-Z, 0-9 = 62 chars)")
    print(f"    Lengths: {lengths}\n")
    
    # Base command
    base_cmd = [
        "hashcat",
        "-m", "120",           # sha1($salt.$pass)
        "-a", "3",             # Brute-force attack
        hash_file,             # Input hash file
        "-1", "?l?u?d",        # Custom charset 1: lowercase + uppercase + digits
        f"--potfile-path={potfile}",
        "--quiet",             # Less verbose output
        "--status",            # Show status
        "--status-timer=10"    # Status every 10 seconds
    ]
    
    # Calculate search space
    print("[*] Search space per length:")
    total_combinations = 0
    for length in lengths:
        combinations = 62 ** length
        total_combinations += combinations
        print(f"    Length {length}: {combinations:,} ({combinations/1e9:.2f} billion)")
    print(f"    TOTAL: {total_combinations:,} ({total_combinations/1e9:.2f} billion)\n")
    
    # Run attack for each length
    for length in lengths:
        print(f"{'='*60}")
        print(f"[*] Attacking passwords of length {length}")
        print(f"{'='*60}\n")
        
        # Create mask (e.g., ?1?1?1?1?1 for length 5)
        mask = "?1" * length
        
        # Full command for this length
        cmd = base_cmd + [mask]
        
        print(f"[*] Command: {' '.join(cmd)}\n")
        
        try:
            # Run hashcat
            result = subprocess.run(
                cmd,
                capture_output=False,  # Show output in real-time
                text=True
            )
            
            # Hashcat returns:
            # 0 = Cracked
            # 1 = Exhausted (no match found)
            # 2 = Aborted (user interrupt)
            # -1 or -2 = Error
            
            if result.returncode == 0:
                print(f"\n[+] Length {length} attack completed - PASSWORD(S) FOUND!\n")
            elif result.returncode == 1:
                print(f"\n[*] Length {length} exhausted - no matches found.\n")
            elif result.returncode == 2:
                print(f"\n[!] Attack aborted by user.\n")
                return False
            else:
                print(f"\n[!] Hashcat error (code {result.returncode})\n")
                
        except KeyboardInterrupt:
            print("\n\n[!] Attack interrupted by user (Ctrl+C)")
            return False
        except Exception as e:
            print(f"\n[!] Error running hashcat: {e}")
            return False
    
    print(f"{'='*60}")
    print("[*] All attacks completed!")
    print(f"{'='*60}\n")
    return True

def parse_potfile(potfile, targets):
    """Parse the hashcat potfile and display results."""
    if not os.path.exists(potfile):
        print(f"[!] Potfile not found: {potfile}")
        return {}
    
    results = {}
    
    try:
        with open(potfile, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Potfile format: hash:salt:password
                parts = line.split(":")
                if len(parts) >= 3:
                    hash_val = parts[0]
                    password = ":".join(parts[2:])  # Handle passwords with ':'
                    
                    if hash_val in targets:
                        results[hash_val] = password
    
    except IOError as e:
        print(f"[!] Error reading potfile: {e}")
    
    return results

def main():
    """Main function to orchestrate the hashcat attack."""
    
    print("="*60)
    print("  Hashcat Password Cracker - Lab 8")
    print("="*60)
    print()
    
    # Configuration
    salt = "www.exploringsecurity.com"
    
    # Target hashes with usernames
    targets = {
        "2834da08d58330d8dafbb2ac1c0f85f6b3b135ef": "Sparky",
        "92e54f10103a3c511853c7098c04141f114719c1": "Mark123",
        "437fbc6892b38db6ac5bdbe2eab3f7bc924527d9": "superman",
        "f44f3b09df53c1c11273def13cacd8922a86d48c": "JillC"
    }
    
    hash_file = "hashes_to_crack.txt"
    potfile = "hashcat_results.pot"
    
    print("[*] Configuration:")
    print(f"    Salt: {salt}")
    print(f"    Algorithm: SHA-1(salt + password)")
    print(f"    Targets: {len(targets)} hashes")
    print(f"    Policy: 5-7 chars, alphanumeric\n")
    
    # Verify hash computation with known password
    print("[*] Verifying hash computation...")
    if verify_hash(salt, "Mark123", "92e54f10103a3c511853c7098c04141f114719c1"):
        print(f"    ✓ Hash verified with known password 'Mark123'\n")
    else:
        print(f"    ✗ Hash verification FAILED!\n")
        print("[!] Check salt or algorithm. Aborting.")
        return 1
    
    # Check if hashcat is installed
    if not check_hashcat_installed():
        print("[!] ERROR: hashcat not found!")
        print("    Please install hashcat:")
        print("    - macOS: brew install hashcat")
        print("    - Linux: sudo apt install hashcat")
        print("    - Or download from: https://hashcat.net/hashcat/")
        return 1
    
    # Create hash file
    if not create_hash_file(targets, salt, hash_file):
        return 1
    
    # Clean up old potfile if it exists
    if os.path.exists(potfile):
        print(f"[*] Removing old potfile: {potfile}\n")
        os.remove(potfile)
    
    # Run the attack
    print("[*] Starting hashcat attack...\n")
    input("Press Enter to start (or Ctrl+C to cancel)...")
    print()
    
    success = run_hashcat_attack(hash_file, potfile, lengths=[5, 6, 7])
    
    if not success:
        print("[!] Attack did not complete successfully.")
        return 1
    
    # Parse and display results
    print("\n" + "="*60)
    print("  RESULTS")
    print("="*60 + "\n")
    
    results = parse_potfile(potfile, targets)
    
    if results:
        print(f"[+] Successfully cracked {len(results)}/{len(targets)} passwords:\n")
        for hash_val, password in results.items():
            username = targets[hash_val]
            print(f"  ✓ {username:12} | Password: {password}")
            print(f"    Hash: {hash_val}")
            print()
        
        # Show uncracked hashes
        uncracked = set(targets.keys()) - set(results.keys())
        if uncracked:
            print(f"[*] {len(uncracked)} password(s) not cracked:")
            for hash_val in uncracked:
                username = targets[hash_val]
                print(f"  ✗ {username:12} | Hash: {hash_val}")
            print()
    else:
        print("[!] No passwords cracked.")
        print("    This might mean:")
        print("    - Passwords are longer than 7 characters")
        print("    - Passwords use characters outside a-z, A-Z, 0-9")
        print("    - Wrong salt or algorithm")
        print()
    
    print(f"[*] Results saved to: {potfile}")
    print(f"[*] Hash file: {hash_file}")
    print()
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user. Exiting.")
        sys.exit(1)

