# Overview 
The goal of this application is to provide full Python functionality to Splunk. Currently, the Python distribution built in to Splunk runs on a version 2.7.x depending on the Splunk version. Additionally, there are significant core modules that are excluded in this distribution. This suite of apps will allow developers to create Python virtual environments and pick the Python version and modules installed to the environment. This includes core distributions of the interpreter in multiple 2.7.x and 3.5+ versions, as well as the use of pip for the installation of additional modules within a virtual environment.

# Why PyDen
## Introduction
The PyDen app is based on the premise that the Splunk built-in CPython distribution is insufficient for advanced development within the Splunk platform. The key example of this is Splunk's own Machine Learning toolkit (MLTK). The Splunk MLTK requires the installation of an add-on which provides access to the Anaconda Python interpreter and several Python libraries that are common in the community for Machine Learning applications, such as `numpy`. 

While this is an excellent solution for providing the needed functionality for the MLTK, it's insufficient for generalized use for three reasons. These are the three primary concerns  that PyDen attempts to address: version flexibility, proper isolation, and access to PyPI packages.

## Version flexibility
Splunk's built-in Python utilizes version 2.7 of CPython. While there are a decent number of common libraries that are continuing support of 2.7, the number is dwindling and  newer projects do not support it at all. The version will also reach end of life in 2020, causing significant supportability and security issues. The PyDen app allows a developer to build CPython from source in a variety of versions including 3.5 and higher through the use of the `createdist` command.

## Development isolation
Modules added to a Splunk app are available to the entire installation, which is in contrast to Python development best practices which calls for the isolation of package requirements through the use of virtual environments. This isolation of packages resolves issues around dependency conflicts and keeps the scope of libraries to the context of the application. This is done through making Python virtual environments available via PyDen's `createvenv` command.

## Leveraging libraries
Splunk does not allow a developer to add additional packages not included with the built-in distribution except through inclusion within the app directly. Ease of inclusion of third-party libraries is a key benefit of Python. However, including non-native libraries within a Splunk application poses two key challenges: dependency chasing and library conflicts (which we discuss in the next section). In order to include a non-native library within a Splunk app, a developer must include it directly within the app's `bin` directory. If the package contains any dependencies, those must be added as well. If any of the dependencies have their own dependencies, they must be included as well. And so on, and so on. By creating access to the `pip` command within Splunk, PyDen does not suffer this problem.

# Architecture
PyDen is broken into two separate Splunk apps called: PyDen and PyDen Manager. The PyDen Manager app contains all the functionality needed for a user to download, compile, and build Python distributions and virtual environments, as well as the ability to use pip to install packages to those environments. The actual CPython builds and environments are placed in the PyDen app. The location of the PyDen app can vary depending on the Splunk architecture. 

For a single search head environment the PyDen app can be placed along side the PyDen Manager in the Splunk apps directory. 

In a deployment with multiple search heads, PyDen can be placed onto the deployment server repository location, `deployment-apps` by default. 

In a deployment utilizing search head clustering, it can be placed into the deployer's `shcluster/apps` directory. 

In all of these scenarios, PyDen Mnagaer must be installed to the same host as PyDen. The `pyden.conf` configuration file inside of the PyDen Manager app contains a stanza called `app` which has a `location` attribute which should specify the absolute path of the PyDen app. Additionally, the PyDen Manager host and the eventual deployment host(s) for PyDen (e.g. members of a search head cluster) should be running the same platform.

If there is a need to utilize the virtual environments for scripts that are dispatched to the indexer layer, PyDen will also need to be deployed to any indexer that may need it. There is currently no specific recommendation on how to accomplish this as there are separate management servers for search head and indexer clusters. 

# Compatibility
The PyDen suite of apps has been tested for compatibility with Splunk 7.2, 7.3, AND 8.0.

# Requirements
The app builds CPython from source and therefore the success of the build is highly dependent on the operating system libraries available. The host OS must have a compiler and the packages needed in order to build Python from source. Please refer to the documentation for your OS for needed packages. Two options are included in the ./configure command during the Python build process: `--enable-optimizations` (if configured) and `--with-ensurepip=install`.

Currently only Linux-based platforms are supported. In theory, this should work on OSX but this is as of yet untested. Further platform support will be developed if requested.

# Installation and Configuration
Installation of the PyDen Manager follows the same process as any other Splunk app. Please refer to Splunk's [documentation](https://docs.splunk.com/Documentation/Splunk/7.2.3/Admin/Deployappsandadd-ons) on the subject. The PyDen app installation process will vary depending on the Splunk deployment architecture. Please see the [Architecture](#Architecture) section for details on where to install PyDen. If PyDen is installed to any location other than the Splunk apps directory, the installation process will consist of extracting the app from the gzipped tarball and placing it in the specified directory on the host.

Both PyDen and PyDen Manager need to be installed on the same host. After both apps are installed, the PyDen Manager needs to be configured through the `pyden.conf` file. This file contains two stanzas: `download` and `app`. The `download` stanza has a single attribute called `url` which is used to specify the location from where Python is downloaded. It is not recommended to change this location except in the need to app proxy information. If a location other than [www.python.org](https://www.python.org) there will be significant gaps in the functionality of the dashboards. The `app` stanza contains two attributes `optimize` and `location`. The `location` attribute is the absolute path of the location of the PyDen app and the `optimize` attribute is a boolean which indicates whether or not Python will be built using the `--enable-optimizations` parameter. Enabling optimizations will provide significant speed improvements but takes significantly longer to build. 

# Custom Commands
There are three primary custom commands that make up the core functionality of PyDen: `createdist`, `createvenv`, and `pip`. There are additional suplemental commands that primarily aid in working with the dashboards.

## Createdist
The `createdist` command is how PyDen downloads and builds a CPython distribution. This command contains two keyword arguments `version` and `download`. The `version` argument is simply the version number of the Python installation to be built. The `download` argument is optional and only used if not doing an automatic download from [www.python.org](https://www.python.org). Instead of being downloaded, the Python source package can be placed inside the PyDen Manager's bin/build directory. When done this way, the `download` argument should provide the name of the package to be used. Package must be a file of `.tgz` format.

*Note: the first distribution created by this command will be set as the default version used by other commands like `createvenv`.*

Examples:

*Download and install version 3.7.2 from www.python.org*
```
| createdist version=3.7.2
```

*Install 3.7.2 version of Python from source package called mypython.tgz*
```
| createdist version=3.7.2 download=mypython.tgz
```

## Createvenv
The `createvenv` command creates a Python virtual environment with a specified version and name. The command has two required keyword arguments: version and name. The version is a version number that references an installed Python distribution from the `createdist` command. The name argument is a name to be associated with the environment for future reference.

*Note: the first environment created by this command will be set as the default environment used by other commands like `pip`.*

Examples:

*Create a virtual environment with Python version 3.7.2 and named mypy*
```
| createvenv version=3.7.2 name=mypy
```

## Pip
The `pip` command installs Python packages available from the Python Package Index. This command works identically to the command-line tool of the same name with one exception. The command takes a single keyword argument called environment which specifies which virtual environment the command applies to. If used, this must be the first argument listed. If not used, the command will apply to the default virtual environment.

Examples:

*Install the package `requests` to the default environment*
```
| pip install requests
```

*Upgrade the pip version of the environment `myvenv`*
```
| pip environment=myvenv install --upgrade pip
```

## Additional Commands
The following commands are included in the PyDen Manager app but are of limited value. They're typically used to provide some needed functionality for a dashboard. 

### Getversions
This command creates a list of events with a field called `version` whose values are PyDen compatible versions of Python available from [www.python.org](https://www.python.org).

Example:

```
| getversions
```

### Pydelete
This command deletes distributions and virtual environments created through the `createdist` and `createvenv` commands. The command takes a single positional argument of the name or version number of the environment or distribution to be deleted.

Examples:

*Delete the `3.7.2` distribution*
```
| pydelete 3.7.2
```

*Delete the virtual environment named `mypy`*
```
| pydelete mypy
```

### Getvenvs
This command creates a set of events with a single field called `environment` whose values are the names of virtual environments created by the `createvenv` command.

Example:

```
| getvenvs
```

### Getpackages
The `getpackages` command is used to get package information from the Python Package Index. There are two modes to this command. The command itself takes a single positional argument. If `pypi_simple_index` is provided as the argument then the command will create a set of events with a single field called `package` whose value is the name of a package from PyPI's [simple index](https://PyPI.org/simple/).

If any other argument is provided, the command will use its other mode which looks up the json data for a PyPI package found at `https://pypi.python.org/pypi/package_name/json` and returns an event with a single field called `description` whose value is the PyPI description of the package provided.

Examples:

*Get all PyPI packages from the PyPI simple index*
```
| getpackages pypi_simple_index
```

*Get the description for the requests package*
```
| getpackages requests
```

# Using virtual environments
Leveraging the environments in the PyDen app is simply a matter of importing the activation modules provided with PyDen.

PyDen comes with two scripts in its bin directory: `activate.py` and  `activate_default.py`. The `activate.py` script contains a function called `activate_venv_or_die`. In order to run a script with a PyDen virtual environment, the script must include the following code at the top, substituting your virtual environment name for `environment_name`:
```python
from activate import activate_venv_or_die
activate_venv_or_die("environment_name")
```

This will utilize Python's `os.execve` function to restart the script with the provided virtual environment. 

While this will work with any valid virtual environment provided, you may not wish to muddy up your import statements with functions. In order to avoid this problem the `activate_default.py` script is provided. This script will activate the default virtual environment defined in the PyDen app's `pyden.conf` configuration file when imported and without the function call. Instead of the above code, simply add the following code to the top of your script:
```python
import activate_default
```

It is important to note that these two scripts are included in the PyDen app and in order to import them as Python modules, you will need to do one of the following:
- Place the script you are writing in the PyDen bin directory (this is highly discouraged as scripts can be overwritten during an upgrade of the app)
- Modify the `sys.path` to include the PyDen bin directory before importing the scripts (this may have unintended side effects)
- Copy `activate.py` and `activate_default.py` files into the app which contains your script (preferred method)
