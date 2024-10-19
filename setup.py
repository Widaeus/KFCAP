from setuptools import setup, find_packages

setup(
    name='KFCAPIMPORT',  # Name of your package
    version='0.1',
    packages=find_packages(where='src'),  # Finds all packages in 'src' folder
    package_dir={'': 'src'},  # Tells setuptools to look in 'src' for packages
    include_package_data=True,
    install_requires=[
        "customtkinter",
        "pandas",
        "pytest",
        "PyCap",
        "requests",
        "semantic-version",
        "typing-extensions"
    ],
    entry_points={
        'console_scripts': [
            'kfcapimport=main:main',  # Assuming 'main' function in main.py starts your GUI
        ],
    },
)