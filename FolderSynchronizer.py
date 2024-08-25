class FolderSynchronizer:
    def __init__(self, source, replica, log_file):
        self.source = source
        self.replica = replica
        self.log_file = log_file