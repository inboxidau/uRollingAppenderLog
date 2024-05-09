sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import os
import sys
import unittest
from rolling_appender_log import URollingAppenderLog, LogLevel, LogOperationException


class TestURollingAppenderLog(unittest.TestCase):

    def test_log_message(self):
        # Test log message writing
        log_file = "test_log.txt"
        logger = URollingAppenderLog(log_file, max_file_size_bytes=100, max_backups=2, print_messages=False)
        logger.log_message("Test message", level=LogLevel.INFO)
        self.assertTrue(os.path.exists(log_file))

        # Cleanup
        os.remove(log_file)

    def test_log_message_print(self):
        # Test log message writing with print_messages=True
        log_file = "test_log.txt"
        logger = URollingAppenderLog(log_file, max_file_size_bytes=100, max_backups=2, print_messages=True)
        logger.log_message("Test message", level=LogLevel.INFO)
        self.assertTrue(os.path.exists(log_file))

        # Cleanup
        os.remove(log_file)

    def test_log_message_exception(self):
        # Test log message writing exception
        log_file = "non_existing_folder/test_log.txt"
        logger = URollingAppenderLog(log_file, max_file_size_bytes=100, max_backups=2, print_messages=False)
        with self.assertRaises(LogOperationException):
            logger.log_message("Test message", level=LogLevel.INFO)

    def test_roll_over_backups(self):
        # Test backup rotation
        log_file = "test_log.txt"
        test_max_backups = 2
        logger = URollingAppenderLog(log_file, max_file_size_bytes=10, max_backups=test_max_backups, print_messages=True)
        logger.log_message("Test message 0", level=LogLevel.INFO)
        logger.log_message("Test message 1", level=LogLevel.INFO)
        logger.log_message("Test message 2", level=LogLevel.INFO)
        logger.log_message("Test message 3", level=LogLevel.INFO)                

        backups = logger.existing_backups
        self.assertEqual(len(backups), test_max_backups)

        # Cleanup
        os.remove(log_file)
        for backup_file in backups:
            os.remove(backup_file)


if __name__ == '__main__':
    unittest.main()
