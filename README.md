# uRollingAppenderLog
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=inboxidau_uRollingAppenderLog&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=inboxidau_uRollingAppenderLog)

Simple micropython rolling appender logging.<P>

Send messages to the log file without fear of filling your storage space.

This class allows you to specify
- the name of the log file
- the maximum number of bytes you would like to log into a file
- how many backup versions of the log file you would like to maintain
- if you also want to print the messages to the console
- log_level

Backup files are given a suffix indicating how old they are. If max_backup is three then

- output.log   *(contains the newest log entries)*  
- output.log.1  *(contains old log entries)* 
- output.log.2  *(contains older log entries)* 
- output.log.3 *(contains oldest log entries)*  

Files will be deleted when they surpass the max_backups value

Log level allows you to specify both the importance of the logged message and also control which messages are displayed by the logger

| Log Level | Description                                                                                    |
|-----------|------------------------------------------------------------------------------------------------|
| DEBUG     | Detailed information, typically only of interest when diagnosing problems.                    |
| INFO      | Confirmation that things are working as expected.                                              |
| ERROR     | Due to a more serious problem, the software has not been able to perform some function.        |

The level assigned to the logger shows output

| Logger Level | DEBUG | INFO | ERROR |
|--------------|-------|------|-------|
| DEBUG        |   ✓   |   ✓  |   ✓   |
| INFO         |       |   ✓  |   ✓   |
| ERROR        |       |      |   ✓   |


✓ indicates that the corresponding log level will be output.<br>
Blank cells indicate that the corresponding log level will not be output.<br>
The rows represent the log level set for the logger instance.<br>
The columns represent the log levels of the messages.<br>

Messages are logged with the following pattern<P>
&nbsp;&nbsp;TID:{TID}-{prefix}-{message}

&nbsp;&nbsp;**where**<br>
&nbsp;&nbsp;&nbsp;&nbsp;TID: is a literal string denoting the start of a message.<br>
&nbsp;&nbsp;&nbsp;&nbsp;{TID} is the UTC timestamp supplied to the log_message function, defaulting to 0000-00-00T00:00:00Z **NOTE: the supplied TID is not validated**<br> 
&nbsp;&nbsp;&nbsp;&nbsp;{prefix} is a literal string representation of the log_level supplied to the log_message function.<br>
&nbsp;&nbsp;&nbsp;&nbsp;{message} is the message supplied to the log_message function.<br>
  
NOTE: Exceptions are not handled within the class and will propogate up the call stack.

```python
# test_logging_app.py

from rolling_appender_log import uRollingAppenderLog, LogLevel

# Instantiate the URollingAppenderLog class with default values
logger = URollingAppenderLog("logger.log")

# Instantiate the URollingAppenderLog class for debugging
logger2 = URollingAppenderLog("logger2.log", LogLevel.DEBUG)

# Instantiate the URollingAppenderLog class for recording only ERROR messages
logger2 = URollingAppenderLog("logger2.log", LogLevel.DEBUG)

# Log messages
logger.log_message("This is an info message.")
logger.log_message("This is another info message.", LogLevel.INFO)
logger.log_message("This is a debug message.", LogLevel.DEBUG)
logger.log_message("This is an error message.", LogLevel.ERROR)
logger.log_message("This is an error message with a specified TID.", LogLevel.ERROR, "2024-01-01T23:59:59Z")

# Log messages
logger2.log_message("This is an info message.")
logger2.log_message("This is another info message.", LogLevel.INFO)
logger2.log_message("This is a debug message.", LogLevel.DEBUG)
logger2.log_message("This is an error message.", LogLevel.ERROR)
logger2.log_message("This is an error message with a specified TID.", LogLevel.ERROR, "2024-01-01T23:59:59Z")
```

If you want to specify the maximum size of a log file in bytes along with the number of backup files or print messages you can adjust the instantiation

```python
# test_logging_app.py

from rolling_appender_log import uRollingAppenderLog, LogLevel

# Instantiate the URollingAppenderLog class with custom values
logger = URollingAppenderLog("test_log.log", max_file_size_bytes=1024, max_backups=3, print_messages=True, LogLevel.DEBUG)

# Log a message
logger.log_message("This is a test message.")

```
