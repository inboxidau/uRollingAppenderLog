import os

class LogLevel:
    ERROR = 1
    DEBUG = 2
    INFO = 3
    
class URollingAppenderLog:
    def __init__(self, log_file, max_file_size_bytes=4 * 20, max_backups=5, print_messages=False, log_level=LogLevel.INFO):
        # if log_level is set to LogLevel.DEBUG then the class will emit its own debug information as "CONSOLE:" only to stdout
        if max_backups < 0:
            raise ValueError("max_backups must be greater than or equal to zero.")        
        self.log_file = log_file
        self.max_file_size_bytes = max_file_size_bytes
        self.max_backups = max_backups
        self.print_messages = print_messages
        self.log_level = log_level

    def get_next_backup_index(self):
        backup_index = 1

        while f"{self.log_file}.{backup_index}" in self.existing_backups:
            backup_index += 1
        if self.print_messages == True and self.log_level == LogLevel.DEBUG:
            print(f"CONSOLE: get_next_backup_index = {backup_index}")
        return backup_index


    def roll_over_backups(self):
        try:        
            if self.max_backups == 0 :
                # If max_backups is set to 0, delete all existing backup files
                for backup_file in [f for f in os.listdir() if f.startswith(f"{self.log_file}.")]:
                    if self.print_messages == True and self.log_level == LogLevel.DEBUG:
                        print(f"CONSOLE: remove {backup_file}")
                    os.remove(backup_file)
                self.existing_backups = []
            else:
                self.existing_backups = [f for f in os.listdir() if f.startswith(f"{self.log_file}.")]

                # Find the file with the largest index and remove it
                while len(self.existing_backups) >= self.max_backups:
                    largest_backup_index = max([int(f.split('.')[-1]) for f in self.existing_backups])
                    largest_backup = f"{self.log_file}.{largest_backup_index}"
                    if self.print_messages == True and self.log_level == LogLevel.DEBUG:
                        print(f"CONSOLE: remove {largest_backup}")                
                    os.remove(largest_backup)
                    self.existing_backups.remove(largest_backup)

                # Rename the remaining files in descending order
                for backup_index in sorted([int(f.split('.')[-1]) for f in self.existing_backups], reverse=True):
                    old_backup = f"{self.log_file}.{backup_index}"
                    new_backup = f"{self.log_file}.{backup_index + 1}"
                    if self.print_messages == True and self.log_level == LogLevel.DEBUG:
                        print(f"CONSOLE: rename {old_backup} to {new_backup}")                
                    os.rename(old_backup, new_backup)

                # rename the current file
                if self.print_messages == True and self.log_level == LogLevel.DEBUG:
                    print(f"CONSOLE: rename {self.log_file} to {self.log_file}.1")             
                os.rename(self.log_file, f"{self.log_file}.1")

                # Adjust the list of existing backups after renaming
                self.existing_backups = [f"{self.log_file}.{i}" for i in range(1, self.get_next_backup_index())]
        
        except OSError as e:
            error_message = f"Error during backup rotation: {e}"
            print(f"CONSOLE: {error_message}")
            raise LogOperationException(error_message)
        
        return self.existing_backups

    def log_message(self, message, level=LogLevel.INFO, TID="0000-00-00T00:00:00Z"): #, TID="0000-00-00T00:00:00Z"
        display_message = False
        if self.log_level == LogLevel.INFO and level in (LogLevel.ERROR, LogLevel.INFO):
            display_message = True
        elif self.log_level == LogLevel.DEBUG and level in (LogLevel.ERROR, LogLevel.DEBUG, LogLevel.INFO):
            display_message = True
        elif self.log_level == LogLevel.ERROR and level == LogLevel.ERROR:
            display_message = True

        if level == LogLevel.INFO:
            prefix = "INFO"
        elif level == LogLevel.DEBUG:
            prefix = "DEBUG"
        elif level == LogLevel.ERROR:
            prefix = "ERROR"
        else:
            prefix = "UNKNOWN"

        message = f"TID:{TID}-{prefix}-{message}"
            
        if display_message == True:    
            if self.print_messages == True:
                print(message)

            self.existing_backups = [f for f in os.listdir() if f.startswith(f"{self.log_file}.")]

            # Check if the log file exists and if its size exceeds the limit
            if self.log_file in os.listdir():
                log_file_size = os.stat(self.log_file)[6]  # Index 6 corresponds to the size in the os.stat result
                if log_file_size > self.max_file_size_bytes:
                    # Roll over backups if the maximum number is reached
                    self.roll_over_backups()

            try:
                # Open the log file in append mode and write the message
                with open(self.log_file, 'a') as file:
                    file.write(message + '\n')
            except OSError as e:
                error_message = f"Error during log_message() {e}"
                print(f"CONSOLE: {error_message}")
                raise LogOperationException(error_message)

