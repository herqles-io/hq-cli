from setuptools import setup, find_packages

setup(
    name='hq-cli',
    version='1.0',
    url='',
    include_package_data=True,
    license='',
    author='Ryan Belgrave',
    author_email='rbelgrave@covermymeds.com',
    description='Herqles CLI',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'requests==2.7.0',
        'requests[security]',
        'schematics==1.0.4',
        'pyyaml==3.11',
    ],
    dependency_links=[],
    scripts=['bin/herq']
)
