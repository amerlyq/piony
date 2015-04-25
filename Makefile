PR := piony

all: test app

### MAIN ###
app:
	@./$(PR).py


### TESTS ###
test: export PYTHONPATH := .:$(PYTHONPATH)
test:
	py.test
list-tests:
	py.test --collect-only

style-lint:
	pylint $(PR) | less

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


.PHONY: all app changelog collect deploy keys test
