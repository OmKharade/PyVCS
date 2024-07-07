from setuptools import setup, find_packages

setup(
    name="pyvcs",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyvcs=cli:main',
        ],
    },
    author="Om Kharade",
    author_email="oskr6128@gmail.com",
    description="A simple version control system implemented in Python",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OmKharade/PyVCS",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
