import os
import re
from setuptools import setup, find_packages

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

with open('README.md') as readme_file:
    readme = readme_file.read()

install_requires = [
    'requests',
    'requests-aws-sign',
    'boto3',
]


def get_version():
    init = open(os.path.join(ROOT, 'requests_sigv4', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='requests-sigv4',
    version=get_version(),
    packages=find_packages(exclude=['tests*']),
    url='https://github.com/cleardataeng/requests-sigv4',
    license='Apache License 2.0',
    author='ClearDATA Engineering',
    author_email='support@cleardata.com',
    description='Library for making sigv4 requests '
        'to AWS API endpoints',
    long_description=open('README.md').read(),
    install_requires=install_requires,
    keywords='aws requests sign sigv4',
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
