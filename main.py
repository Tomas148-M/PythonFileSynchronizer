import argparse
from FolderSynchronizer import FolderSynchronizer

class FolderSynchronizerApp:
    def __init__(self):
        self.args = self.parse_arguments()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="Synchronize two folders.")
        parser.add_argument("--source", required=True, help="Path to the source folder")
        parser.add_argument("--backup", required=True, help="Path to the backup folder")
        parser.add_argument("--interval", type=int, required=True, help="Synchronization interval in seconds")
        parser.add_argument("--logfile", required=True, help="Path to the log file")
        return parser.parse_args()

    def runApp(self):
        synchronizer = FolderSynchronizer(self.args.source, self.args.backup, self.args.logfile)
        synchronizer.start_sync(self.args.interval)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = FolderSynchronizerApp()
    app.runApp()
