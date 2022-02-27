SHELL = /bin/bash
package = shagen/laskea

.DEFAULT_GOAL := all
isort = isort laskea tests
black = black -S -l 120 --target-version py38 laskea tests

.PHONY: install
install:
	pip install -U pip wheel
	pip install -r tests/requirements.txt
	pip install -U .

.PHONY: install-all
install-all: install
	pip install -r tests/requirements-dev.txt

.PHONY: isort
format:
	$(isort)
	$(black)

.PHONY: init
init:
	pip install -r tests/requirements.txt
	pip install -r tests/requirements-dev.txt

.PHONY: lint
lint:
	python setup.py check -ms
	flake8 laskea/ tests/
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: mypy
mypy:
	mypy laskea

.PHONY: test
test: clean
	pytest --cov=laskea --log-format="%(levelname)s %(message)s" --asyncio-mode=strict

.PHONY: testcov
testcov: test
	@echo "building coverage html"
	@coverage html

.PHONY: all
all: lint mypy testcov

.PHONY: sbom
sbom:
	@docs/third-party/gen-sbom
	@cd docs/third-party && cog -P -r -c --check --markers="[[fill ]]] [[[end]]]" -p "from gen_sbom import *" README.md

.PHONY: clean
clean:
	@rm -rf `find . -name __pycache__`
	@rm -f `find . -type f -name '*.py[co]' `
	@rm -f `find . -type f -name '*~' `
	@rm -f `find . -type f -name '.*~' `
	@rm -rf .cache
	@rm -rf htmlcov
	@rm -rf *.egg-info
	@rm -f .coverage
	@rm -f .coverage.*
	@rm -rf build
	@rm -f *.log
	python setup.py clean
