# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    libms_license = f.read()

setup(
    name='libraryms',
    version='2.0',
    description='Tech interview work',
    long_description=readme,
    author='val0907010',
    author_email='val0907010@gmail.com',
    url='https://github.com/',
    license=libms_license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['Flask', 'Flask-Login', 'Flask-OpenID', 'Flask-SQLAlchemy', 'Flask-WTF',
                      'SQLAlchemy', 'Flask-Migrate', 'Werkzeug', 'WTForms']
)
