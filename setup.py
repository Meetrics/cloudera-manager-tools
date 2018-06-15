from setuptools import setup, find_packages

setup(
    name = 'cloudera_manager_tools',
    version = '1.0.0',
    description = 'Cloudera Manager CLI utility to easily perform common operations using its API interface.',
    url = 'https://github.com/Meetrics/cloudera-manager-tools',
    packages = find_packages(),
    install_requires = [ 'cm-api' ],
    entry_points = {
        'console_scripts': [
            'cmt = cloudera_manager_tools.__main__:main'
        ]
    }
)
