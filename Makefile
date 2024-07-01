# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

include .env
export

DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Available rules:"
	@fgrep -h "##" Makefile | fgrep -v fgrep | sed 's/\(.*\):.*##/\1:  /'

.env:
	cp env_tmpl .env

.venv:
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt

.PHONY: build_venv
build_venv:  ## Rebild the virtual environment
	-rm -rf .venv
	$(MAKE) .venv

.PHONY: run
run: .venv  ## Run script
	.venv/bin/python do_supersearch.py
