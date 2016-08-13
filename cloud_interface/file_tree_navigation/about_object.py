from cloud_interface import drive


class AboutObject:
    def __init__(self):  # FIXME Need to wait for authentication.
        self.about = drive.auth.service.about().get().execute()

    def get_total_bytes(self):
        return int(self.about['quotaBytesTotal'])

    def get_used_bytes(self):
        return int(self.about['quotaBytesUsed'])
