import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


long_description = (
    read('README.rst')
    + '\n' +
    read('CHANGES.rst')
)


tests_require = [
    'grokcore.content',
    'grokcore.view[security_publication]',
    'grokcore.view[test]',
    'zope.app.appsetup',
    'zope.app.wsgi[test]',
    'zope.errorview >= 1.2',
    'zope.testbrowser',
    'zope.testing',
]


setup(
    name='grokcore.rest',
    version='4.1',
    author='Grok Team',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/grokcore.rest',
    download_url='https://pypi.org/project/grokcore.rest/',
    description='REST View component for Grok.',
    long_description=long_description,
    license='ZPL 2.1',
    classifiers=[
        'Development Status :: 7 - Inactive',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Zope :: 3',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>= 3.7',
    install_requires=[
        'grokcore.component >= 2.5dev',
        'grokcore.security',
        'grokcore.traverser >= 3.0.0',
        'grokcore.view',
        'martian',
        'setuptools',
        'zope.component',
        'zope.interface',
        'zope.publisher >= 4.2.2',
    ],
    extras_require={'test': tests_require},
)
