__author__ = 'rotem'

from setuptools import setup, find_packages

setup(name='Probe',
      entry_points={
          'console_scripts': ['probe=console:main'],
      },
      packages=find_packages(),
      version='0.1',
      author='rotem@everything.me',
      description='Probe - Android Benchmark',
      install_requires=['click', 'mysql-python', 'dataset']
)
