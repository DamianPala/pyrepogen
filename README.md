# Pyrepogen
Pyrepogen is a python repository generator for fast and simple preparing the python project repository in standardized way. Pyrepogen provides many options to customize the repository generation.

One of the most important feature of Pyrepogen is to generate **Repoassist** in the generated repository. Repoassist provides some extra features which are useful during your code development and maintaining.

## Requirements

- Python >= 3.7
- Git >= 2.20.0
- GNU Make

> Required software must be available from command line - added into the system PATH.

## Installation

#### **[TEMPORARY UNAVAILABLE]** Install from PyPi

To install Pyrepogen you can use pypi: 

```
pip install pyrepogen
```

#### Install from sources

To install from sources do:

1. Clone or download Pyrepogen repository

2. Enter to `pyrepogen` directory

3. Type `pip install -r requirements.txt`

4. Type `python setup.py install`

   >  Portable usage from sources without installation is also available.

## Example

The fastest way to show how Pyrepogen works is to use demo. Just type:

```
pyrepogen --demo
```

Then a repository will be generated in the `demo_project` directory at your current working directory.

## Usage

There are two ways to generate a repository: **wizard** and a **configuration file**.

### Wizard

To run wizard, type `pyrepogen` in your command line terminal and follow the wizard.

In the case of using from sources, just type `make run` in the root of pyrepogen and follow the wizard.

### Config file

In the case when you want to generate many repositories, using a predefined configuration file is the best solution.  

Configuration file could be created in many ways:

1. Using following config file template and saved as `gen_repo.cfg` file
2. Automatically generated in current working directory when you run Pyrepogen with only a `repo_path` parameter.
3. By copying from sources the `gen_repo.cfg` file.

#### Config file template

```
# Required parameters:
repo-name = 
# project-type values: package or module
project-type = 
project-name = 
author = 
author-email = 
short-description = 
# changelog-type, authors-type values: generated or prepared
changelog-type = 
authors-type = 

# Optional parameters:
maintainer = 
maintainer-email = 
home-page = 
# is-cloud, is-sample-layout, is-git values: true or false
is-cloud = 
is-sample-layout = 
is-git = 
git-origin = 
```

The next step is to run Pyrepogen with path where a repository will be generated:

```
pyrepogen <path where you want to generate a repo>
```

> Always specify paths with double quotes when you type space - " " in it!
>
> In this specified path the directory named with repo-name parameter will be created. 

When your config file is not in your current working directory or it has a different name, you can specify it using `-c` option:

```
pyrepogen <path where you want to generate a repo> -c <path to config file>
```

#### Config file parameters

Following table describes some of the most interesting and exotic configuration file parameters.

| Parameter        | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| changelog&#x2011;type   | generated - the changelog file will be automatically generated and updated every release; prepared - the changelog file should be prepared by you manually. |
| authors&#x2011;type     | The same behavior as in the changelog file.                  |
| is&#x2011;cloud         | true - additional futures regarding a cloud handling will be generated; false - do not use this feature |
| is&#x2011;sample&#x2011;layout | true - generate sample files; false - do not use this feature |
| is&#x2011;git           | true - init Git repository; false - do not use this feature  |
| git&#x2011;origin       | Specify an origin of your Git repository. Leave empty if you do not want to specify the remote origin. |

### Types of repositories

There are two types of repositories that Pyrepogen can generate: package and module

#### Package repository

This type of repository is a Python Package. Source files are stored in repository tree in the directory named from `project-name` parameter.

#### Module repository

Module repository is intended to developing a Standalone Python Module. In this case a source file is stored directly in the repository tree and named with name from `project-name` parameter.

### Repository generation flow

1. Create repository directory.
   - If `git-origin` parameter was set then a repository directory will has the same name as the remote repository.
2. If `is-git` parameter was set then an empty repository will be initialized.
3. If `git-origin` parameter was set then a repository from the origin will be cloned.
4. Generate repository directories.
5. Generate repository files.
6. Generate Repoassist.
7. If `is-git` parameter was set then generated and not ignored files will be added into the repository tree.

### Available Options

| Option        | Description                                                  |
| ------------- | ------------------------------------------------------------ |
| repo_path   | Path to the directory where the repository will be generated. If directory does not exist then will be created. In this path the directory named with repo-name parameter will be created. Always enter with double quotes. |
| &#x2011;c/&#x2011;&#x2011;config | Path to the repository config file. |
| &#x2011;u/&#x2011;&#x2011;update | Path to the repository where Repoassist will be updated. |
| &#x2011;q/&#x2011;&#x2011;quiet | Disable output. |
| &#x2011;d/&#x2011;&#x2011;debug   | Enable debug output. |
| &#x2011;f/&#x2011;&#x2011;force | Override existing files. |
| &#x2011;v/&#x2011;&#x2011;version | Show version. |
| --demo | Generate a demo repository in your current working directory. |

## Repository structure

Generated repository tree is prepared with a structure as following.

```
my_repository
|-- docs
|-- my_project
|   (only in package repo type - directory for source code)
|
|-- repoassist
|   (generated repoassist files by pyrepogen)
|-- tests
|
|-- my_project.py
|   (only in module repo type - source code file)
|-- .gitignore
|-- cloud_credentials.txt
|   (only when cloud feature was choosen)
|-- conftest.py
|-- LICENSE
|   (by default MIT License is generated)
|-- Makefile
|-- README.md
|-- requirements.txt
|-- requirements-dev.txt
|-- setup.cfg
|-- setup.py
|-- TODO.md
|-- tox.ini
    (tox configuration file)
```



# Repoassist

Repoassist is a package generated by Pyrepogen to provide many features useful during your code development and maintaining. This package is stored in `repoassist` directory and used through GNU Make.

## Usage

Usage of this **Repoassist** is based on make targets from the command line. As a terminal, **Linux like terminal with the shell** is recommended, e.g. Git Bash or native Cygwin Console. Windows Command Line terminal **is not supported**.

By typing the `make help` you will list all available targets with simple description.

### Available Targets

#### Make requirements

- Lists necessary environment requirements.
- Installing [Meld](http://meldmerge.org/) is strongly recommended to convenient source files interactive formatting.

#### Make prepare

- Installs development requirements from `requirements-dev.txt` file.
- Installs requirements from `requirements.txt` file.

#### Make update

- Updates Repoassist in your repository to version from installed Pyrepogen.
- If git repository is initialized then new files will be automatically added into the repository tree after receiving a confirmation from wizard.
- To run this target installed Pyrepogen is required.
- Before update Repoassist, update Pyrepogen is recommended to the latest version.

#### Make release

- Generates a **source distribution package** and **wheel** based on source files added to repository tree.
- Packages are generated using [Python Build Reasonables (pbr)](https://docs.openstack.org/pbr/latest/).
- Wizard to simplifying and standardizing the generation process.
- There are two ways to generate packages: release and regenerate.
- Output packages are stored in `dist` directory.

##### Release

- Full package generation process.
- Release tag and release message are delivered by user.

##### Regenerate

- Regenerate current sources to package without tagging.
- If the last commit is equal to last tag commit, then generated package will be a final release package with proper release tag.
- If there are commits after last release tag, then generated package will be a development release package with last release tag with `devN` suffix.
- Changelog and AUTHORS files are not generated in this release type.

##### Extra features

- System Text Editor is used to prepare release message rather than a command line to improve comfort of releasing process. Furthermore by default in Text Editor window are written commit messages since last release tag, ordered from last to first. You can use them to prepare more reliable release message.
  - **Markdown syntax** can be easily used to prepare a great release message.
- Repository check before release regarding work tree, uncommited changes etc.
- Entered a release tag during the release process are automatically checked with compliance to **Semantic Version**.
- Entered a release tag less than the previous is instantly cached and refused.
- Project `__version__` variable is automatically updated using entered release tag.
- Based on previous release tag new **Changelog** file is generated and incorporated in the new release.
- Based on authors of commits in the repository actual **AUTHORS** file is generated and incorporated in the new release.
- After generating Changelog and AUTORHS **new automatic commit** is added to the repository and **pushed to origin** if exists.

#### Make install

- Installs requirements from `requirements.txt` file.
- Installs a package or module in your Python site-packages directory.

#### Make test

- Runs `pytest` with tests from `tests` directory.
- Options for `pytest` are available in `setup.cfg` file.

#### Make coverage

- Runs `coverage` with `pytest` with tests from `tests` directory.
- Generates a html report.
- Options for `coverage` are available in `setup.cfg` file.

#### Make coverage_report

- Shows a coverage report in your default web browser.

#### Make tox

- Runs `tox` for testing.

#### Make venv

- Prepares virtual environment in `venv` directory.

#### Make format

- Runs Autopep8 formatter for the file specified as an argument.

- Original file and formatted file are opened in Meld in the merge mode to easy review changes and selectively applying them.
  - Meld is opened in the three panes:

  | NOT FORMATTED FILE | FINAL FILE | FORMATTED FILE |
  | ------------------ | ---------- | -------------- |
  | some code          | some code  | some code      |

  - After accepting or modifying changes you must save the final file.

- File to format must be provided as argument for example: `make format <path to a file>`

- Aggressive formatting settings is used in `autopep8` by default.

- After closing the Meld, a `flake8` report will be generated on the formatted file.

- When the formatted file has changes only in line endings comparing to the original file then it is treated as no changes and merging process will not be started.

#### Make lint

- Runs `flake8` with your source files.
- By default, `tests` directory is included.
- Options for `flake8` are available in `setup.cfg` file.

#### Make doc

- TODO!!!!!!!!!!!!!!

#### Make install_reqs

- Installs requirements from `requirements.txt` file.

#### Make update_reqs

- Discovers requirements and prepares `requirements.txt` and `requirements-dev.txt` files.
- `requirements.txt` file is prepared using `pipreqs` and source code directory in your repository (package directory or root repository directory for package or module repository type respectively).
- `repoassist` and `tests` directories are ignored during requirements discovery.
- `requirements-dev.txt` file is prepared based on packages required by Repoassist. 
- If `requirements.txt` file exists it will be updated.
- If `requirements-dev.txt` file exists it will not be overwritten.

#### Make clean

- Cleans repository among others from:
  - build files
  - distribution files
  - Python cache files
  - Pytest cache files

### Cloud feature

Repoassist has integrated a simple cloud manager for easy and convenient storage a generated source and binary distribution package on the cloud server. Generated files can be uploaded into a specified server using `ftp` connection and credentials from the `cloud_credentials.txt` file. It is recommended to not commit the credentials file.

Cloud feature availability can be selected during repository generation process. This feature is optional.

#### cloud_credentials.txt file

There are a few important parameters in this file:

- `server` - your server address 
- `username` - a ftp client username
- `password` - a ftp client password
- `main_bucket_path` - a directory where your files will be stored
- `client_name` - a name of the client directory in the `main bucket`
- `project_name` - a name of the project directory in the `main bucket` or `client` directory

The final path, where files will be stored is constructed from the `main_bucket_path `, `client_name `, `project_name `. For instance where all of them is specified then the path will look like following:

```
<main_bucket_path>/<client_name>/<project_name>
```

If the `client_name` or `project_name` will be omitted (for example `client_name`) , final path is constructed like this:

```
<main_bucket_path>/<project_name>
```

Only the `main_bucket_path` path is mandatory.

> `main_bucket_path`  must contain a parent directory e.g. `main_bucket_path = /fw_cloud` . Cannot be root('/'). If only the parent directory exists the rest directories will be created.

#### Server Structure

Two kind of files is generated during a releasing process: a source distribution and binary distribution package. These files are stored in separated buckets `source` and `binary` respectively. 

#### Available targets

##### Make upload

- Uploads last generated source and binary distribution packages to the cloud server.
- Confirms an existence of uploaded package on the server.

##### Make list_cloud

- Lists main bucket on the cloud server.

##### Make download_package

- Download specified package from the cloud server to the artifacts directory - `dist`
- If a file already exists in an artifacts location it will not be overwritten and an appropriate warning will be printed. 



TODO: describe versioning update mechanism

## Q&A

1. Q: How can I change the project name?
   A: For package repo - rename package directory, for module repo - rename module. Finaly change a  `name` parameter in the [metadata] section in `setup.cfg` file.
2. Q: Can I create git repository inside my project repository?
   A: Yes you could but only as git submodule.
3. Q: How can I connect given repository source distribution package with proper git commit?
   A: In the source distribution package the latest git commit hash is stored in: `<project_name>.egg-info/pbr.json` as a `git_version` parameter.
4. Q: What will happen if generate again a repository in the same directory?
   A: Without `--force` option Repoassist directory will be overwritten. With `--force` option, all generated files will be updated.







**DESCRIBE setup.cfg file**



# === UNDER CONSTRUCTION ===
Update the requirements.txt file

* Describe mechanism regarding dev release tag only in dist not in git that is set when release on different commit than last release tag commit
