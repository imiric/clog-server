from setuptools import setup, find_packages

import versioneer

setup(
    name='clog-server',
    version=versioneer.get_version(),
    cmd_class=versioneer.get_cmdclass(),
    url='https://github.com/imiric/clog-server',
    description='centralized logging server',
    author='Ivan Mirić',
    author_email='imiric@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Logging',
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'flask==0.10.1',
        'flask-marshmallow==0.6.2',
        'flask-script==2.0.5',
    ]
)
