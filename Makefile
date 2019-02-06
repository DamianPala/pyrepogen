PYTHON     := python
TEST_PATH  := ./tests


ifeq (release,$(firstword $(MAKECMDGOALS)))
RELEASE_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(RELEASE_ARGS):;@:)
endif

ifeq (format,$(firstword $(MAKECMDGOALS)))
FORMAT_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(FORMAT_ARGS):;@:)
endif


default: prepare

requirements:
	@echo "Repository requirements:"
	@echo "    1. Required Python version: 3.7"
	@echo "    2. Installed Pip"
	@echo "    2. Installed Meld Merge and added into the PATH envorinment variable"

run:
	@$(PYTHON) -m pyrepogen

prepare:
	@$(PYTHON) -m pip install -r requirements-dev.txt
	@$(PYTHON) -m pip install -r requirements.txt
	
update:
	@$(PYTHON) -m repoassist update

release:
	@$(PYTHON) -m repoassist release $(RELEASE_ARGS)
	
install:
	@$(PYTHON) -m pip install -r requirements.txt
	@$(PYTHON) setup.py install
	
test:
	@$(PYTHON) -m pytest $(TEST_PATH) --color=yes
	
coverage:
	@coverage run -m pytest $(TEST_PATH) --color=yes && ([ $$? -eq 0 ]) || echo ""
	@coverage html
	@coverage report -m
	
coverage_report:
	@$(PYTHON) -m repoassist coverage_report
	
tox:
	@tox

format:
	@$(PYTHON) -m repoassist format $(FORMAT_ARGS)
	
lint:
	@$(PYTHON) -m flake8
	
#TODO:
doc:
	@$(PYTHON) -m flake8

install_reqs:
	@$(PYTHON) -m pip install -r requirements.txt

update_reqs:
	@$(PYTHON) -m repoassist update_reqs

upload:
	@echo "Run Package Uploader!"
	@$(PYTHON) -m repoassist upload
	
list_cloud:
	@echo "List buckets on the cloud server!"
	@$(PYTHON) -m repoassist list_cloud
	
download_package:
	@echo "Run Package Downloader!"
	@$(PYTHON) -m repoassist download_package
	
clean:
	@$(PYTHON) -m repoassist clean

help:
	@echo "Usage:"
	@echo "	make <target> [flags...]"
	@echo
	@echo "Targets:"
	
	@echo "make requirements"
	@echo "	List necessary repository requirements."

	@echo "make run"
	@echo "	Run Pyrepogen"
	
	@echo "make prepare"
	@echo "	Prepare a development environment based on the requirements.txt and requirements-dev.txt, use only once"

	@echo "make update"
	@echo "	Update Repoassist to version from installed Pyrepogen."
	
	@echo "make release"
	@echo "	Release the package"
	@echo "	Usage: make release [force]"
	@echo "	If you want to omit repository check and git check type: make release force"
	
	@echo "make install"
	@echo "	Install the package"
	
	@echo "make test"
	@echo "	Run tests using pytest"
	
	@echo "make coverage"
	@echo "	Run test coverage"
	
	@echo "make coverage_report"
	@echo "	Show the html coverage report in the default system browser"
	
	@echo "make tox"
	@echo "	Run tox"
	
	@echo "make format"
	@echo "	Run autopep8 formatter for file specified as argument in merge mode"
	@echo "	Usage: make format <path to file to be formatted>"
	
	@echo "make lint"
	@echo "	Run linter"
	
	@echo "make doc"
	@echo "	Generate documentation"
	
	@echo "make install_reqs"
	@echo "	Install requirements.txt"
	
	@echo "make update_reqs"
	@echo "	Update requirements.txt"
	
	@echo "make upload"
	@echo "	Upload packages from artifacts to the cloud server."
	
	@echo "make list_cloud"
	@echo "	List buckets on the cloud server."
	
	@echo "make download_package"
	@echo "	Download specified package from the cloud server."
	
	@echo "make clean"
	@echo "	Clean build and distribution"
	

.PHONY: default requirements run prepare update release install test coverage coverage_report tox format \
	lint doc install_reqs update_reqs upload list_cloud download_package clean help
