import os
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Get version number
about = {}
with open(os.path.join(here, "top_db", "__VERSION__.py")) as f:
    exec(f.read(), about)
    
# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='top_db',
      version=about["__version__"],
      description='MySQL.connector boilerplate',
      long_description=long_description,
      url='https://github.com/5uper5hoot/top-db',
      author='Peter Schutt',
      author_email='peter_schutt@bigpond.com',
      license='MIT',
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Software Development :: User Interfaces',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
      ],
      keywords='mysql-connector boilerplate retry logic',
      packages=find_packages(exclude=['tests']),
      install_requires=[
          "backoff>=1.4.3",
          "mysql-connector-python-rf>=2.2.2"
      ],
      extras_require={
          'dev': ['pytest'],
      })
