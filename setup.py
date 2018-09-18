from setuptools import setup

setup(name='xkbparse',
      version='0.1',
      description='xkb configuration parser',
      url='https://github.com/svenlr/xkbparse',
      author='Sven Langner',
      author_email='sven.langner@tu-bs.de',
      license='MIT',
      packages=['xkbparse'],
      zip_safe=False, install_requires=['pypeg2'])
