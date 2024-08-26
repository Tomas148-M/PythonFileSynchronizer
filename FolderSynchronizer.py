import logging
import hashlib
import os

class FolderSynchronizer:
    def __init__(self, source, replica, log_file):
        print("FolderSynchronizer")
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

    def get_all_files(self, root):
        """Get all files in the directory tree"""
        return set(
            os.path.relpath(os.path.join(dirpath, file), root)
            for dirpath, _, files in os.walk(root)
            for file in files
        )