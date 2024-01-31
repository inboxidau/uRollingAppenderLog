# uRollingAppenderLog
Simple micropython rolling appender logging.

Send messages to the log file without fear of filling your storage space.

This class allows you to specify
- the name of the log file
- the maximum number of bytes you would like to log into a file
- how many backup versions of the log file you would like to maintain

Backup files are given a siffix indicating how old they are. If max_backus is three then

- output.log   *(contains the newest log entries)*  
- output.log.1  *(contains old log entreies)* 
- output.log.2  *(contains older log entreies)* 
- output.log.3 *(contains oldest log entreies)*  

Files will be deleted when they surpass the max_backups value

Exceptions are not handled within the class and will propogate up the call stack.

```python
# test_logging_app.py

from rolling_appender_log import uRollingAppenderLog

# Instantiate the URollingAppenderLog class with default values
logger = URollingAppenderLog("default_log.log")

# Log a message
logger.log_message("This is a test message.")

```

If you want to specify the maximum size of a log file in bytes along with the number of backup files you can adjust the instantiation

```python
# test_logging_app.py

from rolling_appender_log import uRollingAppenderLog

# Instantiate the URollingAppenderLog class with custom values
logger = URollingAppenderLog("test_log.log", max_file_size_bytes=1024, max_backups=3)

# Log a message
logger.log_message("This is a test message.")

```
