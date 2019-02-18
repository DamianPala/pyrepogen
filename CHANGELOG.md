# pyrepogen - Change Log
The Python Repository Generator.

### Version: 0.2.0 | Released: 2019-02-18 
[IPROVEMENT] Improved requirements collecting.
[FEATURE] Added venv makefile target.
[FEATURE] Added generated files git add.
[FEATURE] Added wizard config data validation.
[IMPROVEMENT] Tests directory added to pipreqs ignore as default.
[IMPROVEMENT] Added default requirements for requirements.txt
[FEATURE] Repoassist has forced file overwritten by default.
[FEATURE]: Do not interrupt releasing process when push failed when origin is set.
[FEATURE] Release message in text editor should has commit messages from the last tag by default.
[FEATURE] Release message should be entered in text editor.
[FEATURE] Check GIT version. Minimal GIT version set to 2.20.0.
[FEATURE] Create a demo project in the cwd when --demo argument provided.
[IMPROVEMENT] Check if tag was set properly by comparing get_latest_tag result with regarding tag.
[FIX] gen_repo.cfg fields corrected and updated.
[IMPROVEMENT] section name in config file is not necessary.
[IMPROVEMENT] Improved generated samples of module and package.
[FEATURE] When type make run pyrepogen should be started in wizard mode.
[IMPROVEMENT] Added keyboard interrupt signal handling in wizard.py
[FEATURE] cli.py shall be tested in UTs.
[IMPROVEMENT] Repoassist updated.
[FEATURE] Repoassist can be updated using -u option in Pyrepogen.
[IMPROVEMENT] pygittools.py refactored and integrated.
[IMPROVEMENT] Repoassist can be updated from repoassist by makefile target.
[IMPROVEMENT] Corrections after pygittools update.
[IMPROVEMENT] Removed EmptyRepositoryError.
[IMPROVEMENT] Repoassist update improved.
[FIX] When coverage report not exists then proper error will be raised.
[IMPROVEMENT] Formatter uses tempfile in system temp.
[FIX] Added missing cwd in _prompt_release_msg
[FIX] Added missing '.' in _prompt_release_tag and corrected get_latest_tag in this function.
[IMPROVEMENT] When generated file is updated print updated rather than generated.
[FEATURE] When git-origin is set then repository will be cloned and repository name not prompted.
[IMPROVEMENT] Corrected try-except blocks.
[IMPROVEMENT] Added repo-name parameter to generator config.
[IMPROVEMENT] Added double quotes stripping from path.
[IMPROVEMENT] Generated repository default version changed to 0.0.1
[FEATURE] sicloudman.py replaced cloud.py.
[FEATURE] Proper README.md file is generated in repoassist directory.
[IMPROVEMENT] Added two buckets for artifacts.
[FEATURE] Old Repoassist files will be removed after Repoassist update.
[IMPROVEMENT] reltools.py and meldformat.py integrated.
[FIX] Added missing reltools.py in Repoassist and Repoassist updated.
[FIX] Added missing AUTHORS template.

### Version: 0.1.2 | Released: 2019-01-14 
Added force option to make_install and make_release.
Full update to Python 3.7
Templates cleanup.
Corrected bug regarding sample file generation when they should not be generated.
Added authors file type selection.
Semver replaced with packaging regarding to versioning.

### Version: 0.1.1 | Released: 2019-01-12 
Corrected templates.

### Version: 0.1.0 | Released: 2019-01-12 
Initial Release.