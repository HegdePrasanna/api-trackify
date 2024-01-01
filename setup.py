from setuptools import setup, find_packages

setup(
    name='fastapilogger',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'motor',
    ],
    # Additional metadata
    author='Prasanna Hegde',
    description='FastAPI logger package',
    url='',
)