# -*- coding: utf-8 -*-
"""mlops setup script

:copyright: Copyright (c) 2024 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
import pykern.pksetup

pykern.pksetup.setup(
    name="mlops",
    author="RadiaSoft LLC",
    author_email="pip@radiasoft.net",
    description="Tools for managing our ML operations",
    install_requires=[
        "pykern",
    ],
    license="http://www.apache.org/licenses/LICENSE-2.0.html",
    url="https://github.com/radiasoft/mlops",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
