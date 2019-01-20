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
2. Automatically generated in current working directory when you run Pyrepogen with only `repo_path` parameter.
3. By copying from sources the `gen_repo.cfg` file.

#### Config file template

```
# Required parameters:
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
pyrepogen <path to repo you want to create>
```

> Always specify paths with double quotes when you type space - " " in it!

When your config file is not in your current working directory or it has a different name, you can specify it using `-c` option:

```
pyrepogen <path to repo you want to create> -c <path to config file>
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

### Available Options

| Option        | Description                                                  |
| ------------- | ------------------------------------------------------------ |
| repo_path   | Repo name or path to the directory when the repository will be generated. If directory does not exist then will be created. Always enter with double quotes. |
| &#x2011;c/&#x2011;&#x2011;config | Path to the repository config file. |
| &#x2011;q/&#x2011;&#x2011;quiet | Disable output. |
| &#x2011;d/&#x2011;&#x2011;debug   | Enable debug output. |
| &#x2011;f/&#x2011;&#x2011;force | Override existing files. |
| &#x2011;v/&#x2011;&#x2011;version | Show version. |
| --demo | Generate a demo repository in your current working directory. |



# Repoassist







# === UNDER CONSTRUCTION ===
# Features
- collect requirements as makefile target
- autonomus package with e.g. colreqs.py in generated repository as helper to makefile targets
- ChangeLog and AUTHORS not in repo tree
- when regenerate release package, changelog and authors are not regenerated

# Standalone Script Repo
## Targets
### release
* Generate the ChangeLog file based a git repository
* Generate the AUTHORS file based a git repository
* Update the requirements.txt file
* Prepare the Release Package in `dist` directory containing all files that are in the git repository tree

Describe clean target

Source distribution of module repo is made as package

Regenerate release package has hash in package name if release tag is not on last commit
When regenerate on the same commit as tag - dist will be overwritten and without a commit hash

When you change project name in tree always change it in setup.cfg

Repo inside parent repo without submodule is not allowed

Commit hash is stored into .egg-info/pbr.json as git_version

Describe mechanism regarding dev release tag only in dist not in git that is set when release on different commit than last release tag commit

If generate repo in the same directory as is without force, repoassist is overwritten by default

Repoassist update target

path as argument in pyrepogen must be entered with double quotes