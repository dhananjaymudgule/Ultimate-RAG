# logger.py
 
import logging
import os
from logging.handlers import RotatingFileHandler

#  Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

#  Log file path
LOG_FILE = os.path.join(LOG_DIR, "system.log")

#  Configure Rotating File Handler (max size 5MB, keep last 5 logs)
file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5  # 5MB per log, keep last 5 backups
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

#  Console Handler (Logs to terminal)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

#  Configure Logging
logging.basicConfig(
    level=logging.DEBUG,  # Log everything
    handlers=[file_handler, console_handler],  # Log to file + console
)

#  Logger Instance
logger = logging.getLogger(__name__)
