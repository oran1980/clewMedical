from setuptools import setup, find_packages


install_requires = ['aio_pika']

setup(
    name='consumer',
    author='',
    author_email='',
    version='1.0.1',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'scripts']),
    entry_points={
          'console_scripts': [
              'consumer = consumer.main:main'
          ],
      },
    install_requires=install_requires,
    test_suite="tests",
    zip_safe=False)
