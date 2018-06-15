
PROJ_NAME ?= cloudera_manager_tools

.PHONY: install i uninstall u devinit devinstall devi

define check_virtualenv
	@[ "${VIRTUAL_ENV}" ] || { >&2 echo "[ERROR] Please use a virtualenv during the development."; exit 1; }
endef

install i:
	sudo python setup.py install

uninstall u:
	sudo pip uninstall ${PROJ_NAME}
	sudo rm -f $(shell which cmt)

devinit:
	virtualenv .env
	pip install -r requirements.txt

devinstall devi:
	$(call check_virtualenv)
	pip install -e .

devuninstall devu:
	$(call check_virtualenv)
	python setup.py develop --uninstall
	sudo rm -f $(shell which cmt)

clean:
	sudo rm -rf *.egg-info .env dist build
