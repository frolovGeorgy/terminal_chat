from setuptools import setup, find_packages

setup(
    include_package_data=True,
    name='chat',
    version='0.1',
    description='terminal chat',
    author='Frolov Georgy',
    packages=find_packages(),
    install_requires=[
        'bidict == 0.21.4'
    ]
)
