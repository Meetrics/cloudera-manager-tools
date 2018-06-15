
PROJ_NAME ?= cloudera_manager_tools

.PHONY: install i uninstall u installdev idev

install i:
	pip install .

uninstall u:
	pip uninstall ${PROJ_NAME}

installdev idev:
	@[ "${VIRTUAL_ENV}" ] || { >&2 echo "[ERROR] Please use a virtualenv during the development."; exit 1; }
	pip install -e .
