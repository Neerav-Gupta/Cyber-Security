from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
from PIL import Image
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr

def aes_encrypt(plaintext, key):
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes (128 bits) long.")

    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

    encrypted = encryptor.update(padded_plaintext) + encryptor.finalize()

    return iv + encrypted

def aes_decrypt(encrypted_data, key):
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes (128 bits) long.")

    iv = encrypted_data[:16]
    encrypted = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

    return decrypted.decode()

def embed_lsb(image_path, data):
    image = Image.open(image_path)
    image = image.convert("RGB")
    np_image = np.array(image)
    flat_image = np_image.flatten()

    data_len = len(data)
    header = format(data_len, '032b')  # 32 bits to store the length of the data
    binary_data = ''.join(format(byte, '08b') for byte in data)
    binary_data = header + binary_data  # Prepend the header

    if len(binary_data) > len(flat_image):
        raise ValueError("Data is too large to be embedded in the image")

    for i in range(len(binary_data)):
        flat_image[i] = (flat_image[i] & 0xFE) | int(binary_data[i])

    np_image = flat_image.reshape(np_image.shape)
    stego_image = Image.fromarray(np_image)
    return stego_image

def extract_lsb(image_path):
    image = Image.open(image_path)
    np_image = np.array(image)
    flat_image = np_image.flatten()

    header = ''.join(str(flat_image[i] & 1) for i in range(32))  # Read the first 32 bits
    data_len = int(header, 2)  # Convert binary header to integer
    binary_data = ''.join(str(flat_image[i] & 1) for i in range(32, 32 + data_len * 8))
    data = bytes(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))
    return data

def encode():
    image_path = input("Enter the path to the cover image: ")
    plaintext = input("Enter the message to hide: ")
    key = os.urandom(16)
    print(f"Encryption key (keep this safe to decode): {key.hex()}")
    encrypted_data = aes_encrypt(plaintext, key)
    stego_image = embed_lsb(image_path, encrypted_data)
    encoded_image_path = input("Enter the name of the encoded image: ")
    stego_image.save(encoded_image_path, format="PNG")

    # PSNR Calculation
    original_image = Image.open(image_path)
    original_np_image = np.array(original_image)
    stego_np_image = np.array(stego_image)
    psnr_value = psnr(original_np_image, stego_np_image)
    print(f"PSNR: {psnr_value} dB")

def decode():
    image_path = input("Enter the path to the stego image: ")
    key = bytes.fromhex(input("Enter the encryption key: "))
    extracted_data = extract_lsb(image_path)
    decrypted_data = aes_decrypt(extracted_data, key)
    print(f"Decrypted Data: {decrypted_data}")

if __name__ == "__main__":
    command = input("What do you want to do? (1. encode/2. decode): ")
    if command == "1":
        encode()
    elif command == "2":
        decode()
    else:
        print("Invalid command.")
