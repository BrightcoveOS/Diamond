DESTDIR=/
PROJECT=diamond
VERSION=4.0.0
RELEASE := $(shell ls -1 dist/*.noarch.rpm 2>/dev/null | wc -l )
PLATFORM := $(shell uname -p)

all:
	@echo "make run      - Run Diamond from this directory"
	@echo "make config   - Run a simple configuration CLI program"
	@echo "make watch    - Watch and continuously run tests"
	@echo "make test     - Run tests"
	@echo "make docs     - Build docs"
	@echo "make sdist    - Create source package"
	@echo "make bdist    - Create binary package"
	@echo "make install  - Install on local system"
	@echo "make rpm      - Generate a rpm package"
	@echo "make deb      - Generate a deb package"
	@echo "make tar      - Generate a tar ball"
	@echo "make pkg      - Generate a solaris package"
	@echo "make clean    - Get rid of scratch and byte files"
	@echo "make cleanws  - Strip trailing whitespaces from files"

run:
	./bin/diamond --configfile=conf/diamond.conf --foreground

config:
	./bin/diamond-setup --configfile=conf/diamond.conf

watch:
	watchr test.watchr

test:
	./test.py

docs:
	./build_doc.py --configfile=conf/diamond.conf

sdist:
	./setup.py sdist --prune

bdist:
	./setup.py bdist --prune

install:
	./setup.py install --root $(DESTDIR)

rpm: buildrpm

buildrpm: sdist
	./setup.py bdist_rpm \
		--post-install=rpm/postinstall \
		--pre-uninstall=rpm/preuninstall \
		--install-script=rpm/install \
		--release=`ls dist/*.noarch.rpm | wc -l`

deb: builddeb

builddeb: sdist
	mkdir -p build
	tar -C build -zxf dist/$(PROJECT)-$(VERSION).tar.gz
	(cd build/$(PROJECT)-$(VERSION) && debuild -us -uc)

tar: sdist

pkg: buildpkg

buildpkg:
	./setup.py bdist
	mkdir -p build/root/ build/pkg/
	cd build/root/ && tar -xvf ../../dist/$(PROJECT)-$(VERSION)*.tar.gz
	echo "i pkginfo" > sunos/Prototype
	echo "i checkinstall" >> sunos/Prototype
	cd build/root/ && find . -print | pkgproto | cut -d ' ' -f 1-4 | awk '{ print $$0 " root root"}' >> ../../sunos/Prototype 
	cd sunos/ && pkgmk -o -r ../build/root/ -d ../build/pkg/ -f Prototype
	cd build/pkg && pkgtrans -s . ../../dist/$(PROJECT)-$(VERSION).$(PLATFORM).pkg diamond
	cd dist && gzip $(PROJECT)-$(VERSION).$(PLATFORM).pkg

clean:
	./setup.py clean
	rm -rf dist build MANIFEST
	find . -name '*.pyc' -exec rm {} \;

cleanws:
	find . -name '*.py' -exec sed -i'' -e 's/[ \t]*$$//' {} \;

reltest:
	echo "${RELEASE}"

.PHONY: run watch config test docs sdist bdist install rpm buildrpm deb builddeb tar clean cleanws reltest
