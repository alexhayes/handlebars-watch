from setuptools import setup, find_packages
import sys, os

version = '0.1'
SRC_DIR = 'src'

setup(name='handlebars-watch',
      version=version,
      description="A watching auto-compiler for handlebars.js",
      long_description="""\
Watches a specified location and on detecting a file change, precompiles the file using the handlebars binary.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='handlebars javascript template moustache js',
      author='Alex Hayes',
      author_email='alex@alution.com',
      url='https://github.com/alexhayes/handlebars-watch',
      license='Dual licensed under the MIT or GPL Version 2 licenses.',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
          'console_scripts': [
            'handlebars-watch = handlebars.watch:main',
            ],
      }
    )
