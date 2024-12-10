import os

path = os.getcwd().replace("\\", "/")
os.system(f'{path[0]}: & cd "{path}" & python setup.py sdist & pip install dist/mylibrary-0.0.tar.gz')
