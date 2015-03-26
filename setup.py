#!/usr/bin/env python
import os.path
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
            return f.read()
    except (IOError, OSError):
        return ''


def get_version():
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.append(src_path)
    from tree_output import version as tree_output_version
    return tree_output_version


setup(
    name='tree_output',
    version=get_version(),
    description='Python library to simplify building of tree output with '
                'command-line interfaces.',
    long_description=readme(),
    author='Yauhen Yakimovich',
    author_email='eugeny.yakimovitch@gmail.com',
    url='https://github.com/ewiger/tree_output/',
    license='MIT',
    packages=[
        'tree_output',
    ],
    #package_dir={'', 'tree_output'},
    download_url='https://github.com/ewiger/tree_output/tarball/master',
    install_requires=[
        'colorama>=0.2.7',
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 5 - Production/Stable',
    ],
    tests_require=['nose>=1.0'],
    test_suite='nose.collector',
)
