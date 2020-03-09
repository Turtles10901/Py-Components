"""
Flask-Components
-------------

Flask-Components is a Flask extension to create reuseable 'Components' that render them selves as HTML.
"""
from setuptools import setup


setup(
    name='Flask-Components',
    version='1.0',
    url='http://example.com/flask-components/',
    license='BSD',
    author='Allan Jacobs',
    description='A Flask extension to create modular components that render as HTML.',
    long_description=__doc__,
    packages=['flask_components'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'importlib'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)