#!/usr/bin/env python3
import sys
import os

from bs4 import BeautifulSoup


# Remove HTML tags
html_file = open("file.html", "r")
text = BeautifulSoup(html_file)

