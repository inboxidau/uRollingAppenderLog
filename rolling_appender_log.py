import os

class URollingAppenderLog:
    def __init__(self, log_file, max_file_size_bytes=4 * 20, max_backups=5):
        if max_backups < 0:
            raise ValueError("max_backups must be greater than or equal to zero.")        
        self.log_file = log_file
        self.max_file_size_bytes = max_file_size_bytes
        self.max_backups = max_backups

    def get_next_backup_index(self):
        backup_index = 1

        while f"{self.log_file}.{backup_index}" in self.existing_backups:
            backup_index += 1

        return backup_index

    def roll_over_backups(self):
        if self.max_backups == 0 :
            # If max_backups is set to 0, delete all existing backup files
            for backup_file in [f for f in os.listdir() if f.startswith(self.log_file + '.')]:
                os.remove(backup_file)
            self.existing_backups = []
        else:
            self.existing_backups = [f for f in os.listdir() if f.startswith(self.log_file + '.')]

            # Find the file with the largest index and remove it
            while len(self.existing_backups) >= self.max_backups:
                largest_backup_index = max([int(f.split('.')[-1]) for f in self.existing_backups])
                largest_backup = f"{self.log_file}.{largest_backup_index}"
                os.remove(largest_backup)
                self.existing_backups.remove(largest_backup)

            # Rename the remaining files in descending order
            for backup_index in sorted([int(f.split('.')[-1]) for f in self.existing_backups], reverse=True):
                old_backup = f"{self.log_file}.{backup_index}"
                new_backup = f"{self.log_file}.{backup_index + 1}"
                os.rename(old_backup, new_backup)

            # rename the current file
            os.rename(self.log_file, f"{self.log_file}.1")

            # Adjust the list of existing backups after renaming
            self.existing_backups = [f"{self.log_file}.{i}" for i in range(1, self.get_next_backup_index())]

        return self.existing_backups

    def log_message(self, message):
        self.existing_backups = [f for f in os.listdir() if f.startswith(self.log_file + '.')]

        # Check if the log file exists and if its size exceeds the limit
        if self.log_file in os.listdir():
            log_file_size = os.stat(self.log_file)[6]  # Index 6 corresponds to the size in the os.stat result
            if log_file_size > self.max_file_size_bytes:
                # Roll over backups if the maximum number is reached
                self.roll_over_backups()

        # Open the log file in append mode and write the message
        with open(self.log_file, 'a') as file:
            file.write(message + '\n')

