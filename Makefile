SHELL = /bin/bash
package = shagen/laskea

.DEFAULT_GOAL := all
isort = isort --skip-glob 'laskea/api/jql*' laskea tests
black = black -S -l 120 --target-version py38 --exclude 'laskea/api/jql*' laskea tests

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
	flake8 --exclude 'laskea/api/jql*' laskea/ tests/
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: mypy
mypy:
	mypy --exclude 'laskea/api/jql*' laskea

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
	@./gen-sbom
	@cog -I. -P -c -r --check --markers="[[fill ]]] [[[end]]]" -p "from gen_sbom import *;from gen_licenses import *" docs/third-party/README.md

.PHONY: version
version:
	@cog -I. -P -c -r --check --markers="[[fill ]]] [[[end]]]" -p "from gen_version import *" pyproject.toml laskea/__init__.py

.PHONY: secure
secure:
	@bandit -r -x test_laskea.py,test_cli.py .

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
