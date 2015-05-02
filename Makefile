PR := piony

# Ignore all real files with names of targets.
TARGS := $(shell sed -n 's/^\([-a-z]\+\):.*/\1/p' Makefile|sort -u|xargs)
.PHONY: $(TARGS)

### DEFAULTS ###
all: test debug
dbg: udbg
test: test-exec
style: style-lint


### MAIN ###
debug: ARGS := -V a
debug-all: ARGS := -V

app:  PYARGS := -O
udbg: PYARGS := -m pudb.run
idbg: PYARGS := -m ipdb
vdbg: PYARGS := -S ~/pkg/Komodo-PythonRemoteDebugging/py3_dbgp -d localhost:9000
dasm: PYARGS := -m dis

## {-u -- unbuffered output for vim's :make}
app debug debug-all dbg idbg vdbg:
	@python3 -u $(PYARGS) ./$(PR).py $(ARGS)


### TEST ###
# {-s -- turns off capture output, !dbgrs may need!}
test-dbg: TESTARGS := --capture=no
test-lst: TESTARGS := --collect-only

test-dbg test-lst : test-exec
test-exec: export PYTHONPATH += .
test-exec:
	@py.test $(TESTARGS)  # python -m pytest my_file_test.py


### STYLE ###
style-lint: export PYTHONPATH += .
style-lint:
	@pylint --reports=no --output-format=parseable \
		--extension-pkg-whitelist=PyQt5 \
		--disable=C0111,C0103,W0613 $(PR)
# W0232,E1101

style-pep: PEP8 += --first --statistics
style-more: PEP8 += --show-source --show-pep8
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
