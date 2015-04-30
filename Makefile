PR := piony

all: test debug

### MAIN ###
app:
	@python3 -O $(PR).py
debug:
	@./$(PR).py -V a
debug-all:
	@./$(PR).py -V
clean:
	find . -name "*.pyc" -exec rm {} \;


### TESTS ###
test: export PYTHONPATH := .:$(PYTHONPATH)
test:
	py.test
list-tests:
	py.test --collect-only

style-lint:
	pylint --disable=C0111 $(PR) | less

style-pep8-info: PEP8=--show-source --show-pep8
style-pep8-info: style-pep8
style-pep8:
	pep8 --first --format=pylint #--statistics


### SETUP ###
keys:
	xbindkeys -mk


### USAGE ###
deploy:
	@./deploy


### INFO ###
changelog:
	@./scripts/show-changelog

#:.!cat % | sed -n '/^\([-a-z0-9]\+\):.*/s//\1/p' | sort -u | xargs
.PHONY: all app changelog debug deploy keys list-tests style-lint style-pep8 style-pep8-info test
