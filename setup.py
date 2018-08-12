import re
from os import path
from codecs import open  # To use a consistent encoding
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


# Get version without importing, which avoids dependency issues
def get_version():
    with open('pyswitcheo/__init__.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


install_requires = ['requests==2.19.1', 'neocore', 'jsonschema==2.6.0']


test_requires = ['pytest', 'pytest-sugar', 'pytest-asyncio', 'pytest-cov', 'jsonschema']

extra_requires = {
    'docs': [
        'sphinx >= 1.4',
        'sphinx_rtd_theme',
        'Flask-Sphinx-Themes']}

setup(
    name='pyswitcheo',
    description="Python library to interact with switcheo APIs",
    long_description=long_description,
    version=get_version(),
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=test_requires,
    extra_requires=extra_requires,
    packages=find_packages(),
    zip_safe=False,
    author="Ankur Srivastava",
    author_email="best.ankur@gmail.com",
    download_url="https://github.com/ansrivas/pyswitcheo/archive/{}.tar.gz".format(get_version()),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"]
)
