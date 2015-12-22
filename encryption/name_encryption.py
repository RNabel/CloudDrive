import base64
from Crypto.Cipher import AES
from Crypto import Random

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def encrypt(key, raw):
    """
    Encrypt a string.
    Args:
        key: Encryption key.
        raw: String to encrypt.

    Returns: The encrypted string.
    """
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw)).replace("/", "-")


def decrypt(key, enc):
    """
    Decrypt a string.
    Args:
        key: The encryption key.
        enc: The encrypted string.

    Returns: The decrypted string.

    """
    enc = enc.replace("-", "/")
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))
