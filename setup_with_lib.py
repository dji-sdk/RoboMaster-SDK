
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
import sys
import platform
import os
import re
import subprocess
import shutil

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

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


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        # required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        build_temp = self.build_temp + '_' + ext.name
        if not os.path.exists(build_temp):
            os.makedirs(build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=build_temp)

data_files = []
if platform.system() == "Windows":
    data_files = [('lib/site-packages', ["lib/libmedia_codec/src/ffmpeg-dll/avcodec-58.dll"]),
                  ('lib/site-packages', ["lib/libmedia_codec/src/ffmpeg-dll/avutil-56.dll"]),
                  ('lib/site-packages', ["lib/libmedia_codec/src/ffmpeg-dll/swresample-3.dll"]),
                  ('lib/site-packages', ["lib/libmedia_codec/src/ffmpeg-dll/swscale-5.dll"]),
                  ('lib/site-packages', ["lib/libmedia_codec/src/opus-dll/opus.dll"])]


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
    ],
    ext_modules=[CMakeExtension('libmedia_codec', './lib/libmedia_codec/')],
    cmdclass=dict(build_ext=CMakeBuild),
    data_files=data_files
)
