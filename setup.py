from setuptools import setup, find_packages

# Load version from version.txt
with open("version.txt") as version_file:
    version = version_file.read().strip()

setup(
    name="KFCAP",
    version=version,
    author="Jacob Widaeus",
    author_email="jacob.widaeus@ki.se",
    description="A tool to import and view REDcap data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/widaeus/KFCAP",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "altgraph==0.17.4",
        "certifi==2024.8.30",
        "charset-normalizer==3.4.0",
        "colorama==0.4.6",
        "customtkinter==5.2.2",
        "darkdetect==0.8.0",
        "idna==3.10",
        "iniconfig==2.0.0",
        "numpy==2.1.2",
        "packaging==24.1",
        "pandas==2.2.3",
        "pefile==2023.2.7",
        "pluggy==1.5.0",
        "pyinstaller==6.11.0",
        "pyinstaller-hooks-contrib==2024.9",
        "pytest==8.3.3",
        "python-dateutil==2.9.0.post0",
        "pytz==2024.2",
        "pywin32-ctypes==0.2.3",
        "requests==2.32.3",
        "semantic-version==2.10.0",
        "setuptools==75.2.0",
        "six==1.16.0",
        "tzdata==2024.2",
        "urllib3==2.2.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
    python_requires=">=3.6",
)