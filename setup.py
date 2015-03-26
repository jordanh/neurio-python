import sys
sys.path.append('.')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
  name = 'neurio',
  packages = ['neurio'],
  version = "0.2.7",
  description = 'Neurio energy sensor and appliance automation API library',
  author = 'Jordan Husney',
  author_email = 'jordan.husney@gmail.com',
  url = 'https://github.com/jordanh/neurio-python',
  download_url = 'https://github.com/jordanh/neurio-python/tarball/0.2.7',
  keywords = ['neurio', 'iot', 'energy', 'sensor', 'smarthome', 'automation'],
  classifiers = [],
  install_requires = ['requests'],
)
