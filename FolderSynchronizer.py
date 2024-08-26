import logging
import hashlib
import os
import shutil
import time

class FolderSynchronizer:
    def __init__(self, source, backup, log_file):
        print("FolderSynchronizer")
        self.source = source
        self.backup = backup
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
                self.sync_folders()
                logging.info("Synchronization complete.")
                time.sleep(interval)
        except KeyboardInterrupt:
            logging.info("Folder synchronization terminated.")

    def sync_folders(self):
        self.sync_directories()
        self.sync_files()

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

    def get_all_directories(self, root):
        """Get all directories in the directory tree."""
        return set(
            os.path.relpath(dirpath, root)
            for dirpath, _, _ in os.walk(root)
        )

    def sync_files(self):
        """synchronization of all files"""
        source_files = self.get_all_files(self.source)
        backup_files = self.get_all_files(self.backup)

        files_to_copy = source_files - backup_files
        files_to_delete = backup_files - source_files
        files_to_update = filter(
            lambda f: self.needs_update(f),
            source_files & backup_files
        )

        # Copy new files from source to backup
        list(map(lambda f: self.copy_file(f), files_to_copy))

        # Update modified files in backup
        list(map(lambda f: self.copy_file(f), files_to_update))

        # Delete files from backup that don't exist in source
        list(map(lambda f: self.remove_file(f), files_to_delete))

    def sync_directories(self):
        """synchronization of all directories"""
        source_dirs = self.get_all_directories(self.source)
        backup_dirs = self.get_all_directories(self.backup)

        dirs_to_create = source_dirs - backup_dirs
        dirs_to_delete = backup_dirs - source_dirs

        # Create directories that exist in source but not in backup
        list(map(lambda d: self.create_directory(d), dirs_to_create))

        # Remove directories that exist in backup but not in source
        list(map(lambda d: self.remove_directory(d), dirs_to_delete))

    def needs_update(self, rel_path):
        source_file = os.path.join(self.source, rel_path)
        backup_file = os.path.join(self.backup, rel_path)
        return self.calculate_md5(source_file) != self.calculate_md5(backup_file)

    """************** Files Service Helper Methods ***********************"""
    def copy_file(self, relative_path):
        source_file = os.path.join(self.source, relative_path)
        backup_file = os.path.join(self.backup, relative_path)
        shutil.copy2(source_file, backup_file)
        logging.info(f"File copied/updated: {relative_path}")

    def remove_file(self, relative_path):
        os.remove(os.path.join(self.backup, relative_path))
        logging.info(f"File deleted: {relative_path}")

    """************** Folders Service Helper Methods ***********************"""
    def create_directory(self, relative_path):
        try:
         os.makedirs(os.path.join(self.backup, relative_path))
        except:
         logging.info(f"Directory already exists: {relative_path}")
        logging.info(f"Directory created: {relative_path}")

    def remove_directory(self, relative_path):

        try:
         # Used shutil because os remove have problem with permisions
         shutil.rmtree(os.path.join(self.backup, relative_path))
         logging.info(f"Directory deleted: {relative_path}")
        except:
         logging.info(f"Directory removing failed {relative_path}")

