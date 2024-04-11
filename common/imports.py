from typing import Dict, List, Set, Union, Tuple

from icecream import ic
ic.configureOutput(includeContext=True)


import logging
logging.basicConfig(
    level=logging.CRITICAL,
    format='%(levelname)s: %(filename)s - %(funcName)s - line %(lineno)d'
           '\n\t%(message)s'
)
# Create logger for your package or module
lg = logging.getLogger(__name__)