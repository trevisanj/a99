import sys
if sys.version_info[0] < 3:
    print("Python version detected:\n*****\n{0!s}\n*****\nCannot run, must be using Python 3".format(sys.version))
    sys.exit()

from setuptools import setup, find_packages
from glob import glob


def find_scripts(pkgs):
    ret = []
    for pkgname in pkgs:
        ret.extend(glob(pkgname + '/scripts/*.py'))
    return ret


pkgs = find_packages()
scripts = find_scripts(pkgs)


setup(
    name='a99',
    packages=find_packages(),
    include_package_data=True,
    version='0.17.4.25',
    license='GNU GPLv3',
    platforms='any',
    description='A multi-purpose API in Python',
    author='Julio Trevisan',
    author_email='juliotrevisan@gmail.com',
    url='https://github.com/trevisanj/f311', # use the URL to the github repo
    keywords= ['astronomy', "fits", "spectroscopy", "spectral synthesis", "photometry",
               "honl-london", "nist", "hitran", "multiplicity"],
    install_requires=[],
    scripts=scripts
)


# TODO later install_requires=['numpy', 'matplotlib', 'pyqt5'],  # matplotlib never gets installed correctly by pip, but anyway...
