from __future__ import print_function

from lxml import html
import os
import sys
import datetime as dt
import json
import requests
from time import sleep
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def get_arg(index, default=None):
    """
    Grabs a value from the command line or returns the default one.
    """
    try:
        return sys.argv[index]
    except IndexError:
        return default


def search():
    keyword = get_arg(1)


if __name__ == "__main__":
    search()