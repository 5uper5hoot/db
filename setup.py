import os
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "db", "__VERSION__.py")) as f:
    exec(f.read(), about)

setup(name='db',
      version=about["__version__"],
      description='MySQL.connector boilerplate',
      url='https://github.com/5uper5hoot/db.git',
      author='Peter Schutt',
      author_email='peter@topsport.com.au',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      zip_safe=False,
      install_requires=[
          "backoff>=1.4.3",
          "mysql-connector-python-rf>=2.2.2"
      ])
