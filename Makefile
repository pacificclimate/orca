export PIP_INDEX_URL=https://pypi.pacificclimate.org/simple

# Setup venv
ifeq ($(TMPDIR),)
VENV_PATH := /tmp/orca-venv
else
VENV_PATH := $(TMPDIR)/orca-venv
endif

# Makefile Vars
SHELL:=/bin/bash
PYTHON=${VENV_PATH}/bin/python3
PIP=${VENV_PATH}/bin/pip


.PHONY: all
all: install test pre-commit-hook

.PHONY: install
install: venv
	${PIP} install -U pip
	${PIP} install -r requirements.txt -r test_requirements.txt
	${PIP} install -e .

.PHONY: pre-commit-hook
pre-commit-hook: venv
	${PIP} install pre-commit
	pre-commit install

.PHONY: test
test: venv
	${PYTHON} -m pytest -v --cov=orca --cov-report term-missing tests/

.PHONY: venv
venv:
	test -d $(VENV_PATH) || python3 -m venv $(VENV_PATH)

.PHONY: performance
performance: venv install
	${PIP} install snakeviz
	${PYTHON} -m cProfile -o program.prof scripts/process.py -p /storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_CSIRO-Mk3-6-0_historical+rcp85_r1i1p1_19500101-21001231.nc -t tasmax[0:1:15000][0:1:91][0:1:206] -l DEBUG
	${PYTHON} -m snakeviz program.prof

.PHONY: prod-app
prod-app: venv install
	${PIP} install gunicorn
	source ${VENV_PATH}/bin/activate && gunicorn --bind=0.0.0.0:5000 'orca:create_app()'

.PHONY: dev-app
dev-app: venv install
	${PIP} install gunicorn
	source ${VENV_PATH}/bin/activate && gunicorn --bind=0.0.0.0:5000 'orca:create_app("config.DevConfig")'

.PHONY: test-app
test-app: venv install
	${PIP} install gunicorn
	source ${VENV_PATH}/bin/activate && gunicorn --bind=0.0.0.0:5000 'orca:create_app("config.TestConfig")'
