VERSION_AND_REVISION = $(shell git describe --tags --dirty | sed -e 's/^v//')
PKG_ID = traymenu_${VERSION_AND_REVISION}_all
PYMOD_VERSION = $(shell PYTHONPATH=../src:$$PYTHONPATH python3 -c \
                        'import traymenu; print(traymenu.__version__)')

BUILD_DIR = ./build_dir
BASE_DIR = ${BUILD_DIR}/${PKG_ID}
BIN_DIR = ${BASE_DIR}/usr/bin
LIB_DIR = ${BASE_DIR}/usr/lib/python3/dist-packages/traymenu
ICON_DIR = ${BASE_DIR}/usr/share/icons/hicolor/scalable/apps/

.PHONY: default
default:

.PHONY: deb
deb: clean create_control_file copy_files
	dpkg-deb --build --root-owner-group ${BASE_DIR}

.PHONY: create_control_file
create_control_file:
	mkdir -p ${BASE_DIR}/DEBIAN
	sed -e 's/\$$VERSION/${VERSION_AND_REVISION}/' control > ${BASE_DIR}/DEBIAN/control

.PHONY: copy_files
copy_files:
	mkdir -p ${BIN_DIR}
	mkdir -p ${LIB_DIR}
	mkdir -p ${ICON_DIR}
	cp ../src/bin/traymenu ${BIN_DIR}
	cp ../src/traymenu/*.py ${LIB_DIR}
	cp ../doc/traymenu.svg ${ICON_DIR}
	chmod -R g-w ${BASE_DIR}

.PHONY: show_version
show_version:
	@echo "Traymenu version according to git: '${VERSION_AND_REVISION}'"
	@echo "Traymenu version according to Python: '${PYMOD_VERSION}'"

.PHONY: clean
clean:
	rm -rf ${BUILD_DIR}
