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
