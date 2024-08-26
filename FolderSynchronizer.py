import logging
import hashlib
import os
import shutil
import time

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

    def start_sync(self, interval):
        """the Main synchronization method"""
        logging.info("Starting folder synchronization...")
        try:
            while True:
                self.sync_files()
                logging.info("Synchronization complete.")
                time.sleep(interval)
        except KeyboardInterrupt:
            logging.info("Folder synchronization terminated.")


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

    def sync_files(self):
        source_files = self.get_all_files(self.source)
        replica_files = self.get_all_files(self.replica)

        files_to_copy = source_files - replica_files
        files_to_delete = replica_files - source_files
        files_to_update = filter(
            lambda f: self.needs_update(f),
            source_files & replica_files
        )

        # Copy new files from source to replica
        list(map(lambda f: self.copy_file(f), files_to_copy))

        # Update modified files in replica
        list(map(lambda f: self.copy_file(f), files_to_update))

    def needs_update(self, rel_path):
        source_file = os.path.join(self.source, rel_path)
        replica_file = os.path.join(self.replica, rel_path)
        return self.calculate_md5(source_file) != self.calculate_md5(replica_file)

    """************** Files Service Helper Methods ***********************"""
    def copy_file(self, relative_path):
        source_file = os.path.join(self.source, relative_path)
        replica_file = os.path.join(self.replica, relative_path)
        shutil.copy2(source_file, replica_file)
        logging.info(f"File copied/updated: {relative_path}")
