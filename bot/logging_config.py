# Simple logging: writes to a timestamped file and console.
# Idempotent and closes handlers on exit to avoid leaking open files.

import logging
import os
import atexit
from datetime import datetime


_LOG_FILENAME = None
_HANDLERS_ADDED = False

# Cleanup: remove and close handlers when the program exits
def _close_handlers(root, handlers):
    for h in list(handlers):
        try:
            root.removeHandler(h)
            h.close()
        except Exception:
            pass


def setup_logging():
    # Set up logging once: write to a timestamped file and to the console
    global _LOG_FILENAME, _HANDLERS_ADDED

    root = logging.getLogger()
    if _HANDLERS_ADDED:
        return _LOG_FILENAME

    # If root already has handlers (e.g., a test harness), keep them
    if root.handlers:
        _HANDLERS_ADDED = True
        return _LOG_FILENAME

    if not os.path.exists('logs'):
        os.makedirs('logs')

    _LOG_FILENAME = f"logs/trading_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    fh = logging.FileHandler(_LOG_FILENAME, delay=True)
    sh = logging.StreamHandler()

    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    fh.setLevel(logging.INFO)
    sh.setLevel(logging.INFO)

    root.setLevel(logging.INFO)
    root.addHandler(fh)
    root.addHandler(sh)

    # Close handlers on program exit to free resources
    atexit.register(_close_handlers, root, [fh, sh])

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {_LOG_FILENAME}")

    _HANDLERS_ADDED = True
    return _LOG_FILENAME
