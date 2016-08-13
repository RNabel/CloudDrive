class DownloadWorker:
    def __init__(self, file_obj, output_file_format="{file_id}_{id}", index=0, file_id=None):
        # Set up the parameters.
        if not file_id:
            file_id = file_obj['id']

        self.index = index
        self.file_obj = file_obj
        self.output_name_format = output_file_format

        self.output_file = output_file_format.format(file_id=file_id, id=index)
        print self.output_file

    def run(self):
        self.process()
        print "Thread {} finished.".format(self.index)

    def process(self):
        print "Processing {}...".format(self.index)
        try:
            self.file_obj.GetContentFile(self.output_file, mimetype='text/csv')
        except Exception as e:
            print e
        print "Processing done..."

    def get_file_name(self):
        return self.output_file
