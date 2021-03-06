#/***************************************************************************
# MassiveChangeDetection
#
# Change detection tool
#							 -------------------
#		begin				: 2018-06-26
#		git sha				: $Format:%H$
#		copyright			: (C) 2018 by Dymaxion Labs
#		email				: contact@dymaxionlabs.com
# ***************************************************************************/
#
#/***************************************************************************
# *																		 *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or	 *
# *   (at your option) any later version.								   *
# *																		 *
# ***************************************************************************/

#################################################
# Edit the following to match your sources lists
#################################################


.PHONY: docker_build docker_prepare docker_run test

#Add iso code for any locales you want to support here (space separated)
# default is no locales
LOCALES = es

# If locales are enabled, set the name of the lrelease binary on your system. If
# you have trouble compiling the translations, you may have to specify the full path to
# lrelease
LRELEASE = lrelease
#LRELEASE = lrelease-qt4

# translation
SOURCES = \
	__init__.py \
	massive_change_detection.py \
	provider.py \
	algorithm.py

PLUGINNAME = massive-change-detection

PY_FILES = \
	__init__.py \
	massive_change_detection.py \
	provider.py \
	algorithm.py

EXTRAS = \
	CHANGELOG.md \
	LICENSE.md \
	metadata.txt \
	README.md

EXTRA_DIRS =

PEP8EXCLUDE=pydev,resources.py,conf.py,third_party,ui


#################################################
# Normally you would not need to edit below here
#################################################

VERSION ?= $(shell grep 'version=' metadata.txt | cut -d'=' -f2)

BUILD_DIR ?= $(CURDIR)

HELP = help/build/html

PLUGIN_UPLOAD = $(c)/plugin_upload.py

RESOURCE_SRC=$(shell grep '^ *<file'  | sed 's@</file>@@g;s/.*>//g' | tr '\n' ' ')

QGISDIR=.qgis2

default: test

%.py : %.qrc $(RESOURCES_SRC)
	pyrcc4 -o $*.py  $<

%.qm : %.ts
	$(LRELEASE) $<

test:
	@echo
	@echo "----------------------"
	@echo "Regression Test Suite"
	@echo "----------------------"

	@# Preceding dash means that make will continue in case of errors
	@rm -f .coverage
	@-export PYTHONPATH=`pwd`:$(PYTHONPATH); \
		export QGIS_DEBUG=0; \
		export QGIS_LOG_FILE=/dev/null; \
		nosetests -v --with-id --with-coverage --cover-package=. \
		3>&1 1>&2 2>&3 3>&- || true
	@echo "----------------------"
	@echo "If you get a 'no module named qgis.core error, try sourcing"
	@echo "the helper script we have provided first then run make test."
	@echo "e.g. source run-env-linux.sh <path to qgis install>; make test"
	@echo "----------------------"

deploy: doc transcompile
	@echo
	@echo "------------------------------------------"
	@echo "Deploying plugin to your .qgis2 directory."
	@echo "------------------------------------------"
	# The deploy  target only works on unix like operating system where
	# the Python plugin directory is located at:
	# $HOME/$(QGISDIR)/python/plugins
	mkdir -p $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vf $(PY_FILES) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vf $(EXTRAS) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vfr i18n $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vfr $(HELP) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)/help

# The dclean target removes compiled python files from plugin directory
# also deletes any .git entry
dclean:
	@echo
	@echo "-----------------------------------"
	@echo "Removing any compiled python files."
	@echo "-----------------------------------"
	find $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME) -iname "*.pyc" -delete
	find $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME) -iname ".git" -prune -exec rm -Rf {} \;

derase:
	@echo
	@echo "-------------------------"
	@echo "Removing deployed plugin."
	@echo "-------------------------"
	rm -Rf $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)

zip: deploy dclean
	@echo
	@echo "---------------------------"
	@echo "Creating plugin zip bundle."
	@echo "---------------------------"
	# The zip target deploys the plugin and creates a zip file with the deployed
	# content. You can then upload the zip file on http://plugins.qgis.org
	mkdir -p dist/
	rm -f dist/$(PLUGINNAME)-$(VERSION).zip
	cd $(HOME)/$(QGISDIR)/python/plugins; zip -9r $(CURDIR)/dist/$(PLUGINNAME)-$(VERSION).zip $(PLUGINNAME)

package:
	# Create a zip package of the plugin named $(PLUGINNAME).zip.
	# This requires use of git (your plugin development directory must be a
	# git repository).
	# To use, pass a valid commit or tag as follows:
	#   make package VERSION=Version_0.3.2
	@echo
	@echo "------------------------------------"
	@echo "Exporting plugin to zip package.	"
	@echo "------------------------------------"
	mkdir -p dist/
	rm -f dist/$(PLUGINNAME)-$(VERSION).zip
	git archive --prefix=$(PLUGINNAME)/ -o dist/$(PLUGINNAME)-$(VERSION).zip $(VERSION)
	echo "Created package: dist/$(PLUGINNAME)-$(VERSION).zip"

transup:
	@echo
	@echo "------------------------------------------------"
	@echo "Updating translation files with any new strings."
	@echo "------------------------------------------------"
	@chmod +x scripts/update-strings.sh
	@scripts/update-strings.sh $(LOCALES)

transcompile:
	@echo
	@echo "----------------------------------------"
	@echo "Compiled translation files to .qm files."
	@echo "----------------------------------------"
	@chmod +x scripts/compile-strings.sh
	@scripts/compile-strings.sh $(LRELEASE) $(LOCALES)

transclean:
	@echo
	@echo "------------------------------------"
	@echo "Removing compiled translation files."
	@echo "------------------------------------"
	rm -f i18n/*.qm

doc:
	@echo
	@echo "------------------------------------"
	@echo "Building documentation using sphinx."
	@echo "------------------------------------"
	cd help; make html

pylint:
	@echo
	@echo "-----------------"
	@echo "Pylint violations"
	@echo "-----------------"
	@pylint --reports=n --rcfile=pylintrc . || true
	@echo
	@echo "----------------------"
	@echo "If you get a 'no module named qgis.core' error, try sourcing"
	@echo "the helper script we have provided first then run make pylint."
	@echo "e.g. source run-env-linux.sh <path to qgis install>; make pylint"
	@echo "----------------------"

# Run pep8 style checking
#http://pypi.python.org/pypi/pep8
pep8:
	@echo
	@echo "-----------"
	@echo "PEP8 issues"
	@echo "-----------"
	@pep8 --repeat --ignore=E203,E121,E122,E123,E124,E125,E126,E127,E128 --exclude $(PEP8EXCLUDE) . || true
	@echo "-----------"
	@echo "Ignored in PEP8 check:"
	@echo $(PEP8EXCLUDE)

docker_build:
	@docker build -t dymaxionlabs/massive-change-detection-test-env .

docker_prepare:
	docker run -d --name massive-change-detection-test-env -v $(BUILD_DIR):/tests_directory/$(PLUGINNAME) -e DISPLAY=:99 dymaxionlabs/massive-change-detection-test-env
	sleep 3
	docker exec -it massive-change-detection-test-env sh -c "qgis_setup.sh $(PLUGINNAME)"

docker_run:
	docker exec -it massive-change-detection-test-env sh -c "cd /tests_directory/$(PLUGINNAME) && make test"

clean:
	rm -rf dist/

publish: zip
ifndef QGIS_REPOSITORY_PATH
	$(error QGIS_REPOSITORY_PATH is undefined)
endif
	cp dist/$(PLUGINNAME)-$(VERSION).zip $(QGIS_REPOSITORY_PATH)/$(PLUGINNAME)/
