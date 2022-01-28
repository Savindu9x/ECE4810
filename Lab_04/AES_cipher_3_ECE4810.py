# Written by Arief Budimen
# Reference: https://www.pycryptodome.org/en/latest/src/examples.html
# Import required libraries
from Crypto.Cipher import AES
from hashlib import sha256
from secrets import token_bytes

# Main block of the code
if __name__ == '__main__':
    # Return Random byte for AES-256
    private_key = sha256(token_bytes(32)).digest()
    # create cipher config
    cipher = AES.new(private_key, AES.MODE_GCM)
    # User Input plaintext
    password = input('plaintext: ').encode('utf-8')
    ciphertext, tag = cipher.encrypt_and_digest(password)
    # Prints Encrypted data
    print(f'\nciphertext: {ciphertext}')
    # Input for Decryption
    print(f'tag: {tag}')
    # Usually you would store ciphertext, tag, and nonce in a bin file or something similar
    # and load it again when needed.
    # create cipher config (Nonce is MAC for validity)
    cipher = AES.new(private_key, AES.MODE_GCM, cipher.nonce)
    # decrypt and output plaintext
    decrypted_password = cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
    print(f'\ndecrypted_plaintext: {decrypted_password}')
