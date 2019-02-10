from setuptools import setup, find_packages

setup(
    name='docStyler',
    version='0.1.0',
    packages=['docstyler'],
    url='https://github.com/hfagerlund/mkdocs-docstyler-plugin',
    license='BSD-3',
    author='Heini Fagerlund',
    description='docstyler is a MkDocs plugin for adding persistent, preferred and alternate external stylesheet links to custom themes.',
    python_requires='>=3.6.4',
    install_requires=[
        'mkdocs>=1.0.4'
    ],
    entry_points={
        'mkdocs.plugins': [
            'docstyler = docstyler.plugin:docStyler',
        ]
    },
    package_data={'docstyler': ['templates/*.html']},
    include_package_data = True,
    long_description=open('README.md').read(),
)
