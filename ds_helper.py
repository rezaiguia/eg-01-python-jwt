import os
import tempfile
from pprint import pprint

APP_PATH = os.path.dirname(os.path.abspath(__file__))

from ds_config import DSConfig


class DSHelper:
    def __init__(self):
        pass

    @classmethod
    def print_pretty_json(cls, obj):
        pprint(obj)


