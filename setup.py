from os import path
from setuptools import setup, find_packages

setup(
    name="GMSC-mapper",  
    version="0.0.1_alpha", 
    description="Command line tool to query the Global Microbial smORFs Catalog (GMSC)",  
    long_description=open("./README.md", "r").read(),  
    long_description_content_type="text/markdown",  
    url="https://github.com/BigDataBiology/GMSC-mapper",  
    author="Yiqian Duan",
    author_email="yqduan20@fudan.edu.cn",  
    license="MIT"
    classifiers=[  
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    package_dir={"GMSC-mapper": "GMSC-mapper"}, 
    packages=['GMSC-mapper'],  
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=open('./requirements.txt', 'r').read().splitlines(),
    zip_safe=False,
    entry_points={  
        "console_scripts": ['GMSC-mapper=GMSC-mapper.main:main'],
    }
)
