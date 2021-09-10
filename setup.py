import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-sermepa',
    version='1.1.5',
    packages=[
        'sermepa',
        'sermepa.migrations',
    ],
    include_package_data=True,
    license='MIT License',
    description='A django app to emit and listen Redsys/sermepa POS payments',
    long_description=README,
    install_requires=["pyDes==2.0.1", ],
    url='https://github.com/Etxea/django-sermepa',
    author='Jon Latorre',
    author_email='info@etxea.net',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
