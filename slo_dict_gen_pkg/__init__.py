from .entry_parser import SloleksEntry, WordForm, XMLParser
import os
import sys
from typing import Dict, List, Union

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

__all__ = ["formatting", "entry_parser", 'SloleksEntry', 'WordForm',
           'XMLParser', 'grammar_utilities', 'sys', 'os', "List", "Union", "Dict"]
