from tools import coroutine


@coroutine
def eifc(decryptor):
    while True:
        new_obj = yield
        print "Create PyDrive object"
        print "Download file content"
        print "Save file"

        decryptor.send("Hello Decryptor")


@coroutine
def decryptor(dfc):
    while True:
        new_obj = yield

        print "Decrypt file name + contents"
        print "Save file contents under decrypted name"
        print "Remove encrypted file."

        dfc.send("Hello DFC")


@coroutine
def dfc_new():
    while True:
        new_file = yield

        print "Copy file to DFC folder."
        print "register file as present."
        print "Evict files from cache as necessary."


def cli(_dfc_request):
    while True:
        new_command = raw_input("Input your command: ")
        print "Command typed in"

        _dfc_request.send("New file request.")


@coroutine
def dfc_request(encryptor):
    while True:
        new_request = yield

        print "Determine change type."
        print "Update LRU status"

        encryptor.send("Encrypt file or file properties.")


@coroutine
def encryptor(eofc):
    while True:
        element_to_encrypt = yield

        print "Encrypt file name + content"
        print "Move file to eofc"

        eofc.send("New file to upload.")


@coroutine
def eofc():
    while True:
        element_to_upload = yield

        print "Upload file {}".format(element_to_upload)
        print "Delete encrypted file."


if __name__ == '__main__':
    _eofc = eofc()
    _encryptor = encryptor(_eofc)
    _dfc_request = dfc_request(_encryptor)
    cli(_dfc_request)
