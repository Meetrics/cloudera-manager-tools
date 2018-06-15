
PROJ_NAME ?= cloudera_manager_tools

.PHONY: install i uninstall u initdev installdev idev

install i:
	sudo python setup.py install

uninstall u:
	sudo pip uninstall ${PROJ_NAME}
	sudo rm -f $(shell which cmt)

initdev:
	virtualenv .env
	pip install -r requirements.txt

installdev idev:
	@[ "${VIRTUAL_ENV}" ] || { >&2 echo "[ERROR] Please use a virtualenv during the development."; exit 1; }
	pip install -e .

clean:
	sudo rm -r *.egg-info .env dist build
