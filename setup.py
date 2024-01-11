from setuptools import setup

exec(compile(open('gmsc_mapper/gmsc_mapper_version.py').read(),
             'gmsc_mapper/gmsc_mapper_version.py', 'exec'))

long_description = open('README.md', encoding='utf-8').read()

setup(
    name="GMSC-mapper",
    version=__version__,
    description="Command line tool to query the Global Microbial smORFs Catalog (GMSC)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BigDataBiology/GMSC-mapper",
    author="Yiqian Duan",
    author_email="yqduan20@fudan.edu.cn",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    packages=['gmsc_mapper'],
    install_requires=open('./requirements.txt', 'r').read().splitlines(),
    zip_safe=False,
    entry_points={
        "console_scripts": ['gmsc-mapper=gmsc_mapper.main:main'],
    }
)
