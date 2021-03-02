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
	${PYTHON} -m cProfile -o program.prof scripts/process.py --url "https://data.pacificclimate.org/data/downscaled_gcms/tasmax_day_BCCAQv2+ANUSPLIN300_CanESM2_historical+rcp85_r1i1p1_19500101-21001231.nc.nc?tasmax[0:15000][0:91][0:206]&" --unique-id tasmax_day_BCCAQv2_CanESM2_historical-rcp85_r1i1p1_19500101-21001231_Canada -l DEBUG
	${PYTHON} -m snakeviz program.prof
