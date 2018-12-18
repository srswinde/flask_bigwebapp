#!/usr/bin/env python3

from distutils.core import setup
#import shutil
import subprocess


setup(
    name="flask_bigwebapp",
    version="0.1",
    packages=["flask_bigwebapp"],
    package_data = {'':["templates/*"]}
        )


#shutil.call()
subprocess.run( ["/usr/sbin/apachectl", "restart"] )
