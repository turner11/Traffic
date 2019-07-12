import datetime
import logging
import os
import sys
import time
from pathlib import Path

import coloredlogs


def init_log(log_level=logging.DEBUG):
    """
    For initiating the logger.
    This should be called only once, by Main
    """
    now = time.time()
    ts = datetime.datetime.fromtimestamp(now).strftime('%Y%m%d')
    file_name = os.path.abspath(os.path.join(os.getcwd(), '..', 'traffic_logs', f'{ts}_traffic.log'))
    folder, _ = os.path.split(file_name)
    Path(folder).mkdir(parents=True, exist_ok=True)

    # create formatter and add it to the handlers
    log_format = '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'

    logging.basicConfig(filemode='a',
                        format=log_format,
                        datefmt='%H:%M:%S',
                        level=logging.ERROR,
                        stream=sys.stdout,
                        # filename=file_handler
                        )

    formatter = logging.Formatter(log_format)

    # create file handler which logs even debug messages
    file_handler = logging.FileHandler(file_name)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    std_out = logging.StreamHandler(sys.stdout)
    std_out.setFormatter(formatter)
    std_out.setLevel(log_level)

    # This for avoiding streams to log to root's stderr, which prints in red in jupyter
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        # continue
        root_logger.removeHandler(handler)

    # add the handlers to the logger
    root_logger.addHandler(file_handler)

    # By default the install() function installs a file_handler on the root root_logger,
    # this means that log messages from your code and log messages from the
    # libraries that you use will all show up on the terminal.
    coloredlogs.install(level=log_level, fmt=log_format, stream=sys.stdout)


def test_log():
    # init_log()
    local_logger = logging.getLogger(__name__)
    print('This is just a print')
    local_logger.debug("this is a debugging message")
    local_logger.info("this is an informational message")
    local_logger.warning("this is a warning message")
    local_logger.error("this is an error message")
    local_logger.critical("this is a critical message")


# init_log()
# test_log()
