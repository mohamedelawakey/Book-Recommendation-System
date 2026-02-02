import logging
import os
from logging.handlers import (
    TimedRotatingFileHandler,
    QueueHandler,
    QueueListener
)
import threading
import queue
import json_log_formatter

BASE_LOG_DIR = os.path.join(os.getcwd(), "logs")
ML_LOG_DIR = os.path.join(BASE_LOG_DIR, "ml")
BACKEND_LOG_DIR = os.path.join(BASE_LOG_DIR, "backend")
SYSTEM_LOG_DIR = os.path.join(BASE_LOG_DIR, "system")

os.makedirs(ML_LOG_DIR, exist_ok=True)
os.makedirs(BACKEND_LOG_DIR, exist_ok=True)
os.makedirs(SYSTEM_LOG_DIR, exist_ok=True)

log_queue = queue.Queue()
json_formatter = json_log_formatter.JSONFormatter()


def _start_listener():
    handlers = {}
    for system_type, dir_path in [
        ('ml', ML_LOG_DIR),
        ('backend', BACKEND_LOG_DIR),
        ('system', SYSTEM_LOG_DIR)
    ]:
        log_file = os.path.join(dir_path, f"{system_type}.log")
        fh = TimedRotatingFileHandler(log_file, when='midnight', backupCount=30, encoding="utf-8")
        fh.setFormatter(json_formatter)
        handlers[system_type] = fh

    listener = QueueListener(log_queue, *handlers.values(), respect_handler_level=True)
    listener.start()


threading.Thread(target=_start_listener, daemon=True).start()


def get_logger(name: str, system_type: str = 'backend') -> logging.Logger:
    logger = logging.getLogger(f"{name}.{system_type}")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    queue_handler = QueueHandler(log_queue)
    logger.addHandler(queue_handler)

    return logger
