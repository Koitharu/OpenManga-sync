from setuptools import setup, find_packages

setup(
    name='openmanga-sync',
    version='0.1',
    packages=find_packages(),
    install_requires=['Flask', 'Flask-RESTful', 'Flask-SQLAlchemy']
)