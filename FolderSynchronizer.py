import logging
import hashlib

class FolderSynchronizer:
    def __init__(self, source, replica, log_file):
        self.source = source
        self.replica = replica
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format="%(asctime)s - %(message)s")
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        logging.getLogger().addHandler(console)

    def calculate_md5(self, file_path):
        """Calculate the MD5 checksum of a file."""
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()