from distutils.core import setup
# to install, use: python3 setup.py sdist, python3 setup.py build, sudo python3 setup.py install
setup (
    name = 'utilities',
    version = '1.0.1',
    py_modules = ['simple_cryptography', 'list_helper', 'user_input'],
    author = 'miroamr78',
    url = 'https://github.com/miroamr78/PythonUtilities',
    download_url = 'https://github.com/miroamr78/PythonUtilities/archive/master.zip',
    author_email = 'miroamr78@gmail.com',
    description = 'A collection of utilities for repeated tasks',
    keywords = ['user', 'input', 'utilities', 'helper'],
    classifiers = []
)
