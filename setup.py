from setuptools import setup

setup(name='db',
      version='0.1.2',
      description='MySQL.connector connection manager and statement executor',
      url='https://github.com/5uper5hoot/db.git',
      author='Peter Schutt',
      author_email='peter@topsport.com.au',
      license=None,
      packages=['db'],
      zip_safe=False,
      install_requires=[
          "backoff>=1.4.3",
          "mysql-connector-python-rf>=2.2.2"
      ])
