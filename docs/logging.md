# Python logging in cli context.

This setup has features:

-   name of module where it is used allows to identiffy file
-   logging to console and rotating file (10 MB, 3 files stored)
-   logging level for console and file independently
-   format '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
-   config dictionary
-   cache as making it safer for multiple run in modules

## This snippet is my current logging tool.

```python
#logger.py

from enum import Enum
import logging
import os
from typing import Any, Optional
from logging.handlers import RotatingFileHandler

class LoggerConfig(Enum):
    LOG_TO_FILE_FLAG = 1
    LOG_FILE_PATH = 2
    MAIN_LEVEL = 3
    CONSOLE_LEVEL = 4
    FILE_LEVEL = 5
    FORMAT = 6
    MAX_BYTES = 7
    BACKUP_COUNT = 8

_logger_cache = {}

def setup_logger(name: str, config: Optional[dict[LoggerConfig, Any]]=None) -> logging.Logger:
    if name in _logger_cache:
        return _logger_cache[name]

    default_log_to_file_flag = True
    default_log_file_path = 'logs/cli_tool.log'
    default_level = logging.INFO
    default_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    default_max_bytes = 10 * 1024 * 1024
    default_backup_count = 3

    default_config = {
        LoggerConfig.LOG_TO_FILE_FLAG: default_log_to_file_flag,
        LoggerConfig.LOG_FILE_PATH: default_log_file_path,
        LoggerConfig.MAIN_LEVEL: default_level,
        LoggerConfig.CONSOLE_LEVEL: default_level,
        LoggerConfig.FILE_LEVEL: default_level,
        LoggerConfig.FORMAT: default_format,
        LoggerConfig.MAX_BYTES: default_max_bytes,
        LoggerConfig.BACKUP_COUNT: default_backup_count,
    }

    config = {**default_config, **(config or {})}

    if config[LoggerConfig.MAX_BYTES] <= 0:
        raise ValueError(f"Invalid MAX_BYTES: {config[LoggerConfig.MAX_BYTES]}. It must be a positive integer.")
    if config[LoggerConfig.BACKUP_COUNT] < 0:
        raise ValueError(f"Invalid BACKUP_COUNT: {config[LoggerConfig.BACKUP_COUNT]}. It must be non-negative.")

    logger = logging.getLogger(name)
    logger.setLevel(config[LoggerConfig.MAIN_LEVEL])

    if not logger.handlers:
        formatter = logging.Formatter(config[LoggerConfig.FORMAT])

        console_handler = logging.StreamHandler()
        console_handler.setLevel(config[LoggerConfig.CONSOLE_LEVEL])
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if config[LoggerConfig.LOG_TO_FILE_FLAG]:
            log_file = config[LoggerConfig.LOG_FILE_PATH]

            log_dir = os.path.dirname(log_file)

            if log_dir:
                try:
                    os.makedirs(log_dir, exist_ok=True)
                except OSError as e:
                    logger.error(f"Failed to create log directory '{log_dir}': {e}")
                    raise

            try:
                file_handler = RotatingFileHandler(
                    log_file,
                    maxBytes=config[LoggerConfig.MAX_BYTES],
                    backupCount=config[LoggerConfig.BACKUP_COUNT]
                )
                file_handler.setLevel(config[LoggerConfig.FILE_LEVEL])
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                logger.error(f"Failed to set up file handler for log file '{log_file}': {e}")
                raise

        _logger_cache[name] = logger

    return logger
```

## This is a data model for logger config.

```python
import logging
from cli_tool.logger import LoggerConfig

LOGGER_CONFIG = {
    LoggerConfig.MAIN_LEVEL: logging.INFO,
    LoggerConfig.CONSOLE_LEVEL: logging.INFO,
    LoggerConfig.FILE_LEVEL: logging.INFO,
}
```

## This is a usage of logger in module.

```python
#some_module.py

from cli_tool.config import LOGGER_CONFIG
from logger import setup_logger

logger = setup_logger(__name__, LOGGER_CONFIG)
```

## Strengths:

1. **Module Identification**:

    - The use of the `name` parameter ensures that log entries can identify which module produced them. This is critical in applications with multiple modules.

2. **Configurable Logging**:

    - A `config` dictionary allows flexibility to adjust logging settings without modifying the core `setup_logger` function.

3. **Console and File Logging**:

    - The dual logging system ensures real-time visibility via the console and persistence for later debugging via files.

4. **Rotating File Handler**:

    - Rotating logs avoid bloated files and maintain a history with backups.

5. **Adjustable Log Levels**:

    - Independent log levels for the console and file handlers are a great touch for development versus production settings.

6. **Format String**:
    - The log format includes timestamp, module name, level, and message—perfect for debugging.
