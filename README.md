# Pyrepogen
Pyrepogen is a python repository generator for fast and simple preparing the python project repository in standardized way. Pyrepogen provides many options to customize repository generation.

Furthermore Pyrepogen generate **Repoassist** that provides some extra features useful during your code development and maintain.

## Requirements

- Python >= 3.7
- Git >= 2.20.0

## Installation

To install pyrepogen you can use pypi: **THIS WAY IS CURRENTLY UNAVAILABLE!**

```
pip install pyrepogen
```

Or install from sources:

1. Clone or download pyrepogen repository
2. Enter to `pyrepogen` directory
3. Type `pip install -r requirements.txt`
4. Type `python setup.py install`

## Usage

There are two ways to generate a repository: wizard and a configuration file.

Pyrepogen also provides simple demo repository generation. Just type:

```
pyrepogen --demo
```

Then a repository will be generated in the `demo_project` directory at your current working directory.

### Wizard

To run wizard, type `pyrepogen` in your command line terminal and follow the wizard.

### Config file

In the case when you want to generate many repositories, using a predefined configuration file is the best solution.  Just prepare a configuration file using following template and save it on your hard drive:

```
# Required parameters:
# Possible values: package or script
project-type = 
repo-name = 
project-name = 
author = 
author-email = 
short-description = 
# Possible values: generated or prepared
changelog-type = 
# Possible values: generated or prepared
authors-type = 

# Optional parameters:
maintainer = 
maintainer-email = 
home-page = 
# Possible values: true or false
is-cloud = 
# Possible values: true or false 
is-sample-layout = 
# Possible values: true or false 
is-git = 
# Possible values: true or false
git-origin = 
```

The next step is to run pyrepogen with specified configuration file:

```
pyrepogen <path to repo you want to create> -c <path to config file>
```

> Always specify paths with double quotes!

#### Config parameters

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

## Repoassist







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