import simplecrypt


def encrypt_file(file_name, key):
    # Encrypt file content.
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = simplecrypt.encrypt(key, plaintext)

    # Encrypt file name.
    file_name_enc = encrypt(file_name, key)

    with open(file_name_enc, 'wb') as fo:
        fo.write(enc)


def decrypt_file(file_name, key):
    # Decrypt file contents.
    with open(file_name, 'rb') as fo:
        cipher_text = fo.read()
    dec = simplecrypt.decrypt(key, cipher_text)

    # Decrypt file name.
    file_name_enc = decrypt(file_name, key)

    with open(file_name_enc, 'wb') as fo:
        fo.write(dec)


def encrypt(input_string, key):
    return simplecrypt.encrypt(key, input_string)


def decrypt(input_string, key):
    return simplecrypt.decrypt(key, input_string)
