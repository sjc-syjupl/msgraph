import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='msgraph',
      version='0.2',
      description='API wrapper for Microsoft Graph written in Python',
      long_description=read('README.md'),
      url='https://github.com/sjc-syjupl/msgraph',
      long_description_content_type="text/markdown",
      author='Sylwester Jurczyk, Miguel Ferrer, Nerio Rincon, Yordy Gelvez',
      author_email='syjupl@gmail.com',
      license='MIT',
      packages=['msgraph'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
