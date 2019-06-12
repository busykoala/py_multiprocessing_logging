import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

NAME = 'multiprocessing_logging'
VERSION = '0.0.1'
AUTHOR = 'Busykoala'
EMAIL = 'info@busykoala.ch'
DESCRIPTION = 'Test logging while multiprocessing'
URL = 'https://github.com/busykoala/multiprocessing_logging'
REQUIRED = [
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved ::GPLv3 License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIRED,
    entry_points={
        'console_scripts': ['log_stuff=multiprocessing_logging.console:main'],
    },
)
