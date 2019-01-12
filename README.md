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
