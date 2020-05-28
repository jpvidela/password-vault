from Crypto.Cipher import AES
import secrets


def encrypt(word, key):
    # Passwords must be 16 bytes long. Padding with '~' character if less.
    if len(word) % 16 != 0:
        word = word + (16 - len(word)) * '~'
    iv = secrets.token_bytes(16)
    aes = AES.new(key, AES.MODE_CBC, iv)
    encd = iv + aes.encrypt(word)
    return (encd)


def decrypt(encd, key):
    # Split encd: First 16 bytes are IV key, rest is password encrypted.
    encd_iv = encd[:16]
    encd_word = encd[16:]
    # Initialize new key
    aes = AES.new(key, AES.MODE_CBC, encd_iv)
    decd = aes.decrypt(encd_word)
    # Remove padding
    word = decd.decode('UTF-8').strip('~')
    return (word)
