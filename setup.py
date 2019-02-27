from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

install_requires = [
    'requests',
    'requests-aws-sign',
    'boto3',
]

with open('README.md') as f:
    readme = f.read()

setup(
    name='requests-sigv4',
    version='0.0.1',
    packages=['requests_sigv4'],
    url='https://github.com/cleardataeng/requests-sigv4',
    license='Apache 2.0',
    author='ClearDATA Engineering',
    author_email='support@cleardata.com',
    description='Library for making sigv4 requests '
        'to AWS API endpoints',
    long_description=readme,
    install_requires=install_requires,
    keywords='aws requests sign sigv4',
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest'
    ],
    classifiers=[],

)
