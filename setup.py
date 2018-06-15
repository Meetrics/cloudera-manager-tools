from setuptools import setup

setup(
    name = 'cloudera-manager-tools',
    version = '1.0.0',dependenc
    packages = ['cloudera-manager-tools'],
    install_requires = [ 'cm-api' ],
    entry_points = {
        'console_scripts': [
            'cmt = cloudera-manager-tools.__main__:main'
        ]
    }
)
