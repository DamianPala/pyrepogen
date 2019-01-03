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