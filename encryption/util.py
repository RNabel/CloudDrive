import hashlib
import secrets


def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = hashlib.md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length + iv_length]


def create_password(password):
    return hashlib.md5(password).digest()


def get_password():
    return create_password(secrets.password)
