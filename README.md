# cloudera-manager-tools
Cloudera Manager CLI tools to easily perform common operations using its API interface.

# Setup
## Requirements
+ Python 2.7
+ pip
+ *make* (optional)
+ *virtualenv* (development)

## Installation
1. Clone the project
1. Run ``sudo python setup.py install`` or just ``make install``

## Usage
1. Run ``cmt --help`` to get complete usage info.

## Uninstallation
1. ``sudo pip uninstall cloudera_manager_tools && sudo rm -f $(which cmt)`` or just ``make uninstall``

# Development
## Configure environment
1. Clone the project
1. Configure the dev env with ``make devinit``
1. Activate the virtualenv ``source .env/bin/activate``
1. Install CMT in editable mode in the virtualenv ``make devinstall``

## Developing new CMT services
If you want to implement a new **SERVICE** named _**myservice**_ for CMT, you need to:
1. Create a new ``myservice.py`` file in the [``cloudera-manager-tools``](cloudera_manager_tools)  folder
1. Implement in it a ``Myservice`` class (**Uppercase capital letter**) which extends one of the CMT abstract classes defined in [``__interfaces__.py``](cloudera_manager_tools/__interfaces__.py)
1. Implement actions for your **myservice** by implementing *public* methods (whose name is not staring by "\_").

Have a look at the code in any of the already implemented services in the [``cloudera-manager-tools``](cloudera_manager_tools) for more details.

**IMPORTANT NOTES**:  
1. Any ``.py`` file in the [``cloudera-manager-tools``](cloudera_manager_tools), whose name is not starting with "\__" (two underscores) will be loaded as **SERVICE**
1. Any method defined in your CMT service class whose name is not starting with "\_" (an underscore) will be exposed as **ACTION** for your service.
