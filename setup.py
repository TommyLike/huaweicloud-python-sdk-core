#!/usr/bin/env python

"""
distutils/setuptools install script.
"""
import io
from os import path
from setuptools import setup, find_packages

import huaweipythonsdkcore

root_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(root_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='huaweicloud-python-sdk-core',
    version=huaweipythonsdkcore.__version__,
    description='HuaweiCloud Python SDK Core',
    long_description=long_description,
    author='Huawei Cloud',
    url='https://github.com/huaweicloud/huaweicloud-python-sdk-core',
    maintainer_email="support@huaweicloud.com",
    scripts=[],
    packages=find_packages(),
    install_requires=['urllib3 >= 1.23',
                      'six >= 1.10.0',
                      'retrying >= 0.9.0'],
    license="Apache License 2.0",
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
