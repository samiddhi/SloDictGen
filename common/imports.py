from typing import Dict, List, Set, Union, Tuple, Optional

import os
proj_dir = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from icecream import ic
ic.configureOutput(includeContext=True)


import logging
logging.basicConfig(level=logging.DEBUG, encoding='utf-8')

# Create a file handler for critical messages
file_handler = logging.FileHandler('logfile.log')
file_handler.setLevel(logging.CRITICAL)

# Add a formatter to the file handler
formatter = logging.Formatter('%(levelname)s: %(filename)s - %(funcName)s - line %(lineno)d\n\t%(message)s')
file_handler.setFormatter(formatter)

# Remove the existing handlers from the root logger
logging.getLogger().handlers = []

# Add the file handler to the root logger
logging.getLogger().addHandler(file_handler)

# Test
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('I pooped')