"""
Logging configuration for import-related operations.

This module configures a dedicated logger that writes informational
and higher-level messages to a file used during data import processes.
"""

import logging

# Create (or retrieve) a named logger for import operations
logger = logging.getLogger("import")

# Set the minimum log level for the logger
logger.setLevel(logging.INFO)

# Configure a file handler to write logs to a UTF-8 encoded file
handler = logging.FileHandler("import.log", encoding="utf-8")

# Define log message format with timestamp and severity level
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)

# Attach the formatter to the handler
handler.setFormatter(formatter)

# Prevent adding duplicate handlers if the module is imported multiple times
if not logger.handlers:
    logger.addHandler(handler)