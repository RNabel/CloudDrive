import hashlib
import secrets


def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = hashlib.md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length + iv_length]


def create_password(password):
    """
    Creates password of correct length by hashing the input password.
    Args:
        password: The human readable password.

    Returns: The hashed 32 character password.

    """
    return hashlib.md5(password).digest()


def get_password():
    """
    Return hashed password which is saved in secrets.
    Note: not to be called repeatedly!

    Returns: The hashed password.

    """
    # TODO Cache hashed password locally.
    return create_password(secrets.password)
