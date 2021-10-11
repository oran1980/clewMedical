from setuptools import setup, find_packages


install_requires = ['aio_pika', 'asyncio']

setup(
    name='publisher',
    author='',
    author_email='',
    version='1.0.1',
    description='Mapping raw data into medication events',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'scripts']),
    entry_points={
          'console_scripts': [
              'publisher = publisher.main:main'
          ],
      },
    install_requires=install_requires,
    test_suite="tests",
    zip_safe=False)
