PYTHON     := python
RM		   := rm
TEST_PATH  := ./tests


default: prepare

prepare:
	$(PYTHON) -m pip install --user -r requirements-dev.txt
	$(PYTHON) -m pip install --user -r requirements.txt

release:
	$(PYTHON) setup.py sdist
	
test:
	$(PYTHON) -m pytest $(TEST_PATH) --color=yes

lint:
	$(PYTHON) -m flake8
	
doc:
#TODO:
	$(PYTHON) -m flake8

coverage:
	@coverage run -m pytest tests && ([ $$? -eq 0 ]) || echo ""
	@coverage html
	@coverage report -m	
	
update_reqs:
	@echo "test"
	
clean:
	$(RM) -rf build/
	$(RM) -rf dist/
	$(RM) -rf *.egg-info
	$(RM) -rf AUTHORS
	$(RM) -rf ChangeLog

help:
	@echo "Usage:"
	@echo "	make <target> [flags...]"
	@echo
	@echo "Targets:"
	@echo "make prepare"
	@echo "	Prepare development environment based on requirements.txt and requirements-dev.txt, use only once"
	@echo "make release"
	@echo "	Release the package"
	@echo "make install"
	@echo "	Install the package"
	@echo "make test"
	@echo "	Run tests"
	@echo "make lint"
	@echo "	Run linter"
	@echo "make clean"
	@echo "	Clean build and distribution"
	

.PHONY: default prepare release install test lint clean help
