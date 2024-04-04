from typing import Dict, List, Set, Union
from icecream import ic


import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(filename)s - %(funcName)s - line %(lineno)d'
           '\n\t%(message)s'
)

# Create logger for your package or module
lg = logging.getLogger(__name__)