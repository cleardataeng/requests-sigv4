from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

install_requires = [
    'requests',
    'requests-aws-sign',
    'boto3',
]

setup(
    name='requests-sigv4',
    version='0.1.6',
    packages=find_packages(exclude=['tests*']),
    url='https://github.com/cleardataeng/requests-sigv4',
    license='Apache License 2.0',
    author='ClearDATA Engineering',
    author_email='support@cleardata.com',
    description='Library for making sigv4 requests to AWS API endpoints',
    long_description='Library for making sigv4 requests to AWS API endpoints',
    install_requires=install_requires,
    keywords='aws requests sign sigv4',
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
        'Programming Language :: Python :: 3.8',
    ],
)
