
"""
RoboMaster SDK is based on the Python language and is suitable for the Python SDK software library
 of the RoboMater series.
Currently applicable to RoboMaster EP and Tello Edu and other products, it provides a rich API interface,
including: motion control, flight control, intelligent identification, lighting effect settings, data push,
video streaming and audio streaming APIs. And the design follows the principle of being as simple as possible,
and can be quickly used to facilitate learning and teaching. Based on each API interface,
there are code examples, you can refer to our developer documentation robomaster-dev.readthedocs.io.
"""

from setuptools import setup, find_packages
import os.path
import sys
if sys.version_info < (3, 6, 5):
    sys.exit("RoboMaster SDK requires Python 3.6.5 or later")

curr = os.path.abspath(os.path.dirname(__file__))


def fetch_version():
    with open(os.path.join(curr, 'src', 'robomaster', 'version.py')) as f:
        ns = {}
        exec(f.read(), ns)
        return ns


version_data = fetch_version()
version = version_data['__version__']


setup(
    name='robomaster',
    version=version,
    description="RoboMaster Python SDK",
    long_description=__doc__,
    long_description_content_type="text/markdown",
    author='EDU SDK TEAM',
    license='Apache License, Version 2.0',
    zip_safe=True,
    keywords='dji robomaster sdk robot drone'.split(),
    url="http://www.robomaster.com",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    package_data={
      'robomaster': ['LICENSE.txt', 'README.md']
    },
    install_requires=[
        'numpy >= 1.18',
        'opencv-python >= 4.2',
        'netaddr >= 0.8',
        'netifaces >= 0.10',
        'myqr >= 2.3'
    ]
)
