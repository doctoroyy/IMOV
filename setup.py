from setuptools import setup, find_packages


setup(
  name='imov',
  version='0.1.4',
  packages=find_packages(),
  entry_points={
    'console_scripts': [
      'imov=imov:run',
    ]
  },
  install_requires=[
    "requests",
    "openpyxl",
    "lxml",
    "setuptools",
  ],
  url='https://github.com/doctoroyy/IMDB-TOP-250',
  author='doctoroyy',
  author_email='doctor.oyy@gmail.com',
  description='A Python Crawler for IMDB-TOP-250.'
)
