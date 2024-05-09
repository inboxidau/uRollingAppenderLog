import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest # noqa
from rolling_appender_log import URollingAppenderLog, LogLevel, LogOperationException # noqa


class TestAdvancedURollingAppenderLog(unittest.TestCase):

    def test_max_file_size_exceeded(self):
        # Test when the max file size is exceeded
        log_file = "test.log"
        max_file_size = 20  # Bytes
        logger = URollingAppenderLog(log_file, max_file_size_bytes=max_file_size, max_backups=2, print_messages=False)

        # Fill the log file to exceed the max file size
        with open(log_file, 'w') as file:
            # Write some content to exceed the max file size
            file.write("a" * (max_file_size + 10))

        # Log a message, this should trigger backup rotation
        logger.log_message("Test message", level=LogLevel.INFO)

        # Check if the backup file is created
        backups = [f for f in os.listdir() if f.startswith(f"{log_file}.")]
        self.assertGreater(len(backups), 0)

        # Cleanup
        os.remove(log_file)
        for backup_file in backups:
            os.remove(backup_file)

    def test_max_backups_zero(self):
        # Test when max_backups is set to zero
        log_file = "test.log"
        max_file_size = 20  # Bytes
        logger = URollingAppenderLog(log_file, max_file_size_bytes=max_file_size, max_backups=0, print_messages=False)

        # Fill the log file to exceed the max file size
        with open(log_file, 'w') as file:
            # Write some content to exceed the max file size
            file.write("a" * (max_file_size + 10))

        # Log a message, this should not trigger backup rotation
        logger.log_message("Test message", level=LogLevel.INFO)

        # Check if backup files are not created
        backups = [f for f in os.listdir() if f.startswith(f"{log_file}.")]
        self.assertEqual(len(backups), 0)

        # Cleanup
        os.remove(log_file)

    def test_log_message_debug(self):
        # Test log_message with LogLevel.DEBUG
        log_file = "test.log"
        logger = URollingAppenderLog(log_file, max_file_size_bytes=100, max_backups=2,
                                     print_messages=True, log_level=LogLevel.DEBUG)
        logger.log_message("Test debug message", level=LogLevel.DEBUG)
        logger.log_message("Test info message", level=LogLevel.INFO)

        # Check if messages are printed to the console
        # You may need to manually check the console output for this test

        # Cleanup
        os.remove(log_file)

    def test_log_message_exception(self):
        # Test log_message exception handling
        log_file = "non_existing_folder/test_log"
        logger = URollingAppenderLog(log_file, max_file_size_bytes=100, max_backups=2, print_messages=False)
        with self.assertRaises(LogOperationException):
            logger.log_message("Test message", level=LogLevel.INFO)

    def test_roll_over_backups_with_existing_backups(self):
        # Test backup rotation with existing backups
        log_file = "test.log"
        test_max_backups = 2
        some_content = "Some content"
        backups = [f"{log_file}.{i}" for i in range(1, (test_max_backups*6))]
        for backup_file in backups:
            with open(backup_file, 'w') as file:
                file.write(f"{some_content}")
        logger = URollingAppenderLog(log_file, max_file_size_bytes=len(some_content),
                                     max_backups=test_max_backups, print_messages=False)
        logger.log_message("Test message 0", level=LogLevel.INFO)
        logger.log_message("Test message 1", level=LogLevel.INFO)

        # Check if the backup files are rotated correctly
        new_backups = logger.existing_backups
        self.assertEqual(len(new_backups), test_max_backups)

        # Cleanup
        os.remove(log_file)
        for backup_file in new_backups:
            os.remove(backup_file)


if __name__ == '__main__':
    unittest.main()
