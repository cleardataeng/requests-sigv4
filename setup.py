from setuptools import setup

install_requires = [
    'requests',
    'requests-aws-sign',
    'boto3',
]

with open('README.md') as f:
    readme = f.read()

setup(
    name='requests_sigv4',
    version='0.0.1',
    packages=['requests_sigv4'],
    url='https://github.com/cleardataeng/requests-sigv4',
    license='Apache 2.0',
    author='ClearDATA Engineering',
    author_email='support@cleardata.com',
    description='Library for making sigv4 requests '
        'to AWS API endpoints',
    install_requires=install_requires,
    keywords='aws requests sign sigv4',
    classifiers=[],
)
