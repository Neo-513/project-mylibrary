from setuptools import find_packages, setup
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
setup(name="mylibrary", version="0.0", packages=find_packages())
