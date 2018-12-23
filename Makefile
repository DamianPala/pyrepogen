UNAME_S := $(shell sh -c uname -s 2>/dev/null || echo not)
ifeq ('$(findstring Linux,$(UNAME_S))', 'Linux')
	OS_DETECTED := Linux
	OS_TYPE     := Linux
else ifeq ('$(findstring CYGWIN,$(UNAME_S))', 'CYGWIN')
	OS_DETECTED := Cygwin
	OS_TYPE     := Windows
else ifeq ('$(findstring MINGW,$(UNAME_S))', 'MINGW')
	OS_DETECTED := Mingw
	OS_TYPE     := Windows
else ifeq ('$(findstring not,$(UNAME_S))$(OS)', 'notWindows_NT')
	OS_DETECTED := Windows
	OS_TYPE     := Windows
else
	OS_DETECTED := Unknown
	OS_TYPE     := Unknown
endif

ifeq ($(OS_DETECTED),Linux)
    PYTHON := python3
    NULL   := /dev/null
    WHICH  := which
endif
ifeq ($(OS_DETECTED),Cygwin)
    PYTHON := py -3
    NULL   := /dev/null
    WHICH  := which
endif
ifeq ($(OS_DETECTED),Mingw)
    PYTHON := py -3
    NULL   := /dev/null
    WHICH  := which
endif
ifeq ($(OS_DETECTED),Windows)
    PYTHON := py -3
    NULL   := NUL
    WHICH  := where
endif
ifeq ($(OS_DETECTED),Unknown)
    PYTHON := python3
    NULL   := /dev/null
    WHICH  := which
endif

RM		   := rm
TEST_PATH  := ./tests


default: prepare

prepare:
	$(PYTHON) -m pip install --user -r requirements-dev.txt
	$(PYTHON) -m pip install --user -r requirements.txt

release:
	$(PYTHON) setup.py sdist
	
install:
	$(PYTHON) setup.py install

test:
	$(PYTHON) -m pytest $(TEST_PATH) --color=yes

lint:
	$(PYTHON) -m flake8
	
doc:
	$(PYTHON) -m flake8
	
	
coverage:
	@coverage run -m pytest tests && ([ $$? -eq 0 ]) || echo ""
	@coverage html
	@coverage report -m	

	
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
