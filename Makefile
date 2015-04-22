.PHONY: all app collect deploy keys test

all: test app

app:
	@./piony.py

# USAGE: http://pytest.org/latest/usage.html#cmdline
test: export PYTHONPATH := .:$(PYTHONPATH)
test:
	py.test

collect:
	py.test --collect-only

keys:
	xbindkeys -mk

deploy:
	@./deploy
