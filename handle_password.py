#IMPORTS
from cryptography.fernet import Fernet

#generate key
def generate_key():
    key = Fernet.generate_key()
    with open('python/secret.key', 'wb') as key_file:
        key_file.write(key)

#load it
def load_key():
    return open('python/secret.key', 'rb').read()

#encrypt the password
def encrypt_message(message, key):
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message

#decrypt the password
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()