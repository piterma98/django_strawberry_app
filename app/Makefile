# --- prologue ---
#
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables
.DELETE_ON_ERROR:
.ONESHELL:

# --- variables ---

project_name := django_strawberry_app
python_version := 3.11.1
python_bin := $(HOME)/.pyenv/versions/$(python_version)/bin/python
database_name := postgres_django_strawberry
locale_dir := locale
pytest_options := --cov=.. --cov-report=term

# Check if we have an external virtualenv (like one created with
# virtualenvwrapper). If so, we should use that one.
check_external_virtualenv := $(shell test -d "$(WORKON_HOME)/$(project_name)" && echo $$?)
ifneq ($(check_external_virtualenv), 0)
$(shell test -d .venv || $(python_bin) -m venv .venv)
virtualenv_path := .venv
else
virtualenv_path := $(WORKON_HOME)/$(project_name)
endif

virtualenv_pip := $(virtualenv_path)/bin/pip
virtualenv_python := $(virtualenv_path)/bin/python
virtualenv_precommit := $(virtualenv_path)/bin/pre-commit
virtualenv_coverage := $(virtualenv_path)/bin/coverage

virtualenv_python_version := $(shell $(virtualenv_python) -V)
ifneq ($(virtualenv_python_version),Python $(python_version))
$(warning "Virtualenv is too old, needs upgrade from $(virtualenv_python_version) to $(python_version)")
# bump modification dates on requirements so that they get properly reinstalled
# after upgrading the entire virtualenv
$(shell rm -rf .venv requirements/*.sentinel && $(python_bin) -m venv .venv && touch requirements/*.txt)
endif

# --- targets ---

.PHONY: debug-venv help ensure-database compile-requirements upgrade-package test benchmark coverage-report check docs-html clean run
.DEFAULT_GOAL := help

debug-venv: ## Debug virtualenv-related Makefile variables
	@echo "Project name: $(project_name)"
	@echo "Virtualenv path: $(virtualenv_path)"

help: ## Show this help and exit
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

../$(database_name):
	mkdir -p $@

ensure-database: ../$(database_name) ## Make sure Postgres container is up and test database exists
	@postgres_output=$$(docker-compose up -d $(database_name) 2>&1)
	if [[ $$postgres_output =~ Creating|Starting ]]; then
		echo "Waiting for $(database_name) to start...";
		sleep 5;
	fi
	postgres_container=$$(docker ps | grep '$(database_name)' | cut -f1 -d ' ')
	docker exec -i $$postgres_container psql -U postgres -c 'create database testdb' > /dev/null 2>&1 || true

compile-requirements: ## Regenerate lockfiles from loosely defined requirements files
	$(virtualenv_pip) install pip-tools --upgrade
	@pip-compile --quiet --generate-hashes --allow-unsafe --resolver=backtracking --output-file=requirements/base.txt requirements/base.in
	@pip-compile --quiet --generate-hashes --allow-unsafe --resolver=backtracking --output-file=requirements/dev.txt requirements/dev.in

upgrade-package: ## Upgrade a single package in all lockfiles
ifdef PACKAGE
	@pip-compile --allow-unsafe --generate-hashes --upgrade-package $(PACKAGE) --output-file=requirements/dev.txt requirements/dev.in
	@pip-compile --allow-unsafe --generate-hashes --upgrade-package $(PACKAGE) --output-file=requirements/base.txt requirements/base.in
else
	@echo "Usage: make PACKAGE=django upgrade-package"
	exit 1
endif

requirements/.dev.sentinel: requirements/base.txt requirements/dev.txt
	$(virtualenv_pip) install pip --upgrade
	$(virtualenv_pip) install -r requirements/dev.txt
	touch $@

test: requirements/.dev.sentinel ensure-database ## Run entire test suite and emit coverage terminal report
	# cleanup after running tests
	# see: https://stackoverflow.com/questions/28597794
	$(virtualenv_python) -m pytest $(pytest_options) --benchmark-skip

benchmark: requirements/.dev.sentinel ## Run all benchmarks
	$(virtualenv_python) -m pytest $(pytest_options) --benchmark-only

coverage-report: test ## Emit HTML coverage report after running tests
	$(virtualenv_coverage) html

check: requirements/.dev.sentinel ## Run linters and style checkers
	$(virtualenv_precommit) run --all-files

docs-html: ../docs requirements/.dev.sentinel ## Build technical documentation
	$(virtualenv_sphinx) -b html ../docs ../docs/_build/html -n --keep-going

clean: ## Remove local virtualenv and any intermediate files
	rm -rf .venv
	rm -rf requirements/*.sentinel

ver-%:
	@echo "Tagging and pushing $(project_name) $*"
	git tag ver-$*
	git push origin ver-$*

run: requirements/.dev.sentinel ensure-database
	$(virtualenv_python) manage.py runserver