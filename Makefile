PR := piony

# Ignore all real files with names of targets.
TARGS := $(shell sed -n 's/^\([-a-z]\+\):.*/\1/p' Makefile|sort -u|xargs)
.PHONY: $(TARGS)

### DEFAULTS ###
# USAGE: make dbg A="[a,b]"
all: test debug
dbg: idbg
test: test-exec
style: style-lint

### MAIN ###
debug: ARGS += -V k
debug-all: ARGS += -V a

app:  PYARGS += -O
udbg: PYARGS += -m pudb.run
idbg: PYARGS += -m ipdb
vdbg: PYARGS += -S ~/pkg/Komodo-PythonRemoteDebugging/pydbgp -d localhost:9000
# py3_dbgp
dasm: PYARGS += -m dis

## {-u -- unbuffered output for vim's :make}
debug debug-all app udbg idbg vdbg dasm:
	python3 -u $(PYARGS) ./$(PR).py $(ARGS) $(A)


### TEST ###
# {-s -- turns off capture output, !dbgrs may need!}
test-dbg: MODARGS += --capture=no
test-lst: MODARGS += --collect-only

test-dbg test-lst: test-exec
test-exec: export PYTHONPATH += .
test-exec:
	@py.test $(MODARGS)  # python -m pytest my_file_test.py


### STYLE ###
style-lint: export PYTHONPATH += .
style-lint:
	@pylint --reports=no --output-format=parseable \
		--extension-pkg-whitelist=PyQt5 \
		--disable=C0111,C0103,W0613 $(PR)
# W0232,E1101

style-pep:  MODARGS += --first --statistics
style-more: MODARGS += --show-source --show-pep8
style-pep style-more:
	@pep8 $(PEP8)


### SETUP ###
keys:
	xbindkeys -mk


### USAGE ###
# ALT: {-B -- don't write .pyc}
clean:
	find . -name "*.pyc" -exec rm {} \;
deploy:
	@./scripts/deploy
log:
	@./scripts/show-changelog
help:
	@echo "Use one of those targets: $(TARGS)"
