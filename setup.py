from setuptools import setup

setup(name='reddit-refresh',
      version='1.0',
      description='Checks subreddit for a search term and sends new results via Pushbullet',
      url='http://github.com/Zedjones/Reddit-Refresh',
      author='Zedjones',
      author_email='dojoman19@gmail.com',
      license='GPL',
      packages=[],
      install_requires=[
          'bs4',
      ],
      zip_safe=False)
